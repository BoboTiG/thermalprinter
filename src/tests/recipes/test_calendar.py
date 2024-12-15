from __future__ import annotations

from typing import TYPE_CHECKING, Any
from unittest.mock import MagicMock, patch

import icalevents.icaldownload
import pytest
from freezegun import freeze_time

import thermalprinter.recipes.calendar
from thermalprinter import ThermalPrinter
from thermalprinter.recipes.calendar import Calendar
from thermalprinter.recipes.calendar.__main__ import main

if TYPE_CHECKING:
    from pathlib import Path
    from typing import Generator

    from _typeshed import ReadableBuffer

    from thermalprinter.recipes.calendar import Birthdays


URL = "https://example.org/remote.php/dav/public-calendars/xxx?export"
RESPONSE = """\
BEGIN:VCALENDAR
VERSION:2.0

BEGIN:VEVENT
SUMMARY:Noël au Château
DTSTART;TZID=Europe/Paris:20241214T150000
DTEND;TZID=Europe/Paris:20241214T180000
END:VEVENT

BEGIN:VEVENT
SUMMARY:Débroussaillage
DTSTART;TZID=Europe/Paris:20240814T100000
DTEND;TZID=Europe/Paris:20240814T120000
END:VEVENT

END:VCALENDAR
"""


@pytest.fixture
def calendar() -> Generator[Calendar]:
    with freeze_time("2024-12-14"), Calendar(URL) as cls:
        yield cls


def test_forge_header_image(calendar: Calendar) -> None:
    image = calendar.forge_header_image()
    assert image.size == (189, 197)


@pytest.mark.parametrize(
    ("data", "expected"),
    [
        ("2000-12-14 = Alice", [("Alice", 24)]),
        ("2000-12-14 = Alice\n1986-12-14 = Bob", [("Alice", 24), ("Bob", 38)]),
        ("2000-12-15 = Alice", []),
    ],
)
def test_get_birthdays(data: str, expected: Birthdays, calendar: Calendar, tmp_path: Path) -> None:
    birdthdays_file = tmp_path / "birthdays.lst"
    birdthdays_file.write_text(f"{data}\n")

    with patch.object(thermalprinter.recipes.calendar, "BIRTHDAYS_FILE", birdthdays_file):
        assert calendar.get_birthdays() == expected


def test_get_events(calendar: Calendar) -> None:
    with patch.object(icalevents.icaldownload.ICalDownload, "data_from_url", return_value=RESPONSE):
        assert calendar.get_events() == [("14:00", "17:00", "Noël au Château")]


def test_print_data(calendar: Calendar, printer: ThermalPrinter) -> None:
    result: list[str] = []
    out_orig = printer.out

    def out(*args: Any, **kwargs: Any) -> None:
        result.extend(args)
        out_orig(*args, **kwargs)

    events = [("08:00", "12:00", "Débroussaillage"), ("14:00", "17:00", "Noël au Château")]
    birdthdays = [("Alice", 24)]

    with patch.object(icalevents.icaldownload.ICalDownload, "data_from_url", return_value=RESPONSE):  # noqa: SIM117
        with patch.object(printer, "out", out):
            calendar.printer = printer
            calendar.print_data(events, birdthdays)

    assert result == [
        "C'est l'anniversaire de...",
        "  ... Alice (24) !",
        b"\xd5",
        b"\xcd" * 30,
        b"\xb8",
        b"\xb3",
        " 08:00 - 12:00                ",
        b"\xb3",
        b"\xb3",
        " Débroussaillage              ",
        b"\xb3",
        b"\xc3",
        b"\xc4" * 30,
        b"\xb4",
        b"\xb3",
        " 14:00 - 17:00                ",
        b"\xb3",
        b"\xb3",
        " Noël au Château              ",
        b"\xb3",
        b"\xd4",
        b"\xcd" * 30,
        b"\xbe",
        "Belle journée :)",
    ]


@freeze_time("2024-12-14")
@patch.object(icalevents.icaldownload.ICalDownload, "data_from_url", return_value=RESPONSE)
@patch("sys.argv", ["print-calendar", URL])
def test_main(mocked_sys_argv: MagicMock) -> None:  # noqa: ARG001
    assert main() == 0


@freeze_time("2024-12-14")
@patch.object(icalevents.icaldownload.ICalDownload, "data_from_url", return_value=RESPONSE)
@patch("sys.argv", ["print-calendar", URL, "--port", "loop://"])
def test_main_with_port(mocked_sys_argv: MagicMock, tmp_path: Path) -> None:  # noqa: ARG001
    write_orig = ThermalPrinter.write

    def write(self: ThermalPrinter, data: ReadableBuffer, *, should_log: bool = True) -> int | None:
        if should_log:
            return write_orig(self, data, should_log=should_log)

        # We are writing a lot of data: the image, and it make the test serial device queue full.
        # Let's skip it.
        return None

    with patch("thermalprinter.constants.STATS_FILE", f"{tmp_path}/stats.json"):  # noqa: SIM117
        with patch.object(ThermalPrinter, "write", write):
            assert main() == 0

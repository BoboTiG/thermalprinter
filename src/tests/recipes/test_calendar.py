from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from subprocess import check_call
from typing import TYPE_CHECKING, Any
from unittest.mock import MagicMock, patch

import icalevents.icaldownload
import pytest
from freezegun import freeze_time
from icalevents.icalparser import create_event

from thermalprinter import ThermalPrinter

try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo  # type: ignore[no-redef]

if TYPE_CHECKING:
    from pathlib import Path
    from typing import Generator

    from _typeshed import ReadableBuffer

    from thermalprinter.recipes.calendar import Birthdays

pytest.importorskip("thermalprinter.recipes.calendar", reason="The [calendar] extra dependencies are not installed.")

from thermalprinter.recipes.calendar import TIMEZONE, UNTIL, WHOLE_DAY, Calendar, format_event_date  # noqa: E402

TZ = ZoneInfo(TIMEZONE)
TODAY = datetime(2024, 12, 14, tzinfo=TZ)
URL = "https://example.org/remote.php/dav/public-calendars/xxx?export"

EVENTS_SINGLE_DAY = """\
BEGIN:VCALENDAR
VERSION:2.0

BEGIN:VEVENT
SUMMARY:Noël au Château
DTSTART;TZID=Europe/Paris:20241214T150000
DTEND;TZID=Europe/Paris:20241214T180000
END:VEVENT

BEGIN:VEVENT
SUMMARY:HR Zoom
DTSTART;TZID=America/New_York:20241214T080000
DTEND;TZID=America/New_York:20241214T083000
END:VEVENT

END:VCALENDAR
"""
EVENTS_SINGLE_DAY_RES = [
    (datetime(2024, 12, 14, hour=14, tzinfo=TZ), "14:00 - 14:30", "HR Zoom"),
    (datetime(2024, 12, 14, hour=15, tzinfo=TZ), "15:00 - 18:00", "Noël au Château"),
]

EVENT_MULTI_DAYS = """\
BEGIN:VCALENDAR
VERSION:2.0

BEGIN:VEVENT
SUMMARY:Débroussaillage
DTSTART;TZID=Europe/Paris:20241214T100000
DTEND;TZID=Europe/Paris:20241219T120000
END:VEVENT

END:VCALENDAR
"""
EVENT_MULTI_DAYS_RES = [(datetime(2024, 12, 14, hour=10, tzinfo=TZ), "10:00 - vendredi 12:00", "Débroussaillage")]


@pytest.fixture
def calendar() -> Generator[Calendar]:
    with Calendar(URL) as cls:
        yield cls


def test_forge_header_image(calendar: Calendar) -> None:
    image = calendar.forge_header_image(TODAY)
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
    import thermalprinter.recipes.calendar

    birdthdays_file = tmp_path / "birthdays.lst"
    birdthdays_file.write_text(f"{data}\n")

    with patch.object(thermalprinter.recipes.calendar, "BIRTHDAYS_FILE", birdthdays_file):
        assert calendar.get_birthdays(TODAY) == expected


def test_get_events_on_a_single_day(calendar: Calendar) -> None:
    with patch.object(icalevents.icaldownload.ICalDownload, "data_from_url", return_value=EVENTS_SINGLE_DAY):
        assert calendar.get_events(TODAY) == EVENTS_SINGLE_DAY_RES


def test_get_events_on_multi_days(calendar: Calendar) -> None:
    with patch.object(icalevents.icaldownload.ICalDownload, "data_from_url", return_value=EVENT_MULTI_DAYS):
        assert calendar.get_events(TODAY) == EVENT_MULTI_DAYS_RES


def test_print_data(calendar: Calendar, printer: ThermalPrinter) -> None:
    result: list[str] = []
    out_orig = printer.out

    def out(*args: Any, **kwargs: Any) -> None:
        result.extend(args)
        out_orig(*args, **kwargs)

    birdthdays = [("Alice", 24)]

    with patch.object(printer, "out", out):
        calendar.printer = printer
        calendar.print_data(TODAY, EVENTS_SINGLE_DAY_RES, birdthdays)

    assert result == [
        "C'est l'anniversaire de...",
        "  ... Alice (24) !",
        b"\xd5",
        b"\xcd" * 30,
        b"\xb8",
        b"\xb3",
        " 14:00 - 14:30                ",
        b"\xb3",
        b"\xb3",
        " HR Zoom                      ",
        b"\xb3",
        b"\xc3",
        b"\xc4" * 30,
        b"\xb4",
        b"\xb3",
        " 15:00 - 18:00                ",
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
@patch.object(icalevents.icaldownload.ICalDownload, "data_from_url", return_value=EVENTS_SINGLE_DAY)
@patch("sys.argv", ["print-calendar", URL])
def test_main(mocked_sys_argv: MagicMock) -> None:  # noqa: ARG001
    from thermalprinter.recipes.calendar.__main__ import main

    assert main() == 0


@freeze_time("2024-12-14")
@patch.object(icalevents.icaldownload.ICalDownload, "data_from_url", return_value=EVENTS_SINGLE_DAY)
@patch("sys.argv", ["print-calendar", URL, "--port", "loop://"])
def test_main_with_port(mocked_sys_argv: MagicMock, tmp_path: Path) -> None:  # noqa: ARG001
    from thermalprinter.recipes.calendar.__main__ import main

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


def test_executable(tmp_path: Path) -> None:
    # Create the virtual environment
    venv = tmp_path / "venv"
    python = venv / "bin" / "python"
    check_call(["python", "-m", "venv", str(venv)])

    # Install the extra
    check_call([str(python), "-m", "pip", "install", "-e", ".[calendar]"])

    # Call the new executable
    check_call(["print-calendar", "--help"], cwd=python.parent)


@pytest.mark.parametrize(
    ("now", "start", "end", "expected"),
    [
        # Single-day
        (
            datetime(2024, 12, 14, tzinfo=TZ),
            datetime(2024, 12, 14, hour=8, minute=30, tzinfo=TZ),
            datetime(2024, 12, 14, hour=10, tzinfo=TZ),
            "08:30 - 10:00",
        ),
        # Whole day
        (
            datetime(2024, 12, 14, tzinfo=TZ),
            datetime(2024, 12, 14, hour=8, minute=30, tzinfo=TZ),
            datetime(2024, 12, 14, hour=8, minute=30, tzinfo=TZ),
            WHOLE_DAY,
        ),
        # Multi-days
        (
            datetime(2024, 12, 14, tzinfo=TZ),
            datetime(2024, 12, 14, hour=8, minute=30, tzinfo=TZ),
            datetime(2024, 12, 15, hour=10, tzinfo=TZ),
            "08:30 - demain 10:00",
        ),
        (
            datetime(2024, 12, 14, tzinfo=TZ),
            datetime(2024, 12, 14, hour=8, minute=30, tzinfo=TZ),
            datetime(2024, 12, 16, hour=10, tzinfo=TZ),
            "08:30 - mardi 10:00",
        ),
        (
            datetime(2024, 12, 14, tzinfo=TZ),
            datetime(2024, 12, 13, hour=8, minute=30, tzinfo=TZ),
            datetime(2024, 12, 16, hour=10, tzinfo=TZ),
            WHOLE_DAY,
        ),
        (
            datetime(2024, 12, 14, tzinfo=TZ),
            datetime(2024, 12, 13, hour=8, minute=30, tzinfo=TZ),
            datetime(2024, 12, 14, hour=10, tzinfo=TZ),
            f"{UNTIL} 10:00",
        ),
    ],
)
def test_format_event_date(now: datetime, start: datetime, end: datetime, expected: str) -> None:
    @dataclass
    class D:
        dt: datetime

    event = create_event({"dtstart": D(start), "dtend": D(end)}, True)
    assert format_event_date(now, event) == expected

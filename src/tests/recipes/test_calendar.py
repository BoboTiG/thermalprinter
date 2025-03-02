from __future__ import annotations

from datetime import datetime, timedelta
from subprocess import check_call
from typing import TYPE_CHECKING
from unittest.mock import patch
from zoneinfo import ZoneInfo

import icalendar
import pytest
import responses
from freezegun import freeze_time

from thermalprinter import ThermalPrinter

if TYPE_CHECKING:
    from collections.abc import Generator
    from pathlib import Path
    from typing import Any

    from _typeshed import ReadableBuffer

    from thermalprinter.recipes.calendar import Birthdays

pytest.importorskip("thermalprinter.recipes.calendar", reason="The [calendar] extra dependencies are not installed.")

from thermalprinter.recipes.calendar import (
    BIRTHDAY,
    NICE_DAY,
    TIMEZONE,
    TOMORROW,
    UNTIL,
    WHOLE_DAY,
    Calendar,
    forge_header_image,
    format_event_date,
)

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

BEGIN:VEVENT
SUMMARY:Chandeleur
DTSTART;VALUE=DATE:20241214
DTEND;VALUE=DATE:20241215
RRULE:FREQ=YEARLY;INTERVAL=1;BYMONTH=12
END:VEVENT

END:VCALENDAR
"""
EVENTS_SINGLE_DAY_RES = [
    (datetime(2024, 12, 14, tzinfo=TZ), WHOLE_DAY, "Chandeleur"),
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

BEGIN:VEVENT
SUMMARY:Firenze dans la forêt interdite
DTSTART;TZID=Europe/Paris:20241122T163000
DTEND;TZID=Europe/Paris:20241129T090000
RRULE:FREQ=WEEKLY;INTERVAL=2;BYDAY=SA
END:VEVENT

END:VCALENDAR
"""
EVENT_MULTI_DAYS_RES = [
    (datetime(2024, 12, 7, hour=16, minute=30, tzinfo=TZ), f"{UNTIL} 09:00", "Firenze dans la forêt interdite"),
    (datetime(2024, 12, 14, hour=10, tzinfo=TZ), "10:00", "Débroussaillage"),
]


@pytest.fixture
def calendar() -> Generator[Calendar]:
    with Calendar(URL) as cls:
        yield cls


def test_forge_header_image() -> None:
    image = forge_header_image(TODAY)
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


@responses.activate
def test_get_events_on_a_single_day(calendar: Calendar) -> None:
    responses.add(responses.GET, calendar.url, body=EVENTS_SINGLE_DAY)

    assert calendar.get_events(TODAY) == EVENTS_SINGLE_DAY_RES


@responses.activate
def test_get_events_on_a_single_day__one_day_before(calendar: Calendar) -> None:
    responses.add(responses.GET, calendar.url, body=EVENTS_SINGLE_DAY)

    yesterday = TODAY - timedelta(days=1)
    assert not calendar.get_events(yesterday)


@responses.activate
def test_get_events_on_multi_days(calendar: Calendar) -> None:
    responses.add(responses.GET, calendar.url, body=EVENT_MULTI_DAYS)

    assert calendar.get_events(TODAY) == EVENT_MULTI_DAYS_RES


def test_print_data(calendar: Calendar, printer: ThermalPrinter) -> None:
    result: list[str] = []
    out_orig = printer.out

    def out(data: str, **kwargs: Any) -> None:
        result.append(data)
        if kwargs:
            result.append("    " + ", ".join(f"{k}={v}" for k, v in kwargs.items()))
        out_orig(data, **kwargs)

    birdthdays = [("Alice", 24)]

    with patch.object(printer, "out", out):
        calendar.printer = printer
        calendar.print_data(TODAY, EVENTS_SINGLE_DAY_RES, birdthdays)

    assert result == [
        BIRTHDAY,
        "  ... Alice (24) !",
        "    codepage=CodePage.ISO_8859_1",
        b"\xd5" + b"\xcd" * 30 + b"\xb8",
        "    codepage=CodePage.CP437",
        b"\xb3",
        "    line_feed=False, codepage=CodePage.CP437",
        f" {WHOLE_DAY}             ",
        "    line_feed=False, codepage=CodePage.ISO_8859_1",
        b"\xb3",
        "    codepage=CodePage.CP437",
        b"\xb3",
        "    line_feed=False, codepage=CodePage.CP437",
        " Chandeleur                   ",
        "    line_feed=False, codepage=CodePage.ISO_8859_1",
        b"\xb3",
        "    codepage=CodePage.CP437",
        b"\xc3\xc4\xc4\xc4\xc4\xc4\xc4\xc4\xc4\xc4\xc4\xc4\xc4\xc4\xc4\xc4"
        b"\xc4\xc4\xc4\xc4\xc4\xc4\xc4\xc4\xc4\xc4\xc4\xc4\xc4\xc4\xc4\xb4",
        "    codepage=CodePage.CP437",
        b"\xb3",
        "    line_feed=False, codepage=CodePage.CP437",
        " 14:00 - 14:30                ",
        "    line_feed=False, codepage=CodePage.ISO_8859_1",
        b"\xb3",
        "    codepage=CodePage.CP437",
        b"\xb3",
        "    line_feed=False, codepage=CodePage.CP437",
        " HR Zoom                      ",
        "    line_feed=False, codepage=CodePage.ISO_8859_1",
        b"\xb3",
        "    codepage=CodePage.CP437",
        b"\xc3" + b"\xc4" * 30 + b"\xb4",
        "    codepage=CodePage.CP437",
        b"\xb3",
        "    line_feed=False, codepage=CodePage.CP437",
        " 15:00 - 18:00                ",
        "    line_feed=False, codepage=CodePage.ISO_8859_1",
        b"\xb3",
        "    codepage=CodePage.CP437",
        b"\xb3",
        "    line_feed=False, codepage=CodePage.CP437",
        " Noël au Château              ",
        "    line_feed=False, codepage=CodePage.ISO_8859_1",
        b"\xb3",
        "    codepage=CodePage.CP437",
        b"\xd4" + b"\xcd" * 30 + b"\xbe",
        "    codepage=CodePage.CP437",
        NICE_DAY,
        "    justify=Justify.CENTER, codepage=CodePage.ISO_8859_1",
    ]


@responses.activate
@freeze_time("2024-12-14")
@patch("sys.argv", ["print-calendar", URL])
def test_main() -> None:
    from thermalprinter.recipes.calendar.__main__ import main

    responses.add(responses.GET, URL, body=EVENTS_SINGLE_DAY)

    assert main() == 0


@responses.activate
@freeze_time("2024-12-14")
@patch("sys.argv", ["print-calendar", URL, "--port", "loop://"])
def test_main_with_port(tmp_path: Path) -> None:
    from thermalprinter.recipes.calendar.__main__ import main

    write_orig = ThermalPrinter.write

    def write(self: ThermalPrinter, data: ReadableBuffer, *, should_log: bool = True) -> int | None:
        if should_log:
            return write_orig(self, data, should_log=should_log)

        # We are writing a lot of data: the image, and it make the test serial device queue full.
        # Let's skip it.
        return None

    responses.add(responses.GET, URL, body=EVENTS_SINGLE_DAY)

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
            f"08:30 - {TOMORROW} 10:00",
        ),
        (
            datetime(2024, 12, 14, tzinfo=TZ),
            datetime(2024, 12, 14, hour=8, minute=30, tzinfo=TZ),
            datetime(2024, 12, 16, hour=10, tzinfo=TZ),
            "08:30",
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
    event = icalendar.cal.Event.from_ical(f"""
BEGIN:VEVENT
SUMMARY:Foo
DTSTART;TZID={start.tzinfo}:{start.strftime("%Y%m%dT%H%M%S")}
DTEND;TZID={end.tzinfo}:{end.strftime("%Y%m%dT%H%M%S")}
END:VEVENT
""")
    assert format_event_date(now, event) == expected

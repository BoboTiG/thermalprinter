"""This is part of the Python's module to manage the DP-EH600 thermal printer.
Source: https://github.com/BoboTiG/thermalprinter.
"""

from __future__ import annotations

from contextlib import suppress
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from io import BytesIO
from pathlib import Path
from textwrap import wrap
from typing import TYPE_CHECKING, List, Tuple

from cairosvg import svg2png
from dateutil.relativedelta import relativedelta
from icalevents import icalevents
from PIL import Image

try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo  # type: ignore[no-redef]

if TYPE_CHECKING:
    from types import TracebackType
    from typing import Self

    from thermalprinter import ThermalPrinter

# Might be something you would like to translate
BIRTHDAY = "C'est l'anniversaire de..."  #: Birthdays introduction.
NICE_DAY = "Belle journée :)"  #: Nice words printed at the end.
WHOLE_DAY = "Toute la journée"  #: When an event takes the whole day.
MONTH_NAMES = [
    "Janvier",
    "Février",
    "Mars",
    "Avril",
    "Mai",
    "Juin",
    "Juillet",
    "Août",
    "Septembre",
    "Octobre",
    "Novembre",
    "Décembre",
]  #: Months names.
DAYS_NAMES = [
    "lundi",
    "mardi",
    "mercredi",
    "jeudi",
    "vendredi",
    "samedi",
    "dimanche",
]  #: Days names.
TOMORROW = "demain"  #: Tomorrow.
UNTIL = "jusqu'à"  #: Until.

TIMEZONE = "Europe/Paris"  #: The timezone to display proper hours.

#: File containing birthdays.
BIRTHDAYS_FILE = "~/.birthdays.lst"

#: SVG content of a nice calendar with the current day/month.
AGENDA_MODEL = """\
<svg width="189" height="197">
  <path d="m 172.5,7.519084 h -6.738 c 0.174,-0.5594199 0.354,-1.1188397 0.354,-1.7384122 C 166.116,2.5925802 163.524,0 160.338,0 c -3.186,0 -5.766,2.5925802 -5.766,5.7806718 0,0.6255877 0.168,1.1789923 0.354,1.7384122 h -22.08 C 133.02,6.9596641 133.2,6.4002443 133.2,5.7806718 133.2,2.5925802 130.608,0 127.422,0 c -3.18,0 -5.772,2.5925802 -5.772,5.7806718 0,0.6255877 0.174,1.1789923 0.36,1.7384122 H 99.924 c 0.174,-0.5594199 0.348,-1.1188397 0.348,-1.7384122 C 100.272,2.5925802 97.692,0 94.506,0 91.32,0 88.74,2.5925802 88.74,5.7806718 c 0,0.6255877 0.168,1.1789923 0.348,1.7384122 H 67.002 C 67.176,6.9596641 67.356,6.4002443 67.356,5.7806718 67.356,2.5925802 64.77,0 61.59,0 c -3.186,0 -5.772,2.5925802 -5.772,5.7806718 0,0.6255877 0.168,1.1789923 0.348,1.7384122 H 34.086 C 34.266,6.9596641 34.44,6.4002443 34.44,5.7806718 34.44,2.5925802 31.86,0 28.674,0 c -3.186,0 -5.772,2.5925802 -5.772,5.7806718 0,0.6255877 0.168,1.1789923 0.348,1.7384122 H 16.5 C 7.392,7.519084 0,14.935908 0,24.061069 V 180.45802 C 0,189.58919 7.392,197 16.5,197 H 153.87 L 189,161.78061 V 24.061069 C 189,14.935908 181.608,7.519084 172.5,7.519084 Z m 7.5,150.520026 -1.866,1.87075 h -14.13 c -6.612,0 -12,5.40171 -12,12.03054 v 14.16595 l -1.866,1.87075 H 16.5 c -4.134,0 -7.5,-3.37457 -7.5,-7.51908 V 54.137405 h 171 z" style="stroke-width:6.00763" />
  <text y="40" x="96.25"><tspan x="96.25" text-anchor="middle" style="font-size:30px;font-family:'droid Sans';fill:#ffffff">MONTH</tspan></text>
  <text y="155" x="96.25"><tspan x="96.25" text-anchor="middle" style="font-size:122px;font-family:'Droid Sans'">DAY</tspan></text>
</svg>
"""  # noqa: E501

Birthday = Tuple[str, int]
Birthdays = List[Birthday]
Event = Tuple[datetime, str, str]
Events = List[Event]


@dataclass
class Calendar:
    """Print daily stuff from your calendar, and birthdays as a bonus!

    :param str url: The calendar URL.
    :param thermalprinter.ThermalPrinter | None printer: Optional printer to use.
    """

    url: str
    printer: ThermalPrinter | None = None
    tz: ZoneInfo = field(init=False)

    def __post_init__(self) -> None:
        self.tz = ZoneInfo(TIMEZONE)

    def __enter__(self) -> Self:
        """`with Calender(...) as calendar: ...`"""
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Save stats."""
        if self.printer:
            with self.printer:
                pass

    def start(self) -> None:
        """Where all the magic happens."""
        now = datetime.now(tz=self.tz).replace(hour=0, minute=0, second=0, microsecond=0)
        events = self.get_events(now)
        anniversaries = self.get_birthdays(now)
        self.print_data(now, events, anniversaries)

    def get_birthdays(self, when: datetime) -> Birthdays:
        """Get a list of birthdays."""
        data = ""
        with suppress(FileNotFoundError):
            data = Path(BIRTHDAYS_FILE).expanduser().read_text()

        month_and_day = f"{when.month:02d}-{when.day:02d}"
        birthdays = []

        for line in data.splitlines():
            if line[5:10] == month_and_day:
                born, name = line.split("=", 1)
                born_date = datetime.strptime(born.strip(), "%Y-%m-%d").replace(tzinfo=self.tz)
                years = relativedelta(when, born_date).years
                birthdays.append((name.strip(), years))

        return birthdays

    def get_events(self, when: datetime) -> Events:
        """Retrieve events of the day."""
        events = icalevents.events(url=self.url, start=when, end=when + timedelta(days=1), tzinfo=self.tz)
        return sorted((event.start, format_event_date(when, event), event.summary) for event in events)

    def forge_header_image(self, when: datetime) -> Image:
        """Create the image object containing the nice image with current month, and day."""
        agenda_svg = AGENDA_MODEL.replace("MONTH", MONTH_NAMES[when.month - 1]).replace("DAY", str(when.day))
        agenda_png = svg2png(agenda_svg, background_color="white")
        return Image.open(BytesIO(agenda_png))

    def print_data(self, when: datetime, events: Events, anniversaries: Birthdays) -> None:
        """Just print."""
        if not self.printer:
            return

        from thermalprinter import CodePage, Justify

        printer = self.printer

        def header() -> None:
            """Print the header."""
            printer.codepage(CodePage.ISO_8859_1)
            printer.feed()
            printer.image(self.forge_header_image(when))
            printer.feed()

        def birthdays() -> None:
            """Print anniversaries."""
            printer.feed()
            printer.out(BIRTHDAY)
            for name, years in anniversaries:
                printer.out(f"  ... {name} ({years}) !", codepage=CodePage.ISO_8859_1)
            printer.feed()

        def line(evt: Event, *, first_line: bool = False, last_line: bool = False) -> None:
            """Print an event."""
            _, duration, sumary = evt

            if first_line:
                printer.out(b"\xd5", line_feed=False, codepage=CodePage.CP437)
                printer.out(b"\xcd" * (printer.max_column - 2), line_feed=False, codepage=CodePage.CP437)
                printer.out(b"\xb8", codepage=CodePage.CP437)

            printer.out(b"\xb3", line_feed=False, codepage=CodePage.CP437)
            printer.out(
                " {0: <{1}} ".format(duration, printer.max_column - 4),
                line_feed=False,
                codepage=CodePage.ISO_8859_1,
            )
            printer.out(b"\xb3", codepage=CodePage.CP437)

            for line_ in wrap(sumary, printer.max_column - 4):
                printer.out(b"\xb3", line_feed=False, codepage=CodePage.CP437)
                printer.out(
                    " {0: <{1}} ".format(line_, printer.max_column - 4),
                    line_feed=False,
                    codepage=CodePage.ISO_8859_1,
                )
                printer.out(b"\xb3", codepage=CodePage.CP437)

            left, middle, right = (b"\xd4", b"\xcd", b"\xbe") if last_line else (b"\xc3", b"\xc4", b"\xb4")
            printer.out(left, line_feed=False, codepage=CodePage.CP437)
            printer.out(middle * (printer.max_column - 2), line_feed=False, codepage=CodePage.CP437)
            printer.out(right, codepage=CodePage.CP437)

        def footer() -> None:
            """Printed the footer."""
            printer.feed()
            printer.out(NICE_DAY, justify=Justify.CENTER, codepage=CodePage.ISO_8859_1)
            printer.feed(4)

        header()
        if anniversaries:
            birthdays()
        if events:
            first, last = events[0], events[-1]
            for event in events:
                line(event, first_line=event is first, last_line=event is last)
        footer()


def format_event_date(now: datetime, event: icalevents.Event) -> str:
    """Given the current date, and an iCal event, return the formated event's start, and end.

    :param: datetime now: the current date to compare event's dates to.
    :param: icalevents.Event event: the iCal event.
    :rtype: str
    :return: the formated event duration.
    """
    delta = event.end - event.start

    # A single-day event
    if not delta.days:
        if event.start == event.end:
            return WHOLE_DAY
        return f"{event.start.strftime('%H:%M')} - {event.end.strftime('%H:%M')}"

    # A multi-days event

    if event.start < now < event.end and event.end.strftime("%Y-%m-%d") != now.strftime("%Y-%m-%d"):
        return WHOLE_DAY

    delta = event.end - now
    if delta.days == 1:
        return f"{event.start.strftime('%H:%M')} - {TOMORROW} {event.end.strftime('%H:%M')}"

    if delta.days < 1:
        return f"{UNTIL} {event.end.strftime('%H:%M')}"

    return (
        f"{event.start.strftime('%H:%M')} - {DAYS_NAMES[int(event.end.strftime('%w'))]} {event.end.strftime('%H:%M')}"
    )

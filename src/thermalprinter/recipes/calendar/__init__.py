"""This is part of the Python's module to manage the DP-EH600 thermal printer.
Source: https://github.com/BoboTiG/thermalprinter.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from io import BytesIO
from pathlib import Path
from textwrap import wrap
from typing import TYPE_CHECKING

from cairosvg import svg2png
from dateutil.relativedelta import relativedelta
from icalevents import icalevents
from PIL import Image
from pytz import utc

if TYPE_CHECKING:
    from types import TracebackType
    from typing import Self

    from thermalprinter import ThermalPrinter

# Might be something you would like to translate
BIRTHDAY = "C'est l'anniversaire de..."  #: Birthdays introduction.
NICE_DAY = "Belle journée :)"  #:Printed at the end.
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
]  #: Months transaltions

#: File containing birthdays.
BIRTHDAYS_FILE = "~/.birthdays.lst"

#: SVG content of a nice calendar with the current day/month.
AGENDA_MODEL = """\
<svg>
  <path transform="matrix(6,0,0,6,0,0)" d="m 29.375,1.25 -1.123,0 C 28.281,1.157 28.311,1.064 28.311,0.961 28.311,0.431 27.879,0 27.348,0 c -0.531,0 -0.961,0.431 -0.961,0.961 0,0.104 0.028,0.196 0.059,0.289 l -3.68,0 C 22.795,1.157 22.825,1.064 22.825,0.961 22.825,0.431 22.393,0 21.862,0 21.332,0 20.9,0.431 20.9,0.961 c 0,0.104 0.029,0.196 0.06,0.289 l -3.681,0 C 17.308,1.157 17.337,1.064 17.337,0.961 17.337,0.431 16.907,0 16.376,0 c -0.531,0 -0.961,0.431 -0.961,0.961 0,0.104 0.028,0.196 0.058,0.289 l -3.681,0 C 11.821,1.157 11.851,1.064 11.851,0.961 11.851,0.431 11.42,0 10.89,0 10.359,0 9.928,0.431 9.928,0.961 c 0,0.104 0.028,0.196 0.058,0.289 l -3.68,0 C 6.336,1.157 6.365,1.064 6.365,0.961 6.365,0.431 5.935,0 5.404,0 4.873,0 4.442,0.431 4.442,0.961 4.442,1.065 4.47,1.157 4.5,1.25 l -1.125,0 C 1.857,1.25 0.625,2.483 0.625,4 l 0,26 c 0,1.518 1.232,2.75 2.75,2.75 l 22.895,0 5.855,-5.855 0,-22.895 c 0,-1.517 -1.232,-2.75 -2.75,-2.75 z m 1.25,25.023 -0.311,0.311 -2.355,0 c -1.102,0 -2,0.898 -2,2 l 0,2.355 -0.311,0.311 -22.273,0 c -0.689,0 -1.25,-0.561 -1.25,-1.25 l 0,-21 28.5,0 z" />
  <text y="40" transform="translate(100)">
    <tspan x="0" text-anchor="middle" style="fill:#ffffff;font-size:30px;font-family:droid Sans">MONTH</tspan>
  </text>
  <text y="155" transform="translate(100)">
    <tspan x="0" text-anchor="middle" style="font-size:122px;font-family:Droid Sans">DAY</tspan>
  </text>
</svg>
"""  # noqa: E501
AGENDA_MODEL_SIZE = (189, 197)

Birthday = tuple[str, int]
Birthdays = list[Birthday]
Event = tuple[str, str, str]
Events = list[Event]


@dataclass
class Calendar:
    """Print daily stuff from your calendar.

    :param str url: The calendar URL.
    :param thermalprinter.ThermalPrinter | None printer: Optional printer to use.
    """

    url: str
    printer: ThermalPrinter | None = None
    now: datetime = field(init=False)

    def __post_init__(self) -> None:
        self.now = utc.localize(datetime.now())

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
        events = self.get_events()
        anniversaries = self.get_birthdays()
        self.print_data(events, anniversaries)

    def get_birthdays(self) -> Birthdays:
        """Get a list of birthdays."""
        month_and_day = f"{self.now.month:02d}-{self.now.day:02d}"

        data = Path(BIRTHDAYS_FILE).expanduser().read_text()
        birthdays = []

        for line in data.splitlines():
            if line[5:10] == month_and_day:
                born, name = line.split("=", 1)
                born_date = utc.localize(datetime.strptime(born.strip(), "%Y-%m-%d"))
                years = relativedelta(self.now, born_date).years
                birthdays.append((name.strip(), years))

        return birthdays

    def get_events(self) -> Events:
        """Retrieve events of the day."""
        events = icalevents.events(url=self.url, end=self.now + timedelta(days=1))
        return sorted(
            {(event.start.strftime("%H:%M"), event.end.strftime("%H:%M"), event.summary) for event in events},
            key=lambda x: x[0],
        )

    def forge_header_image(self) -> Image:
        """Create the image object containing the nice image with current month, and day."""
        agenda_svg = AGENDA_MODEL.replace("MONTH", MONTH_NAMES[self.now.month - 1]).replace("DAY", str(self.now.day))
        agenda_png = svg2png(agenda_svg, parent_width=AGENDA_MODEL_SIZE[0], parent_height=AGENDA_MODEL_SIZE[1])
        return Image.open(BytesIO(agenda_png))

    def print_data(self, events: Events, anniversaries: Birthdays) -> None:
        """Just print."""
        if not self.printer:
            return

        from thermalprinter import CodePage, Justify

        printer = self.printer

        def header() -> None:
            """Print the header."""
            printer.codepage(CodePage.ISO_8859_1)
            printer.feed()
            printer.image(self.forge_header_image())
            printer.feed()

        def birthdays() -> None:
            """Print anniversaries."""
            printer.out(BIRTHDAY)
            for name, years in anniversaries:
                printer.out(f"  ... {name} ({years}) !", codepage=CodePage.ISO_8859_1)
            printer.feed()

        def line(evt: Event, first_line: bool = False, last_line: bool = False) -> None:
            """Print an event."""
            start, end, sumary = evt
            hour = WHOLE_DAY if start == end else f"{start} - {end}"

            if first_line:
                printer.out(b"\xd5", line_feed=False, codepage=CodePage.CP437)
                printer.out(b"\xcd" * (printer.max_column - 2), line_feed=False, codepage=CodePage.CP437)
                printer.out(b"\xb8", codepage=CodePage.CP437)

            printer.out(b"\xb3", line_feed=False, codepage=CodePage.CP437)
            printer.out(
                " {0: <{1}} ".format(hour, printer.max_column - 4),
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

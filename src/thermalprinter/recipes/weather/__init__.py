"""This is part of the Python's module to manage the DP-EH600 thermal printer.
Source: https://github.com/BoboTiG/thermalprinter.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from logging import getLogger
from pathlib import Path
from typing import TYPE_CHECKING

import requests

if TYPE_CHECKING:
    from types import TracebackType
    from typing import Any, Self

    from thermalprinter import ThermalPrinter

# Might be something you would like to translate
TITLE = "Météo"  #: Title.
SAINT_OF_THE_DAY = "Fête du jour : {}"  #: Prefix before the saint of the day.
UNKNOWN = "Inconnu(e)"  #: When the day does not meet a saint of the day.
NORTH = "N"  #: The North cord point abbreviation.
EAST = "E"  #: The East cord point abbreviation.
SOUTH = "S"  #: The South cord point abbreviation.
WEST = "O"  #: The West cord point abbreviation.

#: OpenWeatherMap API URL
URL = "https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=metric&appid={appid}"
SAINTS_FILE = "./saints.lst"  #: File containing calendar saints.

# Sync with https://openweathermap.org/weather-conditions
DESCRIPTIONS = {
    # Group 2xx: Thunderstorm
    "thunderstorm": "Orage",
    "thunderstorm with light rain": "Orage avec fine pluie",
    "thunderstorm with rain": "Orage avec pluie",
    "thunderstorm with heavy rain": "Orage avec fortes pluies",
    "light thunderstorm": "Léger orage",
    "heavy thunderstorm": "Fort orage",
    "ragged thunderstorm": "Orage en dent de scie",
    "thunderstorm with light drizzle": "Orage avec légère bruine",
    "thunderstorm with drizzle": "Orage avec bruine",
    "thunderstorm with heavy drizzle": "orage avec forte bruine",
    # Group 3xx: Drizzle
    "light intensity drizzle": "Légère bruine",
    "drizzle": "Bruine",
    "heavy intensity drizzle": "Forte bruine",
    "light intensity drizzle rain": "Légère bruine avec pluie",
    "drizzle rain": "Bruine pluvieuse",
    "heavy intensity drizzle rain": "Forte bruine pluvieuse",
    "shower rain and drizzle": "Averse et bruine",
    "heavy shower rain and drizzle": "Forte averse et bruine",
    "shower drizzle": "Averse et bruine",
    # Group 5xx: Rain
    "light rain": "Pluie légère",
    "moderate rain": "Pluie modérée",
    "heavy intensity rain": "Pluie très intense",
    "very heavy rain": "Pluie très forte",
    "extreme rain": "Pluie extrême",
    "freezing rain": "Pluie vergalçante",
    "light intensity shower rain": "Pluie légère",
    "shower rain": "Averse",
    "heavy intensity shower rain": "Forte averse",
    "ragged shower rain": "Pluie en dent de scie",
    # Group 6xx: Snow
    "light snow": "Neige légère",
    "snow": "Neige",
    "heavy snow": "Forte neige",
    "sleet": "Grésil",
    "light shower sleet": "Grésil léger",
    "shower sleet": "Averse de grésil",
    "light rain and snow": "Pluie fine et neige",
    "rain and snow": "Pluie et neige",
    "light shower snow": "Pluie légère et neige",
    "shower snow": "Pluie de neige",
    "heavy shower snow": "Tempête de neige",
    # Group 7xx: Atmosphere
    "mist": "Brume",
    "smoke": "Fumée",
    "haze": "Brume",
    "sand/dust whirls": "Tourbillons de sable/poussière",
    "fog": "Brouillard",
    "sand": "Sable",
    "dust": "Poussière",
    "volcanic ash": "Cendres volcaniques",
    "squalls": "Bourrasques",
    "tornado": "Tornade",
    # Group 800: Clear
    "clear sky": "Ciel dégagé",
    # Group 80x: Clouds
    "few clouds": "Quelques nuages",
    "scattered clouds": "Nuages épars",
    "broken clouds": "Nuages fragmentés",
    "overcast clouds": "Nuages couverts",
}  #: :meta hide-value:

# https://github.com/schachmat/wego/blob/2.3/frontends/ascii-art-table.go
ASCII_ARTS = {
    # Group 2xx: Thunderstorm
    "thunderstorm": """\
 _`/"".-.
   \\_(   ).    {description}
   /(___(__)   {temp_min} - {temp_max} °C
    ⚡ʻ ʻ⚡ʻ ʻ   & {wind} km/h
    ʻ ʻ ʻ ʻ    {precipitations} mm/h - {humidity}%
    """,
    "heavy thunderstorm": """\
     .-.
    (   ).     {description}
   (___(__)    {temp_min} - {temp_max} °C
  ‚ʻ⚡ʻ‚⚡‚ʻ     & {wind} km/h
  ‚ʻ‚ʻ⚡ʻ‚ʻ     {precipitations} mm/h - {humidity}%
    """,
    # Group 3xx: Drizzle
    # Group 5xx: Rain
    "light rain": """\
     .-.
    (   ).     {description}
   (___(__)    {temp_min} - {temp_max} °C
    ʻ ʻ ʻ ʻ    & {wind} km/h
   ʻ ʻ ʻ ʻ     {precipitations} mm/h - {humidity}%
    """,
    "shower rain": """\
 _`/"".-.
   \\_(   ).    {description}
   /(___(__)   {temp_min} - {temp_max} °C
     ʻ ʻ ʻ ʻ   & {wind} km/h
    ʻ ʻ ʻ ʻ    {precipitations} mm/h - {humidity}%
    """,
    "very heavy rain": """\
     .-.
    (   ).     {description}
   (___(__)    {temp_min} - {temp_max} °C
  ‚ʻ‚ʻ‚ʻ‚ʻ     & {wind} km/h
  ‚ʻ‚ʻ‚ʻ‚ʻ     {precipitations} mm/h - {humidity}%
    """,
    "heavy intensity shower rain": """\
 _`/"".-.
   \\_(   ).    {description}
   /(___(__)   {temp_min} - {temp_max} °C
   ‚ʻ‚ʻ‚ʻ‚ʻ    & {wind} km/h
   ‚ʻ‚ʻ‚ʻ‚ʻ    {precipitations} mm/h - {humidity}%
    """,
    "freezing rain": """\
     .-.
    (   ).     {description}
   (___(__)    {temp_min} - {temp_max} °C
    ʻ * ʻ *    & {wind} km/h
   * ʻ * ʻ     {precipitations} mm/h - {humidity}%
    """,
    # Group 6xx: Snow
    "snow": """\
     .-.
    (   ).     {description}
   (___(__)    {temp_min} - {temp_max} °C
    *  *  *    & {wind} km/h
   *  *  *     {precipitations} mm/h - {humidity}%
    """,
    "heavy snow": """\
     .-.
    (   ).     {description}
   (___(__)    {temp_min} - {temp_max} °C
   * * * *     & {wind} km/h
  * * * *      {precipitations} mm/h - {humidity}%
    """,
    "heavy shower snow": """\
 _`/"".-.
   \\_(   ).    {description}
   /(___(__)   {temp_min} - {temp_max} °C
    * * * *    & {wind} km/h
   * * * *     {precipitations} mm/h - {humidity}%
    """,
    "shower sleet": """\
 _`/"".-.
   \\_(   ).    {description}
   /(___(__)   {temp_min} - {temp_max} °C
     ʻ * ʻ *   & {wind} km/h
    * ʻ * ʻ    {precipitations} mm/h - {humidity}%
    """,
    "shower snow": """\
 _`/"".-.
   \\_(   ).    {description}
   /(___(__)   {temp_min} - {temp_max} °C
     *  *  *   & {wind} km/h
    *  *  *    {precipitations} mm/h - {humidity}%
    """,
    # Group 7xx: Atmosphere
    "fog": """\

 _ - _ - _ -   {description}
  _ - _ - _    {temp_min} - {temp_max} °C
 _ - _ - _ -   & {wind} km/h
               {precipitations} mm/h - {humidity}%
    """,
    "tornado": """\
    (    )
     (  )     {description}
    ( )       {temp_min} - {temp_max} °C
     ()       & {wind} km/h
     .        {precipitations} mm/h - {humidity}%
    """,
    "squalls": """\

               {description}
   \\ \\ \\ \\     {temp_min} - {temp_max} °C
     \\ \\ \\ \\   & {wind} km/h
               {precipitations} mm/h - {humidity}%
    """,
    # Group 800: Clear
    "clear sky": """\
    \\ . /
   - .-. -     {description}
  ‒ (   ) ‒    {temp_min} - {temp_max} °C
   . `-᾿ .     & {wind} km/h
    / ' \\      {precipitations} mm/h - {humidity}%
    """,
    # Group 80x: Clouds
    "broken clouds": """\

     .--.      {description}
  .-(    ).    {temp_min} - {temp_max} °C
 (___.__)__)   & {wind} km/h
               {precipitations} mm/h - {humidity}%
    """,
    "few clouds": """\
   \\__/
 __/  .-.      {description}
   \\_(   ).    {temp_min} - {temp_max} °C
   /(___(__)   & {wind} km/h
               {precipitations} mm/h - {humidity}%
    """,
    "overcast clouds": """\

     .--.      {description}
  .-(    ).    {temp_min} - {temp_max} °C
 (___.__)__)   & {wind} km/h
               {precipitations} mm/h - {humidity}%
    """,
}  #: :meta hide-value:
# ASCII art aliases
# Group 2xx: Thunderstorm
ASCII_ARTS["thunderstorm with light rain"] = ASCII_ARTS["thunderstorm"]
ASCII_ARTS["thunderstorm with rain"] = ASCII_ARTS["thunderstorm"]
ASCII_ARTS["thunderstorm with heavy rain"] = ASCII_ARTS["heavy thunderstorm"]
ASCII_ARTS["light thunderstorm"] = ASCII_ARTS["thunderstorm"]
ASCII_ARTS["ragged thunderstorm"] = ASCII_ARTS["thunderstorm"]
ASCII_ARTS["thunderstorm with light drizzle"] = ASCII_ARTS["thunderstorm"]
ASCII_ARTS["thunderstorm with drizzle"] = ASCII_ARTS["thunderstorm"]
ASCII_ARTS["thunderstorm with heavy drizzle"] = ASCII_ARTS["heavy thunderstorm"]
# Group 3xx: Drizzle
ASCII_ARTS["light intensity drizzle"] = ASCII_ARTS["light rain"]
ASCII_ARTS["drizzle"] = ASCII_ARTS["light rain"]
ASCII_ARTS["heavy intensity drizzle"] = ASCII_ARTS["heavy intensity shower rain"]
ASCII_ARTS["light intensity drizzle rain"] = ASCII_ARTS["light rain"]
ASCII_ARTS["drizzle rain"] = ASCII_ARTS["light rain"]
ASCII_ARTS["heavy intensity drizzle rain"] = ASCII_ARTS["very heavy rain"]
ASCII_ARTS["shower rain and drizzle"] = ASCII_ARTS["shower rain"]
ASCII_ARTS["heavy shower rain and drizzle"] = ASCII_ARTS["heavy intensity shower rain"]
ASCII_ARTS["shower drizzle"] = ASCII_ARTS["shower rain"]
# Group 5xx: Rain
ASCII_ARTS["moderate rain"] = ASCII_ARTS["shower rain"]
ASCII_ARTS["heavy intensity rain"] = ASCII_ARTS["very heavy rain"]
ASCII_ARTS["extreme rain"] = ASCII_ARTS["very heavy rain"]
ASCII_ARTS["light intensity shower rain"] = ASCII_ARTS["shower rain"]
ASCII_ARTS["ragged shower rain"] = ASCII_ARTS["shower rain"]
# Group 6xx: Snow
ASCII_ARTS["light snow"] = ASCII_ARTS["snow"]
ASCII_ARTS["sleet"] = ASCII_ARTS["snow"]
ASCII_ARTS["light shower sleet"] = ASCII_ARTS["shower sleet"]
ASCII_ARTS["light rain and snow"] = ASCII_ARTS["shower sleet"]
ASCII_ARTS["rain and snow"] = ASCII_ARTS["shower sleet"]
ASCII_ARTS["light shower snow"] = ASCII_ARTS["shower snow"]
# Group 7xx: Atmosphere
ASCII_ARTS["mist"] = ASCII_ARTS["fog"]
ASCII_ARTS["smoke"] = ASCII_ARTS["fog"]
ASCII_ARTS["haze"] = ASCII_ARTS["fog"]
ASCII_ARTS["sand/dust whirls"] = ASCII_ARTS["fog"]
ASCII_ARTS["sand"] = ASCII_ARTS["fog"]
ASCII_ARTS["dust"] = ASCII_ARTS["fog"]
ASCII_ARTS["volcanic ash"] = ASCII_ARTS["fog"]
# Group 80x: Clouds
ASCII_ARTS["scattered clouds"] = ASCII_ARTS["few clouds"]

log = getLogger(__name__)


@dataclass
class Weather:
    """Print the weather of the day using the data from OpenWeatherMap.

    :param float lat: Location latitude.
    :param float lon: Location longitude.
    :param str appid: OpenWeatherMap appid.
    :param thermalprinter.ThermalPrinter | None printer: Optional printer to use.
    """

    lat: float
    lon: float
    appid: str
    printer: ThermalPrinter | None = None

    def __enter__(self) -> Self:
        """`with Weather(...) as weather: ...`"""
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
        today = self.get_today_data()
        data = self.forge_data(today)
        self.print_data(data)

    def get_the_saint_of_the_day(self) -> str:
        """Guess the saint of the day."""
        today = datetime.now(tz=UTC).strftime("%d/%m")
        lines = (Path(__file__).parent / SAINTS_FILE).read_text().splitlines()
        return next((line.split(";", 1)[1].strip() for line in lines if line.startswith(today)), UNKNOWN)

    def get_today_data(self) -> dict[str, Any]:
        """Retreive today weather metrics."""
        url = URL.format(lat=self.lat, lon=self.lon, appid=self.appid)
        with requests.get(url, timeout=15) as req:
            data = req.json()
        log.info("Got weather data: %s", data)
        return data["daily"][0]

    def forge_data(self, today: dict[str, Any]) -> dict[str, Any]:
        """Craft the dict with only required metrics."""
        data = {
            "ascii": ASCII_ARTS[today["weather"][0]["description"]].rstrip(),
            "humidity": today["humidity"],
            "description": DESCRIPTIONS[today["weather"][0]["description"]],
            "precipitations": int(today.get("rain", 0)),
            "temp_max": int(today["temp"]["max"]),
            "temp_min": int(today["temp"]["min"]),
            "wind": mps_to_kmph(today["wind_speed"]),
            "wind_dir": wind_dir(today["wind_deg"]),
        }
        log.debug("Crafted data: %s", data)
        return data

    def print_data(self, data: dict[str, Any]) -> None:
        """Just print."""
        if not self.printer:
            return

        from thermalprinter import CodePage, Justify, Size

        printer = self.printer

        printer.codepage(CodePage.ISO_8859_1)
        printer.feed()
        printer.out(TITLE, bold=True, size=Size.LARGE)
        printer.out(datetime.now().strftime("%Y-%m-%d"))  # noqa: DTZ005
        printer.feed()

        lines = data.pop("ascii").splitlines()
        printer.out(lines[0])

        # State
        printer.out(lines[1].format(**data))

        # Temperature
        printer.out(lines[2].format(**data))

        # Wind
        part1, part2 = lines[3].split("&", 1)
        printer.out(part1, line_feed=False)
        if isinstance(data["wind_dir"], bytes):
            printer.out(data["wind_dir"], line_feed=False, codepage=CodePage.THAI2)
        else:
            printer.out(data["wind_dir"], line_feed=False)
        printer.out(part2.format(**data))

        # Precipitations
        printer.out(lines[4].format(**data))

        # Saint of the day
        printer.feed()
        printer.out(
            SAINT_OF_THE_DAY.format(self.get_the_saint_of_the_day()),
            justify=Justify.CENTER,
            codepage=CodePage.ISO_8859_1,
        )

        printer.feed(3)


def mps_to_kmph(mps: float) -> int:
    """Convert the wind unity from m/sec to km/h.

    :param float mps: The input value in m/sec.
    :rtype: int
    :return: The converted value to km/h.
    """
    return int(mps * 3.6)


def wind_dir(angle: float) -> bytes | str:
    """Get the corresponding wind direction arrow, or the cord point abbreviation.

    :param float angle: The wind angle.
    :rtype: bytes | str
    :return:
        The cord point abbreviation. Either bytes for arrows, or plain string.

        .. note::
            Bytes values are :const:`thermalprinter.constants.CodePage` ``THAI2`` characters.
    """
    directions: list[bytes | str] = [
        # North
        b"\x8d",
        # North-East
        f"{NORTH}{EAST}",
        f"{NORTH}{EAST}",
        # East
        b"\x8e",
        b"\x8e",
        # South-East
        f"{SOUTH}{EAST}",
        f"{SOUTH}{EAST}",
        # South
        b"\x8f",
        b"\x8f",
        # South-West
        f"{SOUTH}{WEST}",
        f"{SOUTH}{WEST}",
        # West
        b"\x8c",
        b"\x8c",
        # North-West
        f"{NORTH}{WEST}",
        f"{NORTH}{WEST}",
        # North
        b"\x8d",
    ]
    return directions[int(angle / 22.5)]

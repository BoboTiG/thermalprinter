from __future__ import annotations

from copy import deepcopy
from subprocess import check_call
from typing import TYPE_CHECKING
from unittest.mock import patch

import pytest

pytest.importorskip("thermalprinter.recipes.weather", reason="The [weather] extra dependencies are not installed.")

import responses  # noqa: E402
from freezegun import freeze_time  # noqa: E402

from thermalprinter.constants import CodePage, Justify, Size  # noqa: E402
from thermalprinter.recipes.weather import DESCRIPTIONS, URL, Weather  # noqa: E402

if TYPE_CHECKING:
    from collections.abc import Generator
    from pathlib import Path
    from typing import Any

    from thermalprinter import ThermalPrinter

LAT = 42.0
LON = 0.42
APPID = "<APPID>"
RESPONSE = {
    "lat": 42.0,
    "lon": 0.42,
    "timezone": "Europe/Paris",
    "timezone_offset": 3600,
    "current": {},
    "minutely": [],
    "hourly": [],
    "daily": [
        {
            "dt": 1734087600,
            "sunrise": 1734074790,
            "sunset": 1734106633,
            "moonrise": 1734099840,
            "moonset": 1734067140,
            "moon_phase": 0.43,
            "temp": {"day": 9.23, "min": 3.72, "max": 10.63, "night": 4.26, "eve": 6.76, "morn": 6.96},
            "feels_like": {"day": 6.86, "night": 2.72, "eve": 4.67, "morn": 4.78},
            "pressure": 1023,
            "humidity": 75,
            "dew_point": 4.88,
            "wind_speed": 5.25,
            "wind_deg": 152,
            "wind_gust": 9.83,
            "weather": [{"id": 804, "main": "Clouds", "description": "overcast clouds", "icon": "04d"}],
            "clouds": 100,
            "pop": 0,
            "rain": 6.53,
            "uvi": 0.9,
        }
    ],
}
TODAY = RESPONSE["daily"][0]  # type: ignore[index]


@pytest.fixture
def weather() -> Generator[Weather]:
    with freeze_time("2024-12-13"), Weather(LAT, LON, APPID) as cls:
        yield cls


def test_forge_data(weather: Weather) -> None:
    assert weather.forge_data(TODAY) == {
        "ascii": (
            "\n"
            "     .--.      {description}\n"
            "  .-(    ).    {temp_min} - {temp_max} °C\n"
            " (___.__)__)   & {wind} km/h\n"
            "               {precipitations} mm/h - {humidity}%"
        ),
        "description": "Nuages couverts",
        "humidity": 75,
        "precipitations": 6,
        "temp_max": 10,
        "temp_min": 3,
        "wind": 18,
        "wind_dir": "SE",
    }


@pytest.mark.parametrize("description", list(DESCRIPTIONS.keys()))
def test_print_data_fuzzy(description: str, weather: Weather, printer: ThermalPrinter) -> None:
    today = deepcopy(TODAY)
    today["weather"][0]["description"] = description
    data = weather.forge_data(today)

    weather.printer = printer
    weather.print_data(data)


def test_print_data_wind_dir_bytes(weather: Weather, printer: ThermalPrinter) -> None:
    today = deepcopy(TODAY)
    today["wind_deg"] = 0.0
    data = weather.forge_data(today)

    weather.printer = printer
    weather.print_data(data)


def test_line_out(weather: Weather, printer: ThermalPrinter) -> None:
    today = deepcopy(TODAY)
    today["wind_deg"] = 0.0
    today["weather"][0]["description"] = "clear sky"
    data = weather.forge_data(today)

    instructions: list[Any] = []
    orig_codepage = printer.codepage
    orig_feed = printer.feed
    orig_out = printer.out

    def codepage(codepage: CodePage = CodePage.CP437) -> None:
        instructions.append(codepage)
        orig_codepage(codepage)

    def feed(number: int = 1) -> None:
        instructions.extend([r"\n"] * number)
        orig_feed(number)

    def out(data: Any, line_feed: bool = True, **kwargs: Any) -> None:
        instructions.append((data, line_feed, kwargs))
        orig_out(data, line_feed=line_feed, **kwargs)

    with patch.object(printer, "codepage", codepage), patch.object(printer, "feed", feed):  # noqa: SIM117
        with patch.object(printer, "out", out):
            weather.printer = printer
            weather.print_data(data)

    expected = [
        CodePage.ISO_8859_1,
        r"\n",
        ("Météo", True, {"bold": True, "size": Size.LARGE}),
        ("2024-12-13", True, {}),
        r"\n",
        ("    \\ . /", True, {}),
        ("   - .-. -     Ciel dégagé", True, {}),
        ("  ", False, {}),
        CodePage.CP863,
        (b"\xc4", False, {}),
        CodePage.ISO_8859_1,
        (" (   ) ", False, {}),
        CodePage.CP863,
        (b"\xc4", False, {}),
        CodePage.ISO_8859_1,
        ("    3 - 10 °C", True, {}),
        ("   . `-", False, {}),
        CodePage.ISO_8859_7,
        (b"\xa2", False, {}),
        CodePage.ISO_8859_1,
        (" .     ", False, {}),
        CodePage.THAI2,
        (b"\x8d", False, {}),
        CodePage.ISO_8859_1,
        (" 18 km/h", True, {}),
        ("    / ' \\      6 mm/h - 75%", True, {}),
        CodePage.ISO_8859_1,
        r"\n",
        ("Fête du jour : Lucie", True, {"justify": Justify.CENTER}),
        r"\n",
        r"\n",
        r"\n",
    ]
    assert instructions == expected


@responses.activate
def test_main() -> None:
    from thermalprinter.recipes.weather.__main__ import main

    url = URL.format(lat=LAT, lon=LON, appid=APPID)
    responses.add(responses.GET, url, json=RESPONSE)

    with patch("sys.argv", ["print-weather", str(LAT), str(LON), APPID]):
        assert main() == 0


@responses.activate
def test_main_with_port(tmp_path: Path) -> None:
    from thermalprinter.recipes.weather.__main__ import main

    url = URL.format(lat=LAT, lon=LON, appid=APPID)
    responses.add(responses.GET, url, json=RESPONSE)

    with patch("thermalprinter.constants.STATS_FILE", f"{tmp_path}/stats.json"):  # noqa: SIM117
        with patch("sys.argv", ["print-weather", str(LAT), str(LON), APPID, "--port", "loop://"]):
            assert main() == 0


def test_executable(tmp_path: Path) -> None:
    # Create the virtual environment
    venv = tmp_path / "venv"
    python = venv / "bin" / "python"
    check_call(["python", "-m", "venv", str(venv)])

    # Install the extra
    check_call([str(python), "-m", "pip", "install", "-e", ".[weather]"])

    # Call the new executable
    check_call(["print-weather", "--help"], cwd=python.parent)

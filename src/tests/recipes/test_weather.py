from __future__ import annotations

from copy import deepcopy
from typing import TYPE_CHECKING
from unittest.mock import patch

import pytest
import responses
from freezegun import freeze_time

from thermalprinter.recipes.weather import URL, Weather
from thermalprinter.recipes.weather.__main__ import main

if TYPE_CHECKING:
    from pathlib import Path
    from typing import Any, Generator

    from thermalprinter import ThermalPrinter

LAT = 42.0
LON = 0.42
APPID = "<APP_ID>"
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
        },
        {
            "dt": 1734174000,
            "sunrise": 1734161236,
            "sunset": 1734193043,
            "moonrise": 1734188760,
            "moonset": 1734158460,
            "moon_phase": 0.47,
            "temp": {"day": 8.23, "min": 4.13, "max": 8.23, "night": 5.28, "eve": 5.37, "morn": 6.01},
            "feels_like": {"day": 5.26, "night": 5.28, "eve": 3.37, "morn": 3.18},
            "pressure": 1028,
            "humidity": 79,
            "dew_point": 4.76,
            "wind_speed": 5.47,
            "wind_deg": 294,
            "wind_gust": 11.06,
            "weather": [{"id": 502, "main": "Rain", "description": "heavy intensity rain", "icon": "10d"}],
            "clouds": 98,
            "pop": 1,
            "rain": 6.53,
            "uvi": 0.68,
        },
        {
            "dt": 1734260400,
            "sunrise": 1734247680,
            "sunset": 1734279455,
            "moonrise": 1734278460,
            "moonset": 1734249360,
            "moon_phase": 0.5,
            "temp": {"day": 7.04, "min": 3.13, "max": 8.6, "night": 4.92, "eve": 5.3, "morn": 3.61},
            "feels_like": {"day": 4.81, "night": 4.92, "eve": 4.01, "morn": 1.99},
            "pressure": 1037,
            "humidity": 74,
            "dew_point": 2.64,
            "wind_speed": 3.58,
            "wind_deg": 340,
            "wind_gust": 5.08,
            "weather": [{"id": 801, "main": "Clouds", "description": "few clouds", "icon": "02d"}],
            "clouds": 19,
            "pop": 0,
            "uvi": 1.24,
        },
        {
            "dt": 1734346800,
            "sunrise": 1734334122,
            "sunset": 1734365869,
            "moonrise": 1734368820,
            "moonset": 1734339540,
            "moon_phase": 0.54,
            "temp": {"day": 8.67, "min": 4.16, "max": 10.98, "night": 6.57, "eve": 7.54, "morn": 5.22},
            "feels_like": {"day": 7.83, "night": 4.63, "eve": 6.51, "morn": 4.24},
            "pressure": 1037,
            "humidity": 75,
            "dew_point": 4.43,
            "wind_speed": 2.99,
            "wind_deg": 115,
            "wind_gust": 4.76,
            "weather": [{"id": 800, "main": "Clear", "description": "clear sky", "icon": "01d"}],
            "clouds": 0,
            "pop": 0,
            "uvi": 1.31,
        },
        {
            "dt": 1734433200,
            "sunrise": 1734420562,
            "sunset": 1734452287,
            "moonrise": 1734459600,
            "moonset": 1734428820,
            "moon_phase": 0.57,
            "temp": {"day": 10.03, "min": 4.44, "max": 10.03, "night": 7.97, "eve": 7.66, "morn": 4.44},
            "feels_like": {"day": 8.73, "night": 6.72, "eve": 6.12, "morn": 2.36},
            "pressure": 1031,
            "humidity": 63,
            "dew_point": 3.3,
            "wind_speed": 3.1,
            "wind_deg": 162,
            "wind_gust": 5.95,
            "weather": [{"id": 804, "main": "Clouds", "description": "overcast clouds", "icon": "04d"}],
            "clouds": 90,
            "pop": 0,
            "uvi": 0.94,
        },
        {
            "dt": 1734519600,
            "sunrise": 1734506999,
            "sunset": 1734538706,
            "moonrise": 1734550440,
            "moonset": 1734517380,
            "moon_phase": 0.61,
            "temp": {"day": 13.06, "min": 6.68, "max": 13.06, "night": 9.96, "eve": 9.8, "morn": 6.68},
            "feels_like": {"day": 11.88, "night": 7.6, "eve": 7.76, "morn": 4.56},
            "pressure": 1024,
            "humidity": 56,
            "dew_point": 4.47,
            "wind_speed": 4.84,
            "wind_deg": 161,
            "wind_gust": 10.9,
            "weather": [{"id": 802, "main": "Clouds", "description": "scattered clouds", "icon": "03d"}],
            "clouds": 37,
            "pop": 0,
            "uvi": 1.1,
        },
        {
            "dt": 1734606000,
            "sunrise": 1734593435,
            "sunset": 1734625128,
            "moonrise": 1734641160,
            "moonset": 1734605400,
            "moon_phase": 0.64,
            "temp": {"day": 13.55, "min": 8.04, "max": 13.55, "night": 8.12, "eve": 8.04, "morn": 9.96},
            "feels_like": {"day": 12.89, "night": 4.4, "eve": 5.28, "morn": 7.69},
            "pressure": 1011,
            "humidity": 74,
            "dew_point": 8.99,
            "wind_speed": 7.42,
            "wind_deg": 259,
            "wind_gust": 13.37,
            "weather": [{"id": 501, "main": "Rain", "description": "moderate rain", "icon": "10d"}],
            "clouds": 100,
            "pop": 1,
            "rain": 10.41,
            "uvi": 2,
        },
        {
            "dt": 1734692400,
            "sunrise": 1734679868,
            "sunset": 1734711553,
            "moonrise": 1734731640,
            "moonset": 1734693060,
            "moon_phase": 0.67,
            "temp": {"day": 9.57, "min": 6.23, "max": 9.57, "night": 6.56, "eve": 6.29, "morn": 8.06},
            "feels_like": {"day": 6.25, "night": 4.8, "eve": 4.23, "morn": 4.06},
            "pressure": 1019,
            "humidity": 69,
            "dew_point": 3.99,
            "wind_speed": 8.34,
            "wind_deg": 284,
            "wind_gust": 15.47,
            "weather": [{"id": 501, "main": "Rain", "description": "moderate rain", "icon": "10d"}],
            "clouds": 58,
            "pop": 1,
            "rain": 5.1,
            "uvi": 2,
        },
    ],
}
TODAY = RESPONSE["daily"][0]  # type: ignore[index]


@pytest.fixture
def weather() -> Generator[Weather]:
    with Weather(LAT, LON, APPID) as cls:
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


@pytest.mark.parametrize("data", RESPONSE["daily"])
def test_forge_data_fuzzy(data: dict[str, Any], weather: Weather) -> None:
    print(data)
    assert isinstance(weather.forge_data(data), dict)


@freeze_time("2024-12-13")
@pytest.mark.parametrize(
    ("description", "expected"),
    [
        (
            "thunderstorm",
            [
                r"Météo",
                r"2024-12-13",
                r' _`/"".-.',
                r"   \_(   ).    Orage",
                r"   /(___(__)   3 - 10 °C",
                r"    ⚡ʻ ʻ⚡ʻ ʻ   ",
                r"SE",
                r" 18 km/h",
                r"    ʻ ʻ ʻ ʻ    6 mm/h - 75%",
            ],
        ),
        (
            "heavy thunderstorm",
            [
                "Météo",
                "2024-12-13",
                "     .-.",
                "    (   ).     Fort orage",
                "   (___(__)    3 - 10 °C",
                "  ‚ʻ⚡ʻ‚⚡‚ʻ     ",
                "SE",
                " 18 km/h",
                "  ‚ʻ‚ʻ⚡ʻ‚ʻ     6 mm/h - 75%",
            ],
        ),
        (
            "light rain",
            [
                "Météo",
                "2024-12-13",
                "     .-.",
                "    (   ).     Pluie légère",
                "   (___(__)    3 - 10 °C",
                "    ʻ ʻ ʻ ʻ    ",
                "SE",
                " 18 km/h",
                "   ʻ ʻ ʻ ʻ     6 mm/h - 75%",
            ],
        ),
        (
            "shower rain",
            [
                r"Météo",
                r"2024-12-13",
                r' _`/"".-.',
                r"   \_(   ).    Averse",
                r"   /(___(__)   3 - 10 °C",
                r"     ʻ ʻ ʻ ʻ   ",
                r"SE",
                r" 18 km/h",
                r"    ʻ ʻ ʻ ʻ    6 mm/h - 75%",
            ],
        ),
        (
            "very heavy rain",
            [
                "Météo",
                "2024-12-13",
                "     .-.",
                "    (   ).     Pluie très forte",
                "   (___(__)    3 - 10 °C",
                "  ‚ʻ‚ʻ‚ʻ‚ʻ     ",
                "SE",
                " 18 km/h",
                "  ‚ʻ‚ʻ‚ʻ‚ʻ     6 mm/h - 75%",
            ],
        ),
        (
            "heavy intensity shower rain",
            [
                r"Météo",
                r"2024-12-13",
                r' _`/"".-.',
                r"   \_(   ).    Forte averse",
                r"   /(___(__)   3 - 10 °C",
                r"   ‚ʻ‚ʻ‚ʻ‚ʻ    ",
                r"SE",
                r" 18 km/h",
                r"   ‚ʻ‚ʻ‚ʻ‚ʻ    6 mm/h - 75%",
            ],
        ),
        (
            "freezing rain",
            [
                "Météo",
                "2024-12-13",
                "     .-.",
                "    (   ).     Pluie vergalçante",
                "   (___(__)    3 - 10 °C",
                "    ʻ * ʻ *    ",
                "SE",
                " 18 km/h",
                "   * ʻ * ʻ     6 mm/h - 75%",
            ],
        ),
        (
            "snow",
            [
                "Météo",
                "2024-12-13",
                "     .-.",
                "    (   ).     Neige",
                "   (___(__)    3 - 10 °C",
                "    *  *  *    ",
                "SE",
                " 18 km/h",
                "   *  *  *     6 mm/h - 75%",
            ],
        ),
        (
            "heavy snow",
            [
                "Météo",
                "2024-12-13",
                "     .-.",
                "    (   ).     Forte neige",
                "   (___(__)    3 - 10 °C",
                "   * * * *     ",
                "SE",
                " 18 km/h",
                "  * * * *      6 mm/h - 75%",
            ],
        ),
        (
            "heavy shower snow",
            [
                r"Météo",
                r"2024-12-13",
                r' _`/"".-.',
                r"   \_(   ).    Tempête de neige",
                r"   /(___(__)   3 - 10 °C",
                r"    * * * *    ",
                r"SE",
                r" 18 km/h",
                r"   * * * *     6 mm/h - 75%",
            ],
        ),
        (
            "shower sleet",
            [
                r"Météo",
                r"2024-12-13",
                r' _`/"".-.',
                r"   \_(   ).    Averse de grésil",
                r"   /(___(__)   3 - 10 °C",
                r"     ʻ * ʻ *   ",
                r"SE",
                r" 18 km/h",
                r"    * ʻ * ʻ    6 mm/h - 75%",
            ],
        ),
        (
            "shower snow",
            [
                r"Météo",
                r"2024-12-13",
                r' _`/"".-.',
                r"   \_(   ).    Pluie de neige",
                r"   /(___(__)   3 - 10 °C",
                r"     *  *  *   ",
                r"SE",
                r" 18 km/h",
                r"    *  *  *    6 mm/h - 75%",
            ],
        ),
        (
            "fog",
            [
                "Météo",
                "2024-12-13",
                "",
                " _ - _ - _ -   Brouillard",
                "  _ - _ - _    3 - 10 °C",
                " _ - _ - _ -   ",
                "SE",
                " 18 km/h",
                "               6 mm/h - 75%",
            ],
        ),
        (
            "tornado",
            [
                "Météo",
                "2024-12-13",
                "    (    )",
                "     (  )     Tornade",
                "    ( )       3 - 10 °C",
                "     ()       ",
                "SE",
                " 18 km/h",
                "     .        6 mm/h - 75%",
            ],
        ),
        (
            "squalls",
            [
                r"Météo",
                r"2024-12-13",
                r"",
                r"               Bourrasques",
                r"   \ \ \ \     3 - 10 °C",
                r"     \ \ \ \   ",
                r"SE",
                r" 18 km/h",
                r"               6 mm/h - 75%",
            ],
        ),
        (
            "clear sky",
            [
                r"Météo",
                r"2024-12-13",
                r"    \ . /",
                r"   - .-. -     Ciel dégagé",
                r"  ‒ (   ) ‒    3 - 10 °C",
                r"   . `-᾿ .     ",
                r"SE",
                r" 18 km/h",
                r"    / ' \      6 mm/h - 75%",
            ],
        ),
        (
            "broken clouds",
            [
                "Météo",
                "2024-12-13",
                "",
                "     .--.      Nuages fragmentés",
                "  .-(    ).    3 - 10 °C",
                " (___.__)__)   ",
                "SE",
                " 18 km/h",
                "               6 mm/h - 75%",
            ],
        ),
        (
            "few clouds",
            [
                r"Météo",
                r"2024-12-13",
                r"   \__/",
                r" __/  .-.      Quelques nuages",
                r"   \_(   ).    3 - 10 °C",
                r"   /(___(__)   ",
                r"SE",
                r" 18 km/h",
                r"               6 mm/h - 75%",
            ],
        ),
        (
            "overcast clouds",
            [
                "Météo",
                "2024-12-13",
                "",
                "     .--.      Nuages couverts",
                "  .-(    ).    3 - 10 °C",
                " (___.__)__)   ",
                "SE",
                " 18 km/h",
                "               6 mm/h - 75%",
            ],
        ),
    ],
)
def test_print_data(description: str, expected: list[str], weather: Weather, printer: ThermalPrinter) -> None:
    result: list[str] = []
    out_orig = printer.out

    def out(*args: Any, **kwargs: Any) -> None:
        result.extend(args)
        out_orig(*args, **kwargs)

    today = deepcopy(TODAY)
    today["weather"][0]["description"] = description
    data = weather.forge_data(today)

    with patch.object(printer, "out", out):
        weather.printer = printer
        weather.print_data(data)

    assert result == [*expected, "Fête du jour : Lucie"]


@freeze_time("2024-12-13")
def test_print_data_wind_dir_bytes(weather: Weather, printer: ThermalPrinter) -> None:
    result: list[str] = []
    out_orig = printer.out

    def out(*args: Any, **kwargs: Any) -> None:
        result.extend(args)
        out_orig(*args, **kwargs)

    today = deepcopy(TODAY)
    today["wind_deg"] = 0.0
    data = weather.forge_data(today)

    with patch.object(printer, "out", out):
        weather.printer = printer
        weather.print_data(data)

    assert result == [
        "Météo",
        "2024-12-13",
        "",
        "     .--.      Nuages couverts",
        "  .-(    ).    3 - 10 °C",
        " (___.__)__)   ",
        b"\x8d",
        " 18 km/h",
        "               6 mm/h - 75%",
        "Fête du jour : Lucie",
    ]


@responses.activate
def test_main() -> None:
    url = URL.format(lat=LAT, lon=LON, appid=APPID)
    responses.add(responses.GET, url, json=RESPONSE)

    with patch("sys.argv", ["print-weather", str(LAT), str(LON), APPID]):
        assert main() == 0


@responses.activate
def test_main_with_port(tmp_path: Path) -> None:
    url = URL.format(lat=LAT, lon=LON, appid=APPID)
    responses.add(responses.GET, url, json=RESPONSE)

    with (
        patch("thermalprinter.constants.STATS_FILE", f"{tmp_path}/stats.json"),
        patch("sys.argv", ["print-weather", str(LAT), str(LON), APPID, "--port", "loop://"]),
    ):
        assert main() == 0

"""This is part of the Python's module to manage the DP-EH600 thermal printer.
Source: https://github.com/BoboTiG/thermalprinter.
"""


def main() -> int:
    """Entry point."""
    from argparse import ArgumentParser

    from thermalprinter.recipes.weather import Weather

    parser = ArgumentParser(prog="printer-weather")
    parser.add_argument("LAT", type=float, help="Location latitude")
    parser.add_argument("LON", type=float, help="Location longitude")
    parser.add_argument("APP_ID", help="OpenWeatherMap appid")
    parser.add_argument("--port", help="Optional printer port")
    options = parser.parse_args()

    if options.port:
        from thermalprinter import ThermalPrinter

        printer = ThermalPrinter(options.port)
    else:
        printer = None

    with Weather(options.LAT, options.LON, options.APP_ID, printer=printer) as weather:
        weather.start()

    return 0

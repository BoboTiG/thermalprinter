"""This is part of the Python's module to manage the DP-EH600 thermal printer.
Source: https://github.com/BoboTiG/thermalprinter.
"""


def main() -> int:
    """Entry point."""
    from argparse import ArgumentParser

    from thermalprinter.recipes.weather import Weather

    parser = ArgumentParser(prog="printer-weather", description=str(Weather.__doc__).split("\n", 1)[0])
    parser.add_argument("LAT", type=float, help="the location latitude")
    parser.add_argument("LON", type=float, help="the location longitude")
    parser.add_argument("APPID", help="the OpenWeatherMap appid")
    parser.add_argument("-p", "--port", help="optional printer port")
    options = parser.parse_args()

    if options.port:
        from thermalprinter import ThermalPrinter

        printer = ThermalPrinter(options.port)
    else:
        printer = None

    with Weather(options.LAT, options.LON, options.APPID, printer=printer) as weather:
        weather.start()

    return 0

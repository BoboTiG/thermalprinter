"""This is part of the Python's module to manage the DP-EH600 thermal printer.
Source: https://github.com/BoboTiG/thermalprinter.
"""


def main() -> int:
    """Entry point."""
    from argparse import ArgumentParser

    from thermalprinter.recipes.calendar import Calendar

    parser = ArgumentParser(prog="print-calendar")
    parser.add_argument("URL", help="Calendar URL")
    parser.add_argument("--port", help="Optional printer port")
    options = parser.parse_args()

    if options.port:
        from thermalprinter import ThermalPrinter

        printer = ThermalPrinter(options.port)
    else:
        printer = None

    with Calendar(options.URL, printer=printer) as calendar:
        calendar.start()

    return 0

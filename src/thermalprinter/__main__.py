def main() -> int:
    from thermalprinter import ThermalPrinter
    from thermalprinter.tools import calibrate

    with ThermalPrinter(run_setup_cmd=False) as printer:
        calibrate(printer)

    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())

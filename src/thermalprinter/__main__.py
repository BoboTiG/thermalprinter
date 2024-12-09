def main() -> int:
    from thermalprinter import ThermalPrinter

    with ThermalPrinter(run_setup_cmd=False) as printer:
        printer.calibrate()

    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())

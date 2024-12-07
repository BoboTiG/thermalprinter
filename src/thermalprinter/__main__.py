if __name__ == "__main__":
    from thermalprinter import ThermalPrinter
    from thermalprinter.tools import calibrate

    with ThermalPrinter(run_setup_cmd=False) as printer:
        calibrate(printer)

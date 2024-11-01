from thermalprinter.thermalprinter import ThermalPrinter


def test_default_value(printer: ThermalPrinter) -> None:
    assert not printer._rotate


def test_changing_no_value(printer: ThermalPrinter) -> None:
    printer.rotate()
    assert not printer._rotate


def test_changing_state_on(printer: ThermalPrinter) -> None:
    printer.rotate(True)
    assert printer._rotate


def test_changing_state_off(printer: ThermalPrinter) -> None:
    printer.rotate(False)
    assert not printer._rotate


def test_reset_value(printer: ThermalPrinter) -> None:
    printer.reset()
    assert not printer._rotate

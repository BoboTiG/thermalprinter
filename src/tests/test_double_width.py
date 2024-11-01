from thermalprinter.thermalprinter import ThermalPrinter


def test_default_value(printer: ThermalPrinter) -> None:
    assert not printer._double_width
    assert printer.max_column == 32


def test_changing_no_value(printer: ThermalPrinter) -> None:
    printer.double_width()
    assert not printer._double_width
    assert printer.max_column == 32


def test_changing_state_on(printer: ThermalPrinter) -> None:
    printer.double_width(True)
    assert printer._double_width
    assert printer.max_column == 16


def test_changing_state_off(printer: ThermalPrinter) -> None:
    printer.double_width(False)
    assert not printer._double_width
    assert printer.max_column == 32


def test_reset_value(printer: ThermalPrinter) -> None:
    printer.reset()
    assert not printer._double_width
    assert printer.max_column == 32

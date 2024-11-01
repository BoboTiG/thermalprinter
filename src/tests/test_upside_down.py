from thermalprinter.thermalprinter import ThermalPrinter


def test_default_value(printer: ThermalPrinter) -> None:
    assert not printer._upside_down


def test_changing_no_value(printer: ThermalPrinter) -> None:
    printer.upside_down()
    assert not printer._upside_down


def test_changing_state_on(printer: ThermalPrinter) -> None:
    printer.upside_down(True)
    assert printer._upside_down


def test_changing_state_off(printer: ThermalPrinter) -> None:
    printer.upside_down(False)
    assert not printer._upside_down


def test_reset_value(printer: ThermalPrinter) -> None:
    printer.reset()
    assert not printer._upside_down

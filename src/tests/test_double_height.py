from thermalprinter.thermalprinter import ThermalPrinter


def test_default_value(printer: ThermalPrinter) -> None:
    assert not printer._double_height
    assert printer._char_height == 24


def test_changing_no_value(printer: ThermalPrinter) -> None:
    printer.double_height()
    assert not printer._double_height
    assert printer._char_height == 24


def test_changing_state_on(printer: ThermalPrinter) -> None:
    printer.double_height(True)
    assert printer._double_height
    assert printer._char_height == 48


def test_changing_state_off(printer: ThermalPrinter) -> None:
    printer.double_height(False)
    assert not printer._double_height
    assert printer._char_height == 24


def test_reset_value(printer: ThermalPrinter) -> None:
    printer.reset()
    assert not printer._double_height
    assert printer._char_height == 24

from thermalprinter.constants import Justify
from thermalprinter.thermalprinter import ThermalPrinter


def test_default_value(printer: ThermalPrinter) -> None:
    assert printer._justify == Justify.LEFT


def test_changing_no_value(printer: ThermalPrinter) -> None:
    printer.justify()
    assert printer._justify == Justify.LEFT


def test_changing_good_value(printer: ThermalPrinter) -> None:
    printer.justify(Justify.CENTER)
    assert printer._justify == Justify.CENTER


def test_reset_value(printer: ThermalPrinter) -> None:
    printer.reset()
    assert printer._justify == Justify.LEFT

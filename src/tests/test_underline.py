from thermalprinter.constants import Underline
from thermalprinter.thermalprinter import ThermalPrinter


def test_default_value(printer: ThermalPrinter) -> None:
    assert printer._underline == 0


def test_changing_no_value(printer: ThermalPrinter) -> None:
    printer.underline()
    assert printer._underline == 0


def test_changing_thin(printer: ThermalPrinter) -> None:
    printer.underline(Underline.THIN)
    assert printer._underline == 1


def test_changing_thick(printer: ThermalPrinter) -> None:
    printer.underline(Underline.THICK)
    assert printer._underline == 2


def test_reset_value(printer: ThermalPrinter) -> None:
    printer.reset()
    assert printer._underline == 0

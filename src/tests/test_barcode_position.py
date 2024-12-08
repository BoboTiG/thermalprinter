from thermalprinter.constants import BarCodePosition
from thermalprinter.thermalprinter import ThermalPrinter


def test_default_value(printer: ThermalPrinter) -> None:
    assert printer._barcode_position is BarCodePosition.HIDDEN


def test_changing_no_value(printer: ThermalPrinter) -> None:
    printer.barcode_position()
    assert printer._barcode_position is BarCodePosition.HIDDEN


def test_changing_good_value(printer: ThermalPrinter) -> None:
    printer.barcode_position(BarCodePosition.BELOW)
    assert printer._barcode_position is BarCodePosition.BELOW


def test_reset_value(printer: ThermalPrinter) -> None:
    printer.reset()
    assert printer._barcode_position is BarCodePosition.HIDDEN

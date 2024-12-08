import pytest

from thermalprinter.constants import DEFAULT_BARCODE_HEIGHT
from thermalprinter.exceptions import ThermalPrinterValueError
from thermalprinter.thermalprinter import ThermalPrinter


def test_default_value(printer: ThermalPrinter) -> None:
    assert printer._barcode_height == DEFAULT_BARCODE_HEIGHT


def test_changing_no_value(printer: ThermalPrinter) -> None:
    printer.barcode_height()
    assert printer._barcode_height == DEFAULT_BARCODE_HEIGHT


def test_changing_good_value(printer: ThermalPrinter) -> None:
    printer.barcode_height(120)
    assert printer._barcode_height == 120


def test_changing_bad_value__not_int(printer: ThermalPrinter) -> None:
    with pytest.raises(ThermalPrinterValueError):
        printer.barcode_height("42")  # type: ignore[arg-type]


def test_changing_bad_value__not_in_range_low(printer: ThermalPrinter) -> None:
    with pytest.raises(ThermalPrinterValueError):
        printer.barcode_height(-42)


def test_changing_bad_value__not_in_range_high(printer: ThermalPrinter) -> None:
    with pytest.raises(ThermalPrinterValueError):
        printer.barcode_height(512)


def test_reset_value(printer: ThermalPrinter) -> None:
    printer.reset()
    assert printer._barcode_height == DEFAULT_BARCODE_HEIGHT

import pytest

from thermalprinter.exceptions import ThermalPrinterValueError
from thermalprinter.thermalprinter import ThermalPrinter


def test_default_value(printer: ThermalPrinter) -> None:
    assert printer._barcode_width == 3


def test_changing_no_value(printer: ThermalPrinter) -> None:
    printer.barcode_width()
    assert printer._barcode_width == 3


def test_changing_good_value(printer: ThermalPrinter) -> None:
    printer.barcode_width(6)
    assert printer._barcode_width == 6


def test_bad_value__not_int(printer: ThermalPrinter) -> None:
    with pytest.raises(ThermalPrinterValueError):
        printer.barcode_width("42")  # type: ignore[arg-type]


def test_changing_bad_value__not_in_range_low(printer: ThermalPrinter) -> None:
    with pytest.raises(ThermalPrinterValueError):
        printer.barcode_width(-42)


def test_changing_bad_value__not_in_range_high(printer: ThermalPrinter) -> None:
    with pytest.raises(ThermalPrinterValueError):
        printer.barcode_width(512)


def test_reset_value(printer: ThermalPrinter) -> None:
    printer.reset()
    assert printer._barcode_width == 3

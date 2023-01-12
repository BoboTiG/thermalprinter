import pytest

from thermalprinter.exceptions import ThermalPrinterValueError


def test_default_value(printer):
    assert printer._barcode_height == 162


def test_changing_no_value(printer):
    printer.barcode_height()
    assert printer._barcode_height == 162


def test_changing_good_value(printer):
    printer.barcode_height(120)
    assert printer._barcode_height == 120


def test_changing_bad_value__not_int(printer):
    with pytest.raises(ThermalPrinterValueError):
        printer.barcode_height("42")


def test_changing_bad_value__not_in_range_low(printer):
    with pytest.raises(ThermalPrinterValueError):
        printer.barcode_height(-42)


def test_changing_bad_value__not_in_range_high(printer):
    with pytest.raises(ThermalPrinterValueError):
        printer.barcode_height(512)


def test_reset_value(printer):
    printer.reset()
    assert printer._barcode_height == 162

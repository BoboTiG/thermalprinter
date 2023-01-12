import pytest

from thermalprinter.exceptions import ThermalPrinterValueError


def test_default_value(printer):
    assert printer._underline == 0


def test_changing_no_value(printer):
    printer.underline()
    assert printer._underline == 0


def test_changing_good_value(printer):
    printer.underline(2)
    assert printer._underline == 2


def test_changing_bad_value__not_int(printer):
    with pytest.raises(ThermalPrinterValueError):
        printer.underline("42")


def test_changing_bad_value__not_in_range_low(printer):
    with pytest.raises(ThermalPrinterValueError):
        printer.underline(-42)


def test_changing_bad_value__not_in_range_high(printer):
    with pytest.raises(ThermalPrinterValueError):
        printer.underline(512)


def test_reset_value(printer):
    printer.reset()
    assert printer._underline == 0

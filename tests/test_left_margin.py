# coding: utf-8

import pytest

from thermalprinter.exceptions import ThermalPrinterValueError


def test_default_value(printer):
    assert printer._left_margin == 0


def test_changing_no_value(printer):
    printer.left_margin()
    assert printer._left_margin == 0


def test_changing_good_value(printer):
    printer.left_margin(42)
    assert printer._left_margin == 42


def test_changing_bad_value__not_int(printer):
    with pytest.raises(ThermalPrinterValueError):
        printer.left_margin('42')


def test_changing_bad_value__not_in_range_low(printer):
    with pytest.raises(ThermalPrinterValueError):
        printer.left_margin(-42)


def test_changing_bad_value__not_in_range_high(printer):
    with pytest.raises(ThermalPrinterValueError):
        printer.left_margin(48)


def test_reset_value(printer):
    printer.reset()
    assert printer._left_margin == 0

# coding: utf-8

import pytest

from thermalprinter.exceptions import ThermalPrinterValueError


def test_default_value(printer):
    assert printer._size == 'S'
    assert printer.max_column == 32


def test_changing_no_value(printer):
    printer.size()
    assert printer._size == 'S'
    assert printer.max_column == 32


def test_changing_good_value_medium(printer):
    printer.size('M')
    assert printer._size == 'M'
    assert printer.max_column == 32


def test_changing_good_value_large(printer):
    printer.size('L')
    assert printer._size == 'L'
    assert printer.max_column == 16


def test_bad_value__not_str(printer):
    with pytest.raises(ThermalPrinterValueError):
        printer.size(42)


def test_changing_bad_value__not_in_range(printer):
    with pytest.raises(ThermalPrinterValueError):
        printer.size('Z')


def test_reset_value(printer):
    printer.reset()
    assert printer._size == 'S'
    assert printer.max_column == 32

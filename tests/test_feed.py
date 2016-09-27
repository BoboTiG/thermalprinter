#!/usr/bin/env python3
# coding: utf-8

import pytest

from thermalprinter.exceptions import ThermalPrinterValueError


def test_changing_no_value(printer):
    printer.feed()
    assert printer.feeds == 1


def test_changing_good_value(printer):
    printer.feed(42)
    assert printer.feeds == 42 + 1


def test_bad_value__not_int(printer):
    with pytest.raises(ThermalPrinterValueError):
        printer.feed('42')
    assert printer.feeds == 42 + 1


def test_changing_bad_value__not_in_range_low(printer):
    with pytest.raises(ThermalPrinterValueError):
        printer.feed(-42)
    assert printer.feeds == 42 + 1


def test_changing_bad_value__not_in_range_high(printer):
    with pytest.raises(ThermalPrinterValueError):
        printer.feed(512)
    assert printer.feeds == 42 + 1

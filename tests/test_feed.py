#!/usr/bin/python3
# coding: utf-8

import pytest

from ..exceptions import ThermalPrinterValueError


def test_changing_no_value(printer):
        printer.feed()


def test_changing_good_value(printer):
        printer.feed(42)


def test_bad_value__not_int(printer):
        with pytest.raises(ThermalPrinterValueError):
            printer.feed('42')


def test_changing_bad_value__not_in_range_low(printer):
        with pytest.raises(ThermalPrinterValueError):
            printer.feed(-42)


def test_changing_bad_value__not_in_range_high(printer):
        with pytest.raises(ThermalPrinterValueError):
            printer.feed(512)

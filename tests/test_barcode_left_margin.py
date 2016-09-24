#!/usr/bin/python3
# coding: utf-8

import pytest

from ..exceptions import ThermalPrinterValueError


def test_default_value(printer):
        assert printer._barcode_left_margin == 0


def test_changing_no_value(printer):
        printer.barcode_left_margin()
        assert printer._barcode_left_margin == 0


def test_changing_good_value(printer):
        printer.barcode_left_margin(120)
        assert printer._barcode_left_margin == 120


def test_bad_value__not_int(printer):
        with pytest.raises(ThermalPrinterValueError):
            printer.barcode_left_margin('42')


def test_changing_bad_value__not_in_range_low(printer):
        with pytest.raises(ThermalPrinterValueError):
            printer.barcode_left_margin(-42)


def test_changing_bad_value__not_in_range_high(printer):
        with pytest.raises(ThermalPrinterValueError):
            printer.barcode_left_margin(512)

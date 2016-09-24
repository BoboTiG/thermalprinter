#!/usr/bin/python3
# coding: utf-8

import pytest

from ..exceptions import ThermalPrinterValueError


def test_default_value(printer):
        assert printer._line_spacing == 30


def test_changing_no_value(printer):
        printer.line_spacing()
        assert printer._line_spacing == 30


def test_changing_good_value(printer):
        printer.line_spacing(42)
        assert printer._line_spacing == 42


def test_changing_bad_value__not_int(printer):
        with pytest.raises(ThermalPrinterValueError):
            printer.line_spacing('42')


def test_changing_bad_value__not_in_range_low(printer):
        with pytest.raises(ThermalPrinterValueError):
            printer.line_spacing(-42)


def test_changing_bad_value__not_in_range_high(printer):
        with pytest.raises(ThermalPrinterValueError):
            printer.line_spacing(512)

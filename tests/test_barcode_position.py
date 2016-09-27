#!/usr/bin/env python3
# coding: utf-8

import pytest

from thermalprinter.constants import BarCodePosition
from thermalprinter.exceptions import ThermalPrinterConstantError


def test_default_value(printer):
    assert printer._barcode_position is BarCodePosition.HIDDEN


def test_changing_no_value(printer):
    printer.barcode_position()
    assert printer._barcode_position is BarCodePosition.HIDDEN


def test_changing_good_value(printer):
    printer.barcode_position(BarCodePosition.BELOW)
    assert printer._barcode_position is BarCodePosition.BELOW


def test_changing_bad_value(printer):
    with pytest.raises(ThermalPrinterConstantError):
        printer.barcode_position('42')


def test_reset_value(printer):
    printer.reset()
    assert printer._barcode_position is BarCodePosition.HIDDEN

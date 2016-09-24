#!/usr/bin/python3
# coding: utf-8

import pytest

from ..constants import BarCodePosition
from ..exceptions import ThermalPrinterConstantError


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

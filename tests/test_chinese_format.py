#!/usr/bin/env python3
# coding: utf-8

import pytest

from thermalprinter.constants import Chinese
from thermalprinter.exceptions import ThermalPrinterConstantError


def test_default_value(printer):
    assert printer._chinese_format is Chinese.GBK


def test_changing_no_value(printer):
    printer.chinese_format()
    assert printer._chinese_format is Chinese.GBK


def test_changing_good_value(printer):
    printer.chinese_format(Chinese.UTF_8)
    assert printer._chinese_format is Chinese.UTF_8


def test_changing_bad_value(printer):
    with pytest.raises(ThermalPrinterConstantError):
        printer.chinese_format('42')


def test_reset_value(printer):
    printer.reset()
    assert printer._chinese_format is Chinese.GBK

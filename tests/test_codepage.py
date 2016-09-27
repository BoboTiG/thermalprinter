#!/usr/bin/env python3
# coding: utf-8

import pytest

from thermalprinter.constants import CodePage
from thermalprinter.exceptions import ThermalPrinterConstantError


def test_default_value(printer):
    assert printer._codepage is CodePage.CP437


def test_changing_no_value(printer):
    printer.codepage()
    assert printer._codepage is CodePage.CP437


def test_changing_good_value(printer):
    printer.codepage(CodePage.ISO_8859_1)
    assert printer._codepage is CodePage.ISO_8859_1


def test_changing_bad_value(printer):
    with pytest.raises(ThermalPrinterConstantError):
        printer.codepage('42')


def test_changing_but_chinese(printer):
    printer.codepage()  # Restore default
    printer.chinese(True)
    printer.codepage(CodePage.ISO_8859_1)  # Should be ignored
    assert printer._codepage is CodePage.CP437


def test_reset_value(printer):
    printer.reset()
    assert printer._codepage is CodePage.CP437

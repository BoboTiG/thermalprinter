""" UPC_A == UPC_E, skipping the last one.
    JAN13 == EAN13, skipping the last one.
    JAN8 == EAN8, skipping the last one.
"""

import pytest

from thermalprinter.constants import BarCode
from thermalprinter.exceptions import (
    ThermalPrinterConstantError,
    ThermalPrinterValueError,
)


def test_empty_values(printer):
    with pytest.raises(TypeError):
        printer.barcode()


def test_bad_values(printer):
    with pytest.raises(ThermalPrinterConstantError):
        printer.barcode("42", "EAN13")


def test_UPC_A_bad_values_too_few(printer):
    with pytest.raises(ThermalPrinterValueError):
        printer.barcode("0123456789", BarCode.UPC_A)


def test_UPC_A_bad_values_too_many(printer):
    with pytest.raises(ThermalPrinterValueError):
        printer.barcode("01234567890123456789", BarCode.UPC_A)


def test_UPC_A_bad_values_out_of_range(printer):
    with pytest.raises(ThermalPrinterValueError):
        printer.barcode("0123456789ab", BarCode.UPC_A)


def test_UPC_A_good_values(printer):
    printer.barcode("01234567890", BarCode.UPC_A)


def test_JAN13_bad_values_too_few(printer):
    with pytest.raises(ThermalPrinterValueError):
        printer.barcode("0123456789", BarCode.JAN13)


def test_JAN13_bad_values_too_many(printer):
    with pytest.raises(ThermalPrinterValueError):
        printer.barcode("01234567890123456789", BarCode.JAN13)


def test_JAN13_bad_values_out_of_range(printer):
    with pytest.raises(ThermalPrinterValueError):
        printer.barcode("0123456789ab", BarCode.JAN13)


def test_JAN13_good_values(printer):
    printer.barcode("012345678901", BarCode.JAN13)


def test_JAN8_bad_values_too_few(printer):
    with pytest.raises(ThermalPrinterValueError):
        printer.barcode("012345", BarCode.JAN8)


def test_JAN8_bad_values_too_many(printer):
    with pytest.raises(ThermalPrinterValueError):
        printer.barcode("01234567890123456789", BarCode.JAN8)


def test_JAN8_bad_values_out_of_range(printer):
    with pytest.raises(ThermalPrinterValueError):
        printer.barcode("012345ab", BarCode.JAN8)


def test_JAN8_good_values(printer):
    printer.barcode("01234567", BarCode.JAN8)


def test_CODE39_bad_values_too_few(printer):
    with pytest.raises(ThermalPrinterValueError):
        printer.barcode("", BarCode.CODE39)


def test_CODE39_bad_values_too_many(printer):
    with pytest.raises(ThermalPrinterValueError):
        printer.barcode("0" * 512, BarCode.CODE39)


def test_CODE39_bad_values_out_of_range(printer):
    with pytest.raises(ThermalPrinterValueError):
        printer.barcode("0123456789~", BarCode.CODE39)


def test_CODE39_good_values(printer):
    printer.barcode("01234567890", BarCode.CODE39)


def test_ITF_bad_values_too_few(printer):
    with pytest.raises(ThermalPrinterValueError):
        printer.barcode("", BarCode.ITF)


def test_ITF_bad_values_too_many(printer):
    with pytest.raises(ThermalPrinterValueError):
        printer.barcode("0" * 512, BarCode.ITF)


def test_ITF_bad_values_out_of_range(printer):
    with pytest.raises(ThermalPrinterValueError):
        printer.barcode("0123456789ab", BarCode.ITF)


def test_ITF_bad_values_len_not_even(printer):
    with pytest.raises(ThermalPrinterValueError):
        printer.barcode("01234567890", BarCode.ITF)


def test_ITF_good_values(printer):
    printer.barcode("012345678901", BarCode.ITF)


def test_CODABAR_bad_values_too_few(printer):
    with pytest.raises(ThermalPrinterValueError):
        printer.barcode("", BarCode.CODABAR)


def test_CODABAR_bad_values_too_many(printer):
    with pytest.raises(ThermalPrinterValueError):
        printer.barcode("0" * 512, BarCode.CODABAR)


def test_CODABAR_bad_values_out_of_range(printer):
    with pytest.raises(ThermalPrinterValueError):
        printer.barcode("0123456789~", BarCode.CODABAR)


def test_CODABAR_good_values(printer):
    printer.barcode("01234567890", BarCode.CODABAR)


def test_CODE93_bad_values_too_few(printer):
    with pytest.raises(ThermalPrinterValueError):
        printer.barcode("", BarCode.CODE93)


def test_CODE93_bad_values_too_many(printer):
    with pytest.raises(ThermalPrinterValueError):
        printer.barcode("0" * 512, BarCode.CODE93)


def test_CODE93_bad_values_out_of_range(printer):
    with pytest.raises(ThermalPrinterValueError):
        printer.barcode("0123456789现", BarCode.CODE93)


def test_CODE93_good_values(printer):
    printer.barcode("01234567890", BarCode.CODE93)


def test_CODE128_bad_values_too_few(printer):
    with pytest.raises(ThermalPrinterValueError):
        printer.barcode("0", BarCode.CODE128)


def test_CODE128_bad_values_too_many(printer):
    with pytest.raises(ThermalPrinterValueError):
        printer.barcode("0" * 512, BarCode.CODE128)


def test_CODE128_bad_values_out_of_range(printer):
    with pytest.raises(ThermalPrinterValueError):
        printer.barcode("0123456789现", BarCode.CODE128)


def test_CODE128_good_values(printer):
    printer.barcode("01234567890", BarCode.CODE128)

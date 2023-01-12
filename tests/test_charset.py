import pytest

from thermalprinter.constants import CharSet
from thermalprinter.exceptions import ThermalPrinterConstantError


def test_default_value(printer):
    assert printer._charset is CharSet.USA


def test_changing_no_value(printer):
    printer.charset()
    assert printer._charset is CharSet.USA


def test_changing_good_value(printer):
    printer.charset(CharSet.FRANCE)
    assert printer._charset is CharSet.FRANCE


def test_changing_bad_value(printer):
    with pytest.raises(ThermalPrinterConstantError):
        printer.charset("42")


def test_reset_value(printer):
    printer.reset()
    assert printer._charset is CharSet.USA

import pytest

from thermalprinter.exceptions import ThermalPrinterValueError


def test_default_value(printer):
    assert printer._justify == "L"


def test_changing_no_value(printer):
    printer.justify()
    assert printer._justify == "L"


def test_changing_good_value(printer):
    printer.justify("C")
    assert printer._justify == "C"


def test_bad_value__not_str(printer):
    with pytest.raises(ThermalPrinterValueError):
        printer.justify(42)


def test_changing_bad_value__not_in_range(printer):
    with pytest.raises(ThermalPrinterValueError):
        printer.justify("Z")


def test_changing_bad_value__unkknown(printer):
    with pytest.raises(ThermalPrinterValueError):
        printer.justify("LC")


def test_reset_value(printer):
    printer.reset()
    assert printer._justify == "L"

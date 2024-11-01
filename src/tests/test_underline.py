import pytest

from thermalprinter.exceptions import ThermalPrinterValueError
from thermalprinter.thermalprinter import ThermalPrinter


def test_default_value(printer: ThermalPrinter) -> None:
    assert printer._underline == 0


def test_changing_no_value(printer: ThermalPrinter) -> None:
    printer.underline()
    assert printer._underline == 0


def test_changing_good_value(printer: ThermalPrinter) -> None:
    printer.underline(2)
    assert printer._underline == 2


def test_changing_bad_value__not_int(printer: ThermalPrinter) -> None:
    with pytest.raises(ThermalPrinterValueError):
        printer.underline("42")  # type: ignore[arg-type]


def test_changing_bad_value__not_in_range_low(printer: ThermalPrinter) -> None:
    with pytest.raises(ThermalPrinterValueError):
        printer.underline(-42)


def test_changing_bad_value__not_in_range_high(printer: ThermalPrinter) -> None:
    with pytest.raises(ThermalPrinterValueError):
        printer.underline(512)


def test_reset_value(printer: ThermalPrinter) -> None:
    printer.reset()
    assert printer._underline == 0

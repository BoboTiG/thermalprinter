import pytest

from thermalprinter.exceptions import ThermalPrinterValueError
from thermalprinter.thermalprinter import ThermalPrinter


def test_changing_no_value(printer: ThermalPrinter) -> None:
    printer.feed()
    assert printer.feeds == 1


def test_changing_good_value(printer: ThermalPrinter) -> None:
    printer.feed(42)
    assert printer.feeds == 42 + 1


def test_bad_value__not_int(printer: ThermalPrinter) -> None:
    with pytest.raises(ThermalPrinterValueError):
        printer.feed("42")  # type: ignore[arg-type]
    assert printer.feeds == 42 + 1


def test_changing_bad_value__not_in_range_low(printer: ThermalPrinter) -> None:
    with pytest.raises(ThermalPrinterValueError):
        printer.feed(-42)
    assert printer.feeds == 42 + 1


def test_changing_bad_value__not_in_range_high(printer: ThermalPrinter) -> None:
    with pytest.raises(ThermalPrinterValueError):
        printer.feed(512)
    assert printer.feeds == 42 + 1

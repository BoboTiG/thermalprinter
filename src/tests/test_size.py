import pytest

from thermalprinter.exceptions import ThermalPrinterValueError
from thermalprinter.thermalprinter import ThermalPrinter


def test_default_value(printer: ThermalPrinter) -> None:
    assert printer._size == "S"
    assert printer.max_column == 32


def test_changing_no_value(printer: ThermalPrinter) -> None:
    printer.size()
    assert printer._size == "S"
    assert printer.max_column == 32


def test_changing_good_value_medium(printer: ThermalPrinter) -> None:
    printer.size("M")
    assert printer._size == "M"
    assert printer.max_column == 32


def test_changing_good_value_large(printer: ThermalPrinter) -> None:
    printer.size("L")
    assert printer._size == "L"
    assert printer.max_column == 16


def test_bad_value__not_str(printer: ThermalPrinter) -> None:
    with pytest.raises(ThermalPrinterValueError):
        printer.size(42)  # type: ignore[arg-type]


def test_changing_bad_value__not_in_range(printer: ThermalPrinter) -> None:
    with pytest.raises(ThermalPrinterValueError):
        printer.size("Z")


def test_changing_bad_value__unknown(printer: ThermalPrinter) -> None:
    with pytest.raises(ThermalPrinterValueError):
        printer.size("Ml")


def test_reset_value(printer: ThermalPrinter) -> None:
    printer.reset()
    assert printer._size == "S"
    assert printer.max_column == 32

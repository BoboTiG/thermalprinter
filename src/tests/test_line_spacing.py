import pytest

from thermalprinter.constants import Defaults
from thermalprinter.exceptions import ThermalPrinterValueError
from thermalprinter.thermalprinter import ThermalPrinter


def test_default_value(printer: ThermalPrinter) -> None:
    assert printer._line_spacing == Defaults.LINE_SPACING.value


def test_changing_no_value(printer: ThermalPrinter) -> None:
    printer.line_spacing()
    assert printer._line_spacing == Defaults.LINE_SPACING.value


def test_changing_good_value(printer: ThermalPrinter) -> None:
    printer.line_spacing(42)
    assert printer._line_spacing == 42


def test_changing_bad_value__not_int(printer: ThermalPrinter) -> None:
    with pytest.raises(ThermalPrinterValueError):
        printer.line_spacing("42")  # type: ignore[arg-type]


def test_changing_bad_value__not_in_range_low(printer: ThermalPrinter) -> None:
    with pytest.raises(ThermalPrinterValueError):
        printer.line_spacing(-42)


def test_changing_bad_value__not_in_range_high(printer: ThermalPrinter) -> None:
    with pytest.raises(ThermalPrinterValueError):
        printer.line_spacing(512)


def test_reset_value(printer: ThermalPrinter) -> None:
    printer.reset()
    assert printer._line_spacing == Defaults.LINE_SPACING.value

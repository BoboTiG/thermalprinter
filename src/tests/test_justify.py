import pytest

from thermalprinter.exceptions import ThermalPrinterValueError
from thermalprinter.thermalprinter import ThermalPrinter


def test_default_value(printer: ThermalPrinter) -> None:
    assert printer._justify == "L"


def test_changing_no_value(printer: ThermalPrinter) -> None:
    printer.justify()
    assert printer._justify == "L"


def test_changing_good_value(printer: ThermalPrinter) -> None:
    printer.justify("C")
    assert printer._justify == "C"


def test_bad_value__not_str(printer: ThermalPrinter) -> None:
    with pytest.raises(ThermalPrinterValueError):
        printer.justify(42)  # type: ignore[arg-type]


def test_changing_bad_value__not_in_range(printer: ThermalPrinter) -> None:
    with pytest.raises(ThermalPrinterValueError):
        printer.justify("Z")


def test_changing_bad_value__unkknown(printer: ThermalPrinter) -> None:
    with pytest.raises(ThermalPrinterValueError):
        printer.justify("LC")


def test_reset_value(printer: ThermalPrinter) -> None:
    printer.reset()
    assert printer._justify == "L"

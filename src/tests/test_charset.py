import pytest

from thermalprinter.constants import CharSet
from thermalprinter.exceptions import ThermalPrinterConstantError
from thermalprinter.thermalprinter import ThermalPrinter


def test_default_value(printer: ThermalPrinter) -> None:
    assert printer._charset is CharSet.USA


def test_changing_no_value(printer: ThermalPrinter) -> None:
    printer.charset()
    assert printer._charset is CharSet.USA


def test_changing_good_value(printer: ThermalPrinter) -> None:
    printer.charset(CharSet.FRANCE)
    assert printer._charset is CharSet.FRANCE


def test_changing_bad_value(printer: ThermalPrinter) -> None:
    with pytest.raises(ThermalPrinterConstantError):
        printer.charset("42")  # type: ignore[arg-type]


def test_reset_value(printer: ThermalPrinter) -> None:
    printer.reset()
    assert printer._charset is CharSet.USA

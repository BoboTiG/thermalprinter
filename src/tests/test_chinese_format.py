import pytest

from thermalprinter.constants import Chinese
from thermalprinter.exceptions import ThermalPrinterConstantError
from thermalprinter.thermalprinter import ThermalPrinter


def test_default_value(printer: ThermalPrinter) -> None:
    assert printer._chinese_format is Chinese.GBK


def test_changing_no_value(printer: ThermalPrinter) -> None:
    printer.chinese_format()
    assert printer._chinese_format is Chinese.GBK


def test_changing_good_value(printer: ThermalPrinter) -> None:
    printer.chinese_format(Chinese.UTF_8)
    assert printer._chinese_format is Chinese.UTF_8


def test_changing_bad_value(printer: ThermalPrinter) -> None:
    with pytest.raises(ThermalPrinterConstantError):
        printer.chinese_format("42")  # type: ignore[arg-type]


def test_reset_value(printer: ThermalPrinter) -> None:
    printer.reset()
    assert printer._chinese_format is Chinese.GBK

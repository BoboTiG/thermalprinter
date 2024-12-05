from thermalprinter.constants import Size
from thermalprinter.thermalprinter import ThermalPrinter


def test_default_value(printer: ThermalPrinter) -> None:
    assert printer._size == Size.SMALL
    assert printer.max_column == 32


def test_changing_no_value(printer: ThermalPrinter) -> None:
    printer.size()
    assert printer._size == Size.SMALL
    assert printer.max_column == 32


def test_changing_good_value_medium(printer: ThermalPrinter) -> None:
    printer.size(Size.MEDIUM)
    assert printer._size == Size.MEDIUM
    assert printer.max_column == 32


def test_changing_good_value_large(printer: ThermalPrinter) -> None:
    printer.size(Size.LARGE)
    assert printer._size == Size.LARGE
    assert printer.max_column == 16


def test_reset_value(printer: ThermalPrinter) -> None:
    printer.reset()
    assert printer._size == Size.SMALL
    assert printer.max_column == 32

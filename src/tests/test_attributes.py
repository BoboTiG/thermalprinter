import pytest

from thermalprinter.thermalprinter import ThermalPrinter


def test_attribute_get_is_online(printer: ThermalPrinter) -> None:
    assert printer.is_online


def test_attribute_get_is_sleeping(printer: ThermalPrinter) -> None:
    assert not printer.is_sleeping


def test_attribute_get_lines(printer: ThermalPrinter) -> None:
    assert printer.lines == 0


def test_attribute_get_feeds(printer: ThermalPrinter) -> None:
    assert printer.feeds == 0


def test_attribute_get_max_column(printer: ThermalPrinter) -> None:
    assert printer.max_column == 32


def test_attribute_set_is_online(printer: ThermalPrinter) -> None:
    with pytest.raises(AttributeError):
        printer.is_online = False  # type: ignore[misc]


def test_attribute_set_is_sleeping(printer: ThermalPrinter) -> None:
    with pytest.raises(AttributeError):
        printer.is_sleeping = True  # type: ignore[misc]


def test_attribute_set_lines(printer: ThermalPrinter) -> None:
    with pytest.raises(AttributeError):
        printer.lines = 42  # type: ignore[misc]


def test_attribute_set_feeds(printer: ThermalPrinter) -> None:
    with pytest.raises(AttributeError):
        printer.feeds = 42  # type: ignore[misc]


def test_attribute_set_max_column(printer: ThermalPrinter) -> None:
    with pytest.raises(AttributeError):
        printer.max_column = 42  # type: ignore[misc]

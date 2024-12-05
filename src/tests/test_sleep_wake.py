from unittest.mock import Mock, patch

import pytest

from thermalprinter.exceptions import ThermalPrinterValueError
from thermalprinter.thermalprinter import ThermalPrinter


def test_default_state(printer: ThermalPrinter) -> None:
    assert not printer.is_sleeping


def test_sleep_bad_value(printer: ThermalPrinter) -> None:
    with pytest.raises(ThermalPrinterValueError):
        printer.sleep("42")  # type: ignore[arg-type]


def test_sleep_bad_int(printer: ThermalPrinter) -> None:
    with pytest.raises(ThermalPrinterValueError):
        printer.sleep(-42)


def test_sleep(printer: ThermalPrinter) -> None:
    printer.sleep(2)
    assert printer.is_sleeping


def test_sleep_twice(printer: ThermalPrinter) -> None:
    assert not printer.is_sleeping
    with patch.object(printer, "send_command", Mock()) as mocked:
        printer.sleep(2)
        assert printer.is_sleeping
        printer.sleep(2)
        assert printer.is_sleeping
    mocked.assert_called_once()


def test_wake(printer: ThermalPrinter) -> None:
    assert not printer.is_sleeping

    printer.sleep()
    assert printer.is_sleeping

    printer.wake()
    assert not printer.is_sleeping


def test_sleep_after_wake(printer: ThermalPrinter) -> None:
    printer.sleep()
    assert printer.is_sleeping

    printer.wake()
    assert not printer.is_sleeping

    printer.sleep()
    assert printer.is_sleeping


def test_reset_value(printer: ThermalPrinter) -> None:
    printer.reset()
    assert not printer.is_sleeping

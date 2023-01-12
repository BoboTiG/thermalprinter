import pytest

from thermalprinter.exceptions import ThermalPrinterValueError


def test_default_state(printer):
    assert printer.is_sleeping is False


def test_sleep_bad_value(printer):
    with pytest.raises(ThermalPrinterValueError):
        printer.sleep("42")


def test_sleep_bad_int(printer):
    with pytest.raises(ThermalPrinterValueError):
        printer.sleep(-42)


def test_sleep(printer):
    printer.sleep(2)
    assert printer.is_sleeping is True


def test_wake(printer):
    printer.wake()
    assert printer.is_sleeping is False


def test_sleep_after_wake(printer):
    printer.sleep()
    assert printer.is_sleeping is True


def test_reset_value(printer):
    printer.reset()
    assert printer.is_sleeping is False

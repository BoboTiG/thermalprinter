import pytest

from tests.faker import FakeThermalPrinter
from thermalprinter.constants import Defaults
from thermalprinter.exceptions import ThermalPrinterValueError


def test_initialiation_with_context_manager() -> None:
    with FakeThermalPrinter() as printer:
        repr(printer)


def test_initialiation_without_context_manager() -> None:
    printer = FakeThermalPrinter()
    printer.close()


def test_default_values() -> None:
    printer = FakeThermalPrinter()
    assert repr(printer)
    assert printer._conn.baudrate == Defaults.BAUDRATE.value
    assert printer._heat_time == Defaults.HEAT_TIME.value
    assert printer._heat_interval == Defaults.HEAT_INTERVAL.value
    assert printer._most_heated_point == Defaults.MOST_HEATED_POINT.value


def test_changing_good_values() -> None:
    opt = {"heat_time": 120, "heat_interval": 8, "most_heated_point": 5}
    printer = FakeThermalPrinter(baudrate=9600, **opt)
    assert printer._conn.baudrate == 9600
    assert printer._heat_time == 120
    assert printer._heat_interval == 8
    assert printer._most_heated_point == 5


@pytest.mark.parametrize("arg", ["heat_time", "heat_interval", "most_heated_point"])
def test_changing_bad_values(arg: str) -> None:
    opt = {arg: -42}
    with pytest.raises(ThermalPrinterValueError):
        FakeThermalPrinter(**opt)

import pytest

from tests.faker import FakeThermalPrinter
from thermalprinter.constants import Defaults
from thermalprinter.exceptions import ThermalPrinterValueError


def test_initialiation_with_context_manager(port: str) -> None:
    with FakeThermalPrinter(port=port) as printer:
        repr(printer)


def test_initialiation_without_context_manager(port: str) -> None:
    printer = FakeThermalPrinter(port=port)
    printer.close()


def test_default_values(port: str) -> None:
    printer = FakeThermalPrinter(port=port)
    assert repr(printer)
    assert printer._baudrate == Defaults.BAUDRATE.value
    assert printer._heat_time == Defaults.HEAT_TIME.value
    assert printer._heat_interval == Defaults.HEAT_INTERVAL.value
    assert printer._most_heated_point == Defaults.MOST_HEATED_POINT.value


def test_changing_good_values(port: str) -> None:
    opt = {"heat_time": 120, "heat_interval": 8, "most_heated_point": 5}
    printer = FakeThermalPrinter(port=port, baudrate=9600, **opt)
    assert printer._baudrate == 9600
    assert printer._heat_time == 120
    assert printer._heat_interval == 8
    assert printer._most_heated_point == 5


@pytest.mark.parametrize("arg", ["heat_time", "heat_interval", "most_heated_point"])
def test_changing_bad_values(arg: str, port: str) -> None:
    opt = {arg: -42}
    with pytest.raises(ThermalPrinterValueError):
        FakeThermalPrinter(port=port, **opt)

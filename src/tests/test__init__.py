import pytest

from tests.faker import FakeThermalPrinter
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
    assert printer._baudrate == 19200
    assert printer.heat_time == 80
    assert printer.heat_interval == 12
    assert printer.most_heated_point == 3


def test_changing_good_values(port: str) -> None:
    opt = {"heat_time": 120, "heat_interval": 8, "most_heated_point": 5}
    printer = FakeThermalPrinter(port=port, baudrate=9600, **opt)
    assert printer._baudrate == 9600
    assert printer.heat_time == 120
    assert printer.heat_interval == 8
    assert printer.most_heated_point == 5


@pytest.mark.parametrize("arg", ["heat_time", "heat_interval", "most_heated_point"])
def test_changing_bad_values(arg: str, port: str) -> None:
    opt = {arg: -42}
    with pytest.raises(ThermalPrinterValueError):
        FakeThermalPrinter(port=port, **opt)

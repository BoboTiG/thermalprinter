import pytest

from thermalprinter import ThermalPrinter
from thermalprinter.exceptions import ThermalPrinterValueError


def test_initialiation_with_context_manager(port: str) -> None:
    with ThermalPrinter(port=port) as printer:
        repr(printer)


def test_initialiation_without_context_manager(port: str) -> None:
    printer = ThermalPrinter(port=port)
    printer.close()


def test_default_values(port: str) -> None:
    printer = ThermalPrinter(port=port)
    assert repr(printer)
    assert printer._baudrate == 19200
    assert printer.heat_time == 80
    assert printer.heat_interval == 12
    assert printer.most_heated_point == 3


def test_changing_good_values(port: str) -> None:
    opt = {"heat_time": 120, "heat_interval": 8, "most_heated_point": 5}
    printer = ThermalPrinter(port=port, baudrate=9600, **opt)
    assert printer._baudrate == 9600
    assert printer.heat_time == 120
    assert printer.heat_interval == 8
    assert printer.most_heated_point == 5


def test_changing_bad_values(port: str) -> None:
    opt = {"heat_time": 512, "heat_interval": -42, "most_heated_point": -42}
    with pytest.raises(ThermalPrinterValueError), ThermalPrinter(port=port, baudrate=9600, **opt):
        pass

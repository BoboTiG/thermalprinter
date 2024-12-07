import pytest

from thermalprinter.exceptions import ThermalPrinterCommunicationError
from thermalprinter.thermalprinter import ThermalPrinter


def test_flush(printer: ThermalPrinter) -> None:
    printer.flush(True)


def test_init(printer: ThermalPrinter) -> None:
    printer.init(42)


def test_status(printer: ThermalPrinter) -> None:
    with pytest.raises(ThermalPrinterCommunicationError):
        assert printer.status()
    assert printer.status(raise_on_error=False) == {"movement": False, "paper": False, "temp": False, "voltage": False}


def test_test(printer: ThermalPrinter) -> None:
    printer.test()

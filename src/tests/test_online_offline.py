from thermalprinter.thermalprinter import ThermalPrinter


def test_default_state(printer: ThermalPrinter) -> None:
    assert printer.is_online


def test_online(printer: ThermalPrinter) -> None:
    printer.online()
    assert printer.is_online


def test_offline(printer: ThermalPrinter) -> None:
    printer.offline()
    assert not printer.is_online


def test_online_after_offline(printer: ThermalPrinter) -> None:
    printer.online()
    assert printer.is_online


def test_reset_value(printer: ThermalPrinter) -> None:
    printer.reset()
    assert printer.is_online

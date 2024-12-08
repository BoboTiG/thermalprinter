
from thermalprinter.constants import CodePage
from thermalprinter.thermalprinter import ThermalPrinter


def test_default_value(printer: ThermalPrinter) -> None:
    assert printer._codepage is CodePage.CP437


def test_changing_no_value(printer: ThermalPrinter) -> None:
    printer.codepage()
    assert printer._codepage is CodePage.CP437


def test_changing_good_value(printer: ThermalPrinter) -> None:
    printer.codepage(CodePage.ISO_8859_1)
    assert printer._codepage is CodePage.ISO_8859_1


def test_changing_but_chinese(printer: ThermalPrinter) -> None:
    printer.codepage()  # Restore default
    printer.chinese(True)
    printer.codepage(CodePage.ISO_8859_1)  # Should be ignored
    assert printer._codepage is CodePage.CP437


def test_reset_value(printer: ThermalPrinter) -> None:
    printer.reset()
    assert printer._codepage is CodePage.CP437

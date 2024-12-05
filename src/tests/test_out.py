from thermalprinter.constants import Chinese, CodePage, Justify, Underline
from thermalprinter.thermalprinter import ThermalPrinter


def test_print_one_line(printer: ThermalPrinter) -> None:
    printer.out("This is the line.")
    assert printer.lines == 1


def test_print_two_line(printer: ThermalPrinter) -> None:
    printer.out("This is the line 1,")
    printer.out("and the seconds one.")
    assert printer.lines == 2


def test_print_one_line_centered(printer: ThermalPrinter) -> None:
    printer.out("This is the centered line.", justify=Justify.CENTER)
    assert printer._justify == Justify.LEFT


def test_print_one_line_multi_styles(printer: ThermalPrinter) -> None:
    printer.out(
        "This is the centered stroke underline line.",
        justify=Justify.CENTER,
        strike=True,
        underline=Underline.THIN,
    )
    assert printer._justify == Justify.LEFT
    assert not printer._strike
    assert printer._underline == Underline.OFF


def test_print_one_line_chinese(printer: ThermalPrinter) -> None:
    printer.out("现代汉语通用字表", chinese=True, chinese_format=Chinese.UTF_8)
    assert not printer._chinese
    assert printer._chinese_format is Chinese.GBK


def test_print_one_line_greek(printer: ThermalPrinter) -> None:
    printer.out("Στην υγειά μας!", codepage=CodePage.CP737)
    assert printer._codepage is CodePage.CP437


def test_print_one_line_bool(printer: ThermalPrinter) -> None:
    printer.out(True)


def test_print_one_line_int(printer: ThermalPrinter) -> None:
    printer.out(42)


def test_print_one_line_float(printer: ThermalPrinter) -> None:
    printer.out(42.0)


def test_print_one_line_complex(printer: ThermalPrinter) -> None:
    printer.out(42j)


def test_print_one_line_str(printer: ThermalPrinter) -> None:
    printer.out("42")


def test_print_one_line_bytes(printer: ThermalPrinter) -> None:
    printer.out(b"42")


def test_print_one_line_bytearray(printer: ThermalPrinter) -> None:
    printer.out(bytearray("42", "utf-8"))


def test_print_one_line_memoryview(printer: ThermalPrinter) -> None:
    printer.out(memoryview(b"42"))

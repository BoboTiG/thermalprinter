from thermalprinter.constants import Chinese, CodePage


def test_print_one_line(printer):
    printer.out("This is the line.")
    assert printer.lines == 1


def test_print_two_line(printer):
    printer.out("This is the line 1,")
    printer.out("and the seconds one.")
    assert printer.lines == 2 + 1


def test_print_one_line_centered(printer):
    printer.out("This is the centered line.", justify="C")
    assert printer._justify == "L"


def test_print_one_line_multi_styles(printer):
    printer.out(
        "This is the centered stroke underline line.",
        justify="C",
        strike=True,
        underline=1,
    )
    assert printer._justify == "L"
    assert printer._strike is False
    assert printer._underline == 0


def test_print_one_line_chinese(printer):
    printer.out("现代汉语通用字表", chinese=True, chinese_format=Chinese.UTF_8)
    assert printer._chinese is False
    assert printer._chinese_format is Chinese.GBK


def test_print_one_line_greek(printer):
    printer.out("Στην υγειά μας!", codepage=CodePage.CP737)
    assert printer._codepage is CodePage.CP437


def test_print_one_line_bool(printer):
    printer.out(True)


def test_print_one_line_int(printer):
    printer.out(42)


def test_print_one_line_float(printer):
    printer.out(42.0)


def test_print_one_line_complex(printer):
    printer.out(42j)


def test_print_one_line_str(printer):
    printer.out("42")


def test_print_one_line_bytes(printer):
    printer.out(b"42")


def test_print_one_line_bytearray(printer):
    printer.out(bytearray("42", "utf-8"))


def test_print_one_line_memoryview(printer):
    printer.out(memoryview(b"42"))

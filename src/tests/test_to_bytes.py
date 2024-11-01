from thermalprinter.constants import CodePage
from thermalprinter.thermalprinter import ThermalPrinter


def test_type_bool(printer: ThermalPrinter) -> None:
    isinstance(printer.to_bytes(True), bytes)


def test_type_int(printer: ThermalPrinter) -> None:
    isinstance(printer.to_bytes(42), bytes)


def test_type_float(printer: ThermalPrinter) -> None:
    isinstance(printer.to_bytes(42.0), bytes)


def test_type_complex(printer: ThermalPrinter) -> None:
    isinstance(printer.to_bytes(42j), bytes)


def test_type_str(printer: ThermalPrinter) -> None:
    isinstance(printer.to_bytes("42"), bytes)


def test_type_bytes(printer: ThermalPrinter) -> None:
    isinstance(printer.to_bytes(b"42"), bytes)


def test_type_bytearray(printer: ThermalPrinter) -> None:
    isinstance(printer.to_bytes(bytearray("42", "utf-8")), bytes)


def test_type_memoryview(printer: ThermalPrinter) -> None:
    isinstance(printer.to_bytes(memoryview(b"42")), bytes)


def test_charset_CP437(printer: ThermalPrinter) -> None:
    printer.codepage(CodePage.CP437)
    data = "42 现代汉语通用字表 aeiuoy é@`à"
    assert isinstance(printer.to_bytes(data), bytes)


def test_charset_CP932(printer: ThermalPrinter) -> None:
    printer.codepage(CodePage.CP932)
    data = "42 现代汉语通用字表 aeiuoy é@`à"
    assert isinstance(printer.to_bytes(data), bytes)


def test_charset_CP850(printer: ThermalPrinter) -> None:
    printer.codepage(CodePage.CP850)
    data = "42 现代汉语通用字表 aeiuoy é@`à"
    assert isinstance(printer.to_bytes(data), bytes)


def test_charset_CP860(printer: ThermalPrinter) -> None:
    printer.codepage(CodePage.CP860)
    data = "42 现代汉语通用字表 aeiuoy é@`à"
    assert isinstance(printer.to_bytes(data), bytes)


def test_charset_CP863(printer: ThermalPrinter) -> None:
    printer.codepage(CodePage.CP863)
    data = "42 现代汉语通用字表 aeiuoy é@`à"
    assert isinstance(printer.to_bytes(data), bytes)


def test_charset_CP865(printer: ThermalPrinter) -> None:
    printer.codepage(CodePage.CP865)
    data = "42 现代汉语通用字表 aeiuoy é@`à"
    assert isinstance(printer.to_bytes(data), bytes)


def test_charset_CYRILLIC(printer: ThermalPrinter) -> None:
    printer.codepage(CodePage.CYRILLIC)
    data = "42 现代汉语通用字表 aeiuoy é@`à"
    assert isinstance(printer.to_bytes(data), bytes)


def test_charset_CP866(printer: ThermalPrinter) -> None:
    printer.codepage(CodePage.CP866)
    data = "42 现代汉语通用字表 aeiuoy é@`à"
    assert isinstance(printer.to_bytes(data), bytes)


def test_charset_MIK(printer: ThermalPrinter) -> None:
    printer.codepage(CodePage.MIK)
    data = "42 现代汉语通用字表 aeiuoy é@`à"
    assert isinstance(printer.to_bytes(data), bytes)


def test_charset_CP755(printer: ThermalPrinter) -> None:
    printer.codepage(CodePage.CP755)
    data = "42 现代汉语通用字表 aeiuoy é@`à"
    assert isinstance(printer.to_bytes(data), bytes)


def test_charset_IRAN(printer: ThermalPrinter) -> None:
    printer.codepage(CodePage.IRAN)
    data = "42 现代汉语通用字表 aeiuoy é@`à"
    assert isinstance(printer.to_bytes(data), bytes)


def test_charset_CP862(printer: ThermalPrinter) -> None:
    printer.codepage(CodePage.CP862)
    data = "42 现代汉语通用字表 aeiuoy é@`à"
    assert isinstance(printer.to_bytes(data), bytes)


def test_charset_CP1252(printer: ThermalPrinter) -> None:
    printer.codepage(CodePage.CP1252)
    data = "42 现代汉语通用字表 aeiuoy é@`à"
    assert isinstance(printer.to_bytes(data), bytes)


def test_charset_CP1253(printer: ThermalPrinter) -> None:
    printer.codepage(CodePage.CP1253)
    data = "42 现代汉语通用字表 aeiuoy é@`à"
    assert isinstance(printer.to_bytes(data), bytes)


def test_charset_CP852(printer: ThermalPrinter) -> None:
    printer.codepage(CodePage.CP852)
    data = "42 现代汉语通用字表 aeiuoy é@`à"
    assert isinstance(printer.to_bytes(data), bytes)


def test_charset_CP858(printer: ThermalPrinter) -> None:
    printer.codepage(CodePage.CP858)
    data = "42 现代汉语通用字表 aeiuoy é@`à"
    assert isinstance(printer.to_bytes(data), bytes)


def test_charset_IRAN2(printer: ThermalPrinter) -> None:
    printer.codepage(CodePage.IRAN2)
    data = "42 现代汉语通用字表 aeiuoy é@`à"
    assert isinstance(printer.to_bytes(data), bytes)


def test_charset_LATVIA(printer: ThermalPrinter) -> None:
    printer.codepage(CodePage.LATVIA)
    data = "42 现代汉语通用字表 aeiuoy é@`à"
    assert isinstance(printer.to_bytes(data), bytes)


def test_charset_CP864(printer: ThermalPrinter) -> None:
    printer.codepage(CodePage.CP864)
    data = "42 现代汉语通用字表 aeiuoy é@`à"
    assert isinstance(printer.to_bytes(data), bytes)


def test_charset_ISO_8859_1(printer: ThermalPrinter) -> None:
    printer.codepage(CodePage.ISO_8859_1)
    data = "42 现代汉语通用字表 aeiuoy é@`à"
    assert isinstance(printer.to_bytes(data), bytes)


def test_charset_CP737(printer: ThermalPrinter) -> None:
    printer.codepage(CodePage.CP737)
    data = "42 现代汉语通用字表 aeiuoy é@`à"
    assert isinstance(printer.to_bytes(data), bytes)


def test_charset_CP1257(printer: ThermalPrinter) -> None:
    printer.codepage(CodePage.CP1257)
    data = "42 现代汉语通用字表 aeiuoy é@`à"
    assert isinstance(printer.to_bytes(data), bytes)


def test_charset_THAI(printer: ThermalPrinter) -> None:
    printer.codepage(CodePage.THAI)
    data = "42 现代汉语通用字表 aeiuoy é@`à"
    assert isinstance(printer.to_bytes(data), bytes)


def test_charset_CP720(printer: ThermalPrinter) -> None:
    printer.codepage(CodePage.CP720)
    data = "42 现代汉语通用字表 aeiuoy é@`à"
    assert isinstance(printer.to_bytes(data), bytes)


def test_charset_CP855(printer: ThermalPrinter) -> None:
    printer.codepage(CodePage.CP855)
    data = "42 现代汉语通用字表 aeiuoy é@`à"
    assert isinstance(printer.to_bytes(data), bytes)


def test_charset_CP857(printer: ThermalPrinter) -> None:
    printer.codepage(CodePage.CP857)
    data = "42 现代汉语通用字表 aeiuoy é@`à"
    assert isinstance(printer.to_bytes(data), bytes)


def test_charset_CP1250(printer: ThermalPrinter) -> None:
    printer.codepage(CodePage.CP1250)
    data = "42 现代汉语通用字表 aeiuoy é@`à"
    assert isinstance(printer.to_bytes(data), bytes)


def test_charset_CP775(printer: ThermalPrinter) -> None:
    printer.codepage(CodePage.CP775)
    data = "42 现代汉语通用字表 aeiuoy é@`à"
    assert isinstance(printer.to_bytes(data), bytes)


def test_charset_CP1254(printer: ThermalPrinter) -> None:
    printer.codepage(CodePage.CP1254)
    data = "42 现代汉语通用字表 aeiuoy é@`à"
    assert isinstance(printer.to_bytes(data), bytes)


def test_charset_CP1255(printer: ThermalPrinter) -> None:
    printer.codepage(CodePage.CP1255)
    data = "42 现代汉语通用字表 aeiuoy é@`à"
    assert isinstance(printer.to_bytes(data), bytes)


def test_charset_CP1256(printer: ThermalPrinter) -> None:
    printer.codepage(CodePage.CP1256)
    data = "42 现代汉语通用字表 aeiuoy é@`à"
    assert isinstance(printer.to_bytes(data), bytes)


def test_charset_CP1258(printer: ThermalPrinter) -> None:
    printer.codepage(CodePage.CP1258)
    data = "42 现代汉语通用字表 aeiuoy é@`à"
    assert isinstance(printer.to_bytes(data), bytes)


def test_charset_ISO_8859_2(printer: ThermalPrinter) -> None:
    printer.codepage(CodePage.ISO_8859_2)
    data = "42 现代汉语通用字表 aeiuoy é@`à"
    assert isinstance(printer.to_bytes(data), bytes)


def test_charset_ISO_8859_3(printer: ThermalPrinter) -> None:
    printer.codepage(CodePage.ISO_8859_3)
    data = "42 现代汉语通用字表 aeiuoy é@`à"
    assert isinstance(printer.to_bytes(data), bytes)


def test_charset_ISO_8859_4(printer: ThermalPrinter) -> None:
    printer.codepage(CodePage.ISO_8859_4)
    data = "42 现代汉语通用字表 aeiuoy é@`à"
    assert isinstance(printer.to_bytes(data), bytes)


def test_charset_ISO_8859_5(printer: ThermalPrinter) -> None:
    printer.codepage(CodePage.ISO_8859_5)
    data = "42 现代汉语通用字表 aeiuoy é@`à"
    assert isinstance(printer.to_bytes(data), bytes)


def test_charset_ISO_8859_6(printer: ThermalPrinter) -> None:
    printer.codepage(CodePage.ISO_8859_6)
    data = "42 现代汉语通用字表 aeiuoy é@`à"
    assert isinstance(printer.to_bytes(data), bytes)


def test_charset_ISO_8859_7(printer: ThermalPrinter) -> None:
    printer.codepage(CodePage.ISO_8859_7)
    data = "42 现代汉语通用字表 aeiuoy é@`à"
    assert isinstance(printer.to_bytes(data), bytes)


def test_charset_ISO_8859_8(printer: ThermalPrinter) -> None:
    printer.codepage(CodePage.ISO_8859_8)
    data = "42 现代汉语通用字表 aeiuoy é@`à"
    assert isinstance(printer.to_bytes(data), bytes)


def test_charset_ISO_8859_9(printer: ThermalPrinter) -> None:
    printer.codepage(CodePage.ISO_8859_9)
    data = "42 现代汉语通用字表 aeiuoy é@`à"
    assert isinstance(printer.to_bytes(data), bytes)


def test_charset_ISO_8859_15(printer: ThermalPrinter) -> None:
    printer.codepage(CodePage.ISO_8859_15)
    data = "42 现代汉语通用字表 aeiuoy é@`à"
    assert isinstance(printer.to_bytes(data), bytes)


def test_charset_THAI2(printer: ThermalPrinter) -> None:
    printer.codepage(CodePage.THAI2)
    data = "42 现代汉语通用字表 aeiuoy é@`à"
    assert isinstance(printer.to_bytes(data), bytes)


def test_charset_CP856(printer: ThermalPrinter) -> None:
    printer.codepage(CodePage.CP856)
    data = "42 现代汉语通用字表 aeiuoy é@`à"
    assert isinstance(printer.to_bytes(data), bytes)


def test_charset_CP874(printer: ThermalPrinter) -> None:
    printer.codepage(CodePage.CP874)
    data = "42 现代汉语通用字表 aeiuoy é@`à"
    assert isinstance(printer.to_bytes(data), bytes)

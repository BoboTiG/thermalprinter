#!/usr/bin/env python3
# coding: utf-8

from thermalprinter.constants import CodePage


def test_type_bool(printer):
    isinstance(printer._conv(True), bytes)


def test_type_int(printer):
    isinstance(printer._conv(42), bytes)


def test_type_float(printer):
    isinstance(printer._conv(42.0), bytes)


def test_type_complex(printer):
    isinstance(printer._conv(42j), bytes)


def test_type_str(printer):
    isinstance(printer._conv('42'), bytes)


def test_type_bytes(printer):
    isinstance(printer._conv(b'42'), bytes)


def test_type_bytearray(printer):
    isinstance(printer._conv(bytearray('42', 'utf-8')), bytes)


def test_type_memoryview(printer):
    isinstance(printer._conv(memoryview(b'42')), bytes)


def test_charset_CP437(printer):
    printer.codepage(CodePage.CP437)
    data = '42 现代汉语通用字表 aeiuoy é@`à'
    assert isinstance(printer._conv(data), bytes)


def test_charset_CP932(printer):
    printer.codepage(CodePage.CP932)
    data = '42 现代汉语通用字表 aeiuoy é@`à'
    assert isinstance(printer._conv(data), bytes)


def test_charset_CP850(printer):
    printer.codepage(CodePage.CP850)
    data = '42 现代汉语通用字表 aeiuoy é@`à'
    assert isinstance(printer._conv(data), bytes)


def test_charset_CP860(printer):
    printer.codepage(CodePage.CP860)
    data = '42 现代汉语通用字表 aeiuoy é@`à'
    assert isinstance(printer._conv(data), bytes)


def test_charset_CP863(printer):
    printer.codepage(CodePage.CP863)
    data = '42 现代汉语通用字表 aeiuoy é@`à'
    assert isinstance(printer._conv(data), bytes)


def test_charset_CP865(printer):
    printer.codepage(CodePage.CP865)
    data = '42 现代汉语通用字表 aeiuoy é@`à'
    assert isinstance(printer._conv(data), bytes)


def test_charset_CYRILLIC(printer):
    printer.codepage(CodePage.CYRILLIC)
    data = '42 现代汉语通用字表 aeiuoy é@`à'
    assert isinstance(printer._conv(data), bytes)


def test_charset_CP866(printer):
    printer.codepage(CodePage.CP866)
    data = '42 现代汉语通用字表 aeiuoy é@`à'
    assert isinstance(printer._conv(data), bytes)


def test_charset_MIK(printer):
    printer.codepage(CodePage.MIK)
    data = '42 现代汉语通用字表 aeiuoy é@`à'
    assert isinstance(printer._conv(data), bytes)


def test_charset_CP755(printer):
    printer.codepage(CodePage.CP755)
    data = '42 现代汉语通用字表 aeiuoy é@`à'
    assert isinstance(printer._conv(data), bytes)


def test_charset_IRAN(printer):
    printer.codepage(CodePage.IRAN)
    data = '42 现代汉语通用字表 aeiuoy é@`à'
    assert isinstance(printer._conv(data), bytes)


def test_charset_CP862(printer):
    printer.codepage(CodePage.CP862)
    data = '42 现代汉语通用字表 aeiuoy é@`à'
    assert isinstance(printer._conv(data), bytes)


def test_charset_CP1252(printer):
    printer.codepage(CodePage.CP1252)
    data = '42 现代汉语通用字表 aeiuoy é@`à'
    assert isinstance(printer._conv(data), bytes)


def test_charset_CP1253(printer):
    printer.codepage(CodePage.CP1253)
    data = '42 现代汉语通用字表 aeiuoy é@`à'
    assert isinstance(printer._conv(data), bytes)


def test_charset_CP852(printer):
    printer.codepage(CodePage.CP852)
    data = '42 现代汉语通用字表 aeiuoy é@`à'
    assert isinstance(printer._conv(data), bytes)


def test_charset_CP858(printer):
    printer.codepage(CodePage.CP858)
    data = '42 现代汉语通用字表 aeiuoy é@`à'
    assert isinstance(printer._conv(data), bytes)


def test_charset_IRAN2(printer):
    printer.codepage(CodePage.IRAN2)
    data = '42 现代汉语通用字表 aeiuoy é@`à'
    assert isinstance(printer._conv(data), bytes)


def test_charset_LATVIA(printer):
    printer.codepage(CodePage.LATVIA)
    data = '42 现代汉语通用字表 aeiuoy é@`à'
    assert isinstance(printer._conv(data), bytes)


def test_charset_CP864(printer):
    printer.codepage(CodePage.CP864)
    data = '42 现代汉语通用字表 aeiuoy é@`à'
    assert isinstance(printer._conv(data), bytes)


def test_charset_ISO_8859_1(printer):
    printer.codepage(CodePage.ISO_8859_1)
    data = '42 现代汉语通用字表 aeiuoy é@`à'
    assert isinstance(printer._conv(data), bytes)


def test_charset_CP737(printer):
    printer.codepage(CodePage.CP737)
    data = '42 现代汉语通用字表 aeiuoy é@`à'
    assert isinstance(printer._conv(data), bytes)


def test_charset_CP1257(printer):
    printer.codepage(CodePage.CP1257)
    data = '42 现代汉语通用字表 aeiuoy é@`à'
    assert isinstance(printer._conv(data), bytes)


def test_charset_THAI(printer):
    printer.codepage(CodePage.THAI)
    data = '42 现代汉语通用字表 aeiuoy é@`à'
    assert isinstance(printer._conv(data), bytes)


def test_charset_CP720(printer):
    printer.codepage(CodePage.CP720)
    data = '42 现代汉语通用字表 aeiuoy é@`à'
    assert isinstance(printer._conv(data), bytes)


def test_charset_CP855(printer):
    printer.codepage(CodePage.CP855)
    data = '42 现代汉语通用字表 aeiuoy é@`à'
    assert isinstance(printer._conv(data), bytes)


def test_charset_CP857(printer):
    printer.codepage(CodePage.CP857)
    data = '42 现代汉语通用字表 aeiuoy é@`à'
    assert isinstance(printer._conv(data), bytes)


def test_charset_CP1250(printer):
    printer.codepage(CodePage.CP1250)
    data = '42 现代汉语通用字表 aeiuoy é@`à'
    assert isinstance(printer._conv(data), bytes)


def test_charset_CP775(printer):
    printer.codepage(CodePage.CP775)
    data = '42 现代汉语通用字表 aeiuoy é@`à'
    assert isinstance(printer._conv(data), bytes)


def test_charset_CP1254(printer):
    printer.codepage(CodePage.CP1254)
    data = '42 现代汉语通用字表 aeiuoy é@`à'
    assert isinstance(printer._conv(data), bytes)


def test_charset_CP1255(printer):
    printer.codepage(CodePage.CP1255)
    data = '42 现代汉语通用字表 aeiuoy é@`à'
    assert isinstance(printer._conv(data), bytes)


def test_charset_CP1256(printer):
    printer.codepage(CodePage.CP1256)
    data = '42 现代汉语通用字表 aeiuoy é@`à'
    assert isinstance(printer._conv(data), bytes)


def test_charset_CP1258(printer):
    printer.codepage(CodePage.CP1258)
    data = '42 现代汉语通用字表 aeiuoy é@`à'
    assert isinstance(printer._conv(data), bytes)


def test_charset_ISO_8859_2(printer):
    printer.codepage(CodePage.ISO_8859_2)
    data = '42 现代汉语通用字表 aeiuoy é@`à'
    assert isinstance(printer._conv(data), bytes)


def test_charset_ISO_8859_3(printer):
    printer.codepage(CodePage.ISO_8859_3)
    data = '42 现代汉语通用字表 aeiuoy é@`à'
    assert isinstance(printer._conv(data), bytes)


def test_charset_ISO_8859_4(printer):
    printer.codepage(CodePage.ISO_8859_4)
    data = '42 现代汉语通用字表 aeiuoy é@`à'
    assert isinstance(printer._conv(data), bytes)


def test_charset_ISO_8859_5(printer):
    printer.codepage(CodePage.ISO_8859_5)
    data = '42 现代汉语通用字表 aeiuoy é@`à'
    assert isinstance(printer._conv(data), bytes)


def test_charset_ISO_8859_6(printer):
    printer.codepage(CodePage.ISO_8859_6)
    data = '42 现代汉语通用字表 aeiuoy é@`à'
    assert isinstance(printer._conv(data), bytes)


def test_charset_ISO_8859_7(printer):
    printer.codepage(CodePage.ISO_8859_7)
    data = '42 现代汉语通用字表 aeiuoy é@`à'
    assert isinstance(printer._conv(data), bytes)


def test_charset_ISO_8859_8(printer):
    printer.codepage(CodePage.ISO_8859_8)
    data = '42 现代汉语通用字表 aeiuoy é@`à'
    assert isinstance(printer._conv(data), bytes)


def test_charset_ISO_8859_9(printer):
    printer.codepage(CodePage.ISO_8859_9)
    data = '42 现代汉语通用字表 aeiuoy é@`à'
    assert isinstance(printer._conv(data), bytes)


def test_charset_ISO_8859_15(printer):
    printer.codepage(CodePage.ISO_8859_15)
    data = '42 现代汉语通用字表 aeiuoy é@`à'
    assert isinstance(printer._conv(data), bytes)


def test_charset_THAI2(printer):
    printer.codepage(CodePage.THAI2)
    data = '42 现代汉语通用字表 aeiuoy é@`à'
    assert isinstance(printer._conv(data), bytes)


def test_charset_CP856(printer):
    printer.codepage(CodePage.CP856)
    data = '42 现代汉语通用字表 aeiuoy é@`à'
    assert isinstance(printer._conv(data), bytes)


def test_charset_CP874(printer):
    printer.codepage(CodePage.CP874)
    data = '42 现代汉语通用字表 aeiuoy é@`à'
    assert isinstance(printer._conv(data), bytes)

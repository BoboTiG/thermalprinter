# coding: utf-8


def test_test_char(printer):
    from thermalprinter.tools import test_char

    char = '现'.encode()
    test_char(char, printer=printer)


def test_ls(capsys):
    from thermalprinter.tools import ls

    ls()
    out, _ = capsys.readouterr()
    assert out.strip() == """---CONST BarCode
Available bar code types:
BarCode.UPC_A
BarCode.UPC_E
BarCode.JAN13
BarCode.JAN8
BarCode.CODE39
BarCode.ITF
BarCode.CODABAR
BarCode.CODE93
BarCode.CODE128

---CONST BarCodePosition
Available bar code positions:
BarCodePosition.HIDDEN
BarCodePosition.ABOVE
BarCodePosition.BELOW
BarCodePosition.BOTH

---CONST CharSet
Available internal character sets:
CharSet.USA
CharSet.FRANCE
CharSet.GERMANY
CharSet.UK
CharSet.DENMARK
CharSet.SWEDEN
CharSet.ITALY
CharSet.SPAIN
CharSet.JAPAN
CharSet.NORWAY
CharSet.DENMARK2
CharSet.SPAIN2
CharSet.LATIN_AMERICAN
CharSet.KOREA
CharSet.SLOVENIA
CharSet.CHINA

---CONST Chinese
Available Chinese formats:
Chinese.GBK
Chinese.UTF_8
Chinese.BIG5

---CONST CodePage
Available character code tables:
CodePage.CP437
CodePage.CP932
CodePage.CP850
CodePage.CP860
CodePage.CP863
CodePage.CP865
CodePage.CYRILLIC
CodePage.CP866
CodePage.MIK
CodePage.CP755
CodePage.IRAN
CodePage.CP862
CodePage.CP1252
CodePage.CP1253
CodePage.CP852
CodePage.CP858
CodePage.IRAN2
CodePage.LATVIA
CodePage.CP864
CodePage.ISO_8859_1
CodePage.CP737
CodePage.CP1257
CodePage.THAI
CodePage.CP720
CodePage.CP855
CodePage.CP857
CodePage.CP1250
CodePage.CP775
CodePage.CP1254
CodePage.CP1255
CodePage.CP1256
CodePage.CP1258
CodePage.ISO_8859_2
CodePage.ISO_8859_3
CodePage.ISO_8859_4
CodePage.ISO_8859_5
CodePage.ISO_8859_6
CodePage.ISO_8859_7
CodePage.ISO_8859_8
CodePage.ISO_8859_9
CodePage.ISO_8859_15
CodePage.THAI2
CodePage.CP856
CodePage.CP874

---CONST CodePageConverted
Some code pages are not available in Python, use these instead:
CodePageConverted.MIK
CodePageConverted.CP755
CodePageConverted.IRAN
CodePageConverted.IRAN2
CodePageConverted.LATVIA
CodePageConverted.THAI
CodePageConverted.THAI2"""


def test_ls_2_constants(capsys):
    from thermalprinter.constants import BarCodePosition, Chinese
    from thermalprinter.tools import ls

    ls(BarCodePosition, Chinese)
    out, _ = capsys.readouterr()
    assert out.strip() == """---CONST BarCodePosition
Available bar code positions:
BarCodePosition.HIDDEN
BarCodePosition.ABOVE
BarCodePosition.BELOW
BarCodePosition.BOTH

---CONST Chinese
Available Chinese formats:
Chinese.GBK
Chinese.UTF_8
Chinese.BIG5"""


def test_ls_barcode(capsys):
    from thermalprinter.constants import BarCode
    from thermalprinter.tools import ls

    ls(BarCode)
    out, _ = capsys.readouterr()
    assert out.strip() == """---CONST BarCode
Available bar code types:
BarCode.UPC_A
BarCode.UPC_E
BarCode.JAN13
BarCode.JAN8
BarCode.CODE39
BarCode.ITF
BarCode.CODABAR
BarCode.CODE93
BarCode.CODE128"""


def test_ls_barcode_position(capsys):
    from thermalprinter.constants import BarCodePosition
    from thermalprinter.tools import ls

    ls(BarCodePosition)
    out, _ = capsys.readouterr()
    assert out.strip() == """---CONST BarCodePosition
Available bar code positions:
BarCodePosition.HIDDEN
BarCodePosition.ABOVE
BarCodePosition.BELOW
BarCodePosition.BOTH"""


def test_ls_charset(capsys):
    from thermalprinter.constants import CharSet
    from thermalprinter.tools import ls

    ls(CharSet)
    out, _ = capsys.readouterr()
    assert out.strip() == """---CONST CharSet
Available internal character sets:
CharSet.USA
CharSet.FRANCE
CharSet.GERMANY
CharSet.UK
CharSet.DENMARK
CharSet.SWEDEN
CharSet.ITALY
CharSet.SPAIN
CharSet.JAPAN
CharSet.NORWAY
CharSet.DENMARK2
CharSet.SPAIN2
CharSet.LATIN_AMERICAN
CharSet.KOREA
CharSet.SLOVENIA
CharSet.CHINA"""


def test_ls_chinese(capsys):
    from thermalprinter.constants import Chinese
    from thermalprinter.tools import ls

    ls(Chinese)
    out, _ = capsys.readouterr()
    assert out.strip() == """---CONST Chinese
Available Chinese formats:
Chinese.GBK
Chinese.UTF_8
Chinese.BIG5"""


def test_ls_codepage(capsys):
    from thermalprinter.constants import CodePage
    from thermalprinter.tools import ls

    ls(CodePage)
    out, _ = capsys.readouterr()
    assert out.strip() == """---CONST CodePage
Available character code tables:
CodePage.CP437
CodePage.CP932
CodePage.CP850
CodePage.CP860
CodePage.CP863
CodePage.CP865
CodePage.CYRILLIC
CodePage.CP866
CodePage.MIK
CodePage.CP755
CodePage.IRAN
CodePage.CP862
CodePage.CP1252
CodePage.CP1253
CodePage.CP852
CodePage.CP858
CodePage.IRAN2
CodePage.LATVIA
CodePage.CP864
CodePage.ISO_8859_1
CodePage.CP737
CodePage.CP1257
CodePage.THAI
CodePage.CP720
CodePage.CP855
CodePage.CP857
CodePage.CP1250
CodePage.CP775
CodePage.CP1254
CodePage.CP1255
CodePage.CP1256
CodePage.CP1258
CodePage.ISO_8859_2
CodePage.ISO_8859_3
CodePage.ISO_8859_4
CodePage.ISO_8859_5
CodePage.ISO_8859_6
CodePage.ISO_8859_7
CodePage.ISO_8859_8
CodePage.ISO_8859_9
CodePage.ISO_8859_15
CodePage.THAI2
CodePage.CP856
CodePage.CP874"""


def test_ls_codepage_converted(capsys):
    from thermalprinter.constants import CodePageConverted
    from thermalprinter.tools import ls

    ls(CodePageConverted)
    out, _ = capsys.readouterr()
    assert out.strip() == """---CONST CodePageConverted
Some code pages are not available in Python, use these instead:
CodePageConverted.MIK
CodePageConverted.CP755
CodePageConverted.IRAN
CodePageConverted.IRAN2
CodePageConverted.LATVIA
CodePageConverted.THAI
CodePageConverted.THAI2"""


def test_testing(printer):
    from thermalprinter.tools import testing

    testing(printer=printer)

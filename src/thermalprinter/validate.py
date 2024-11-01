"""This is part of the Python's module to manage the DP-EH600 thermal printer.
Source: https://github.com/BoboTiG/thermalprinter.
"""

from __future__ import annotations

from thermalprinter.constants import BarCode, BarCodePosition, CharSet, Chinese, CodePage
from thermalprinter.exceptions import ThermalPrinterConstantError, ThermalPrinterValueError


def validate_barcode(data: str, barcode_type: BarCode) -> None:
    """Validate data against the bar code type.

    :param str data: data to print.
    :param BarCode barecode_type: bar code type to use.
    :exception ThermalPrinterValueError: On incorrect ``data``'s type or value.
    :exception ThermalPrinterConstantError: On bad ``barecode_type``'s type.
    """

    def _range0(min_: int = 48, max_: int = 57) -> list[int]:
        return list(range(min_, max_ + 1))

    def _range1() -> list[int]:
        range_ = [32, 36, 37, 43]
        range_.extend(_range0(45, 57))
        range_.extend(_range0(65, 90))
        return range_

    def _range2() -> list[int]:
        range_ = [36, 43]
        range_.extend(_range0(45, 58))
        range_.extend(_range0(65, 68))
        return range_

    def _range3() -> list[int]:
        return _range0(0, 127)

    if not isinstance(barcode_type, BarCode):
        err = "Valid bar codes are: " + ", ".join([barcode.name for barcode in BarCode])
        raise ThermalPrinterConstantError(err)

    _, (min_, max_), range_type = barcode_type.value
    data_len = len(data)
    range_: list[int] = [_range0, _range1, _range2, _range3][range_type]()  # type: ignore[operator]

    if not min_ <= data_len <= max_:
        txt = "[{}] Should be {} <= len(data) <= {} (current: {})."
        err = txt.format(barcode_type.name, min_, max_, data_len)
        raise ThermalPrinterValueError(err)

    if barcode_type is BarCode.ITF and data_len % 2 != 0:
        msg = "[BarCode.ITF] len(data) must be even."
        raise ThermalPrinterValueError(msg)

    if any(ord(char) not in range_ for char in data):
        valid = map(chr, range_) if range_type != 3 else map(hex, range_)
        err = f"[{barcode_type.name}] Valid characters: {', '.join(valid)}."
        raise ThermalPrinterValueError(err)


def validate_barcode_position(position: BarCodePosition) -> None:
    """Validate a bar code position.

    :param BarCodePosition position: the position to use.
    :exception ThermalPrinterConstantError: On bad ``position``'s type.
    """
    if not isinstance(position, BarCodePosition):
        err = ", ".join([pos.name for pos in BarCodePosition])
        msg = f"Valid positions are: {err}."
        raise ThermalPrinterConstantError(msg)


def validate_charset(charset: CharSet) -> None:
    """Validate a charset.

    :param CharSet charset: new charset to use.
    :exception ThermalPrinterConstantError: On bad ``charset``'s type.
    """
    if not isinstance(charset, CharSet):
        err = f'Valid charsets are: {", ".join([cset.name for cset in CharSet])}.'
        raise ThermalPrinterConstantError(err)


def validate_chinese_format(fmt: Chinese) -> None:
    """Validate a Chinese format.

    :param Chinese fmt: new format to use.
    :exception ThermalPrinterConstantError: On bad ``fmt``'s type.
    """
    if not isinstance(fmt, Chinese):
        err = ", ".join([cfmt.name for cfmt in Chinese])
        msg = f"Valid Chinese formats are: {err}."
        raise ThermalPrinterConstantError(msg)


def validate_codepage(codepage: CodePage) -> None:
    """Validate a code page.

    :param CodePage codepage: new code page to use.
    :exception ThermalPrinterConstantError: On bad ``codepage``'s type.
    """
    if isinstance(codepage, CodePage):
        return

    codes = ""
    last = list(CodePage)[-1]
    for cpage in CodePage:
        sep = "." if cpage is last else ", "
        _, name = cpage.value
        codes += f"{cpage.name} ({name}){sep}" if name else f"{cpage.name}{sep}"
    msg = f"Valid codepages are: {codes}"
    raise ThermalPrinterConstantError(msg)

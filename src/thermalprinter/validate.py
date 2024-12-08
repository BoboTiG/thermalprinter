"""This is part of the Python's module to manage the DP-EH600 thermal printer.
Source: https://github.com/BoboTiG/thermalprinter.
"""

from __future__ import annotations

from thermalprinter.constants import BarCode
from thermalprinter.exceptions import ThermalPrinterValueError


def validate_barcode(data: str, barcode_type: BarCode) -> None:
    """Validate data against the barcode type.

    :param str data: The data to print.
    :param BarCode barecode_type: The barcode type to validate.
    :exception ThermalPrinterValueError: On incorrect ``data``'s type, or value.
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

    _, (min_, max_), range_type = barcode_type.value
    data_len = len(data)
    range_: list[int] = [_range0, _range1, _range2, _range3][range_type]()  # type: ignore[operator]

    if not min_ <= data_len <= max_:
        msg = f"[{barcode_type.name}] Should be {min_} <= len(data) <= {max_} (current: {data_len})."
        raise ThermalPrinterValueError(msg)

    if barcode_type is BarCode.ITF and data_len % 2 != 0:
        msg = "[BarCode.ITF] len(data) must be even."
        raise ThermalPrinterValueError(msg)

    if any(ord(char) not in range_ for char in data):
        valid = map(chr, range_) if range_type != 3 else map(hex, range_)
        err = f"[{barcode_type.name}] Valid characters: {', '.join(valid)}."
        raise ThermalPrinterValueError(err)

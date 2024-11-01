"""This is part of the Python's module to manage the DP-EH600 thermal printer.
Source: https://github.com/BoboTiG/thermalprinter.
"""

from __future__ import annotations

from typing import Any

from thermalprinter.constants import CONSTANTS, BarCode, BarCodePosition, Chinese, CodePage
from thermalprinter.exceptions import ThermalPrinterError
from thermalprinter.thermalprinter import ThermalPrinter

# gnu.png
TESTING_IMG_DATA = """\
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
gg=="""


def ls(*constants: Any) -> None:
    r"""Print constants values.

    :param list \\*constants: constant(s) to print.

    Examples.

    Print all constants:

    >>> ls()

    You can print only constants you want too:

    >>> from thermalprinter.constants import Chinese, CodePage
    >>> # Print Chinese values
    >>> ls(Chinese)
    >>> # Print Chinese and CodePage values
    >>> ls(Chinese, CharSet)
    """
    for constant in constants or CONSTANTS:
        try:
            print("---")
            for value in constant:
                print(value)
            print()
        except AttributeError:  # noqa: PERF203
            print(f"Unknown constant {constant!r}")


def print_char(char: str, printer: ThermalPrinter | None = None) -> None:
    """Test one character with all possible code page.

    :param str char: character to print.
    :param ThermalPrinter printer: optional printer to use for printer_tests.

    Say you are looking for the good code page to print a sequence,
    you can print it using every code pages:

    >>> print_char("现")

    This function is as simple as:

    >>> for codepage in list(CodePage):
    ...    printer.out(printer.out(f"{codepage.name}: {char}"))

    .. versionchanged:: 0.2.0
        Added ``printer`` argument.
    """
    if not printer:
        printer = ThermalPrinter()

    with printer:
        for codepage in list(CodePage):
            printer.out(f"{codepage.name}: {char}")


def printer_tests(printer: ThermalPrinter | None = None, *, raise_on_error: bool = True) -> None:
    """Send to the printer several insctructions to test every printing functions.

    :param ThermalPrinter printer: optional printer to use for printer_tests.
    :param bool raise_on_error: raise on error.

    .. versionchanged:: 0.2.0
        Removed ``port`` and ``heat_time`` arguments.
        Added ``printer`` and ``raise_on_error`` arguments.

    Example:
    >>> from thermalprinter.tools import printer_tests
    >>> printer_tests()
    >>> printer = ThermalPrinter(port="/dev/ttyS0", heat_time=120)
    >>> printer_tests(printer=printer)

    """
    try:
        if not printer:
            printer = ThermalPrinter()

        with printer:
            try:
                from PIL import Image
            except ImportError:
                if raise_on_error:
                    raise
                print("Pillow module not installed, skip picture printing.")
            else:
                import base64
                import io

                with io.BytesIO() as buffer:
                    buffer.write(base64.b64decode(TESTING_IMG_DATA))
                    buffer.seek(0)

                    printer.feed()
                    printer.image(Image.open(buffer))
                    printer.feed()

            printer.barcode_height(80)
            printer.barcode_position(BarCodePosition.BELOW)
            printer.barcode_width(3)
            printer.barcode("012345678901", BarCode.EAN13)

            printer.out("Bold", bold=True)
            printer.out("现代汉语通用字表", chinese=True, chinese_format=Chinese.UTF_8)
            printer.out("Στην υγειά μας!", codepage=CodePage.CP737)
            printer.out(b"Cards \xe8 \xe9 \xea \xeb", codepage=CodePage.CP932)
            printer.out("Double height", double_height=True)
            printer.out("Double width", double_width=True)
            printer.out("Inverse", inverse=True)
            printer.out("Rotate 90°", rotate=True, codepage=CodePage.ISO_8859_1)
            printer.out("Strike", strike=True)
            printer.out("Underline", underline=1)
            printer.out("Upside down", upside_down=True)

            printer.out("Voilà !", justify="C", strike=True, underline=2, codepage=CodePage.ISO_8859_1)

            printer.feed(2)
    except ThermalPrinterError as ex:
        if raise_on_error:
            raise
        print(ex)

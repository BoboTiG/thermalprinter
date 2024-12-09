"""This is part of the Python's module to manage the DP-EH600 thermal printer.
Source: https://github.com/BoboTiG/thermalprinter.
"""

from __future__ import annotations

from typing import Any

from thermalprinter.constants import CONSTANTS


def ls(*constants: Any) -> None:
    """Print constants values.

    :param list constants: Constant(s) to print.

    Print all constants:

    >>> ls()

    Print Chinese constant values:

    >>> ls(Chinese)

    Print Chinese, and CodePage, constant values:

    >>> ls(Chinese, CharSet)
    """
    for constant in constants or CONSTANTS:
        print("---")
        for value in constant:
            print(value)
        print()

"""Python module to manage the DP-EH600 thermal printer.

This module is maintained by Mickaël 'Tiger-222' Schoentgen <contact@tiger-222.fr>.
Based on the work of Phil Burgess and Fried/Ladyada (Adafruit).

Complete documentation: https://thermalprinter.readthedocs.io

You can always get the latest version of this module at: https://github.com/BoboTiG/thermalprinter

If that URL should fail, try contacting the author.
"""

from __future__ import annotations

from thermalprinter.constants import BarCode, BarCodePosition, CharSet, Chinese, CodePage, Command
from thermalprinter.exceptions import ThermalPrinterError
from thermalprinter.thermalprinter import ThermalPrinter

__version__ = "0.3.0"
__author__ = "Mickaël Schoentgen"
__copyright__ = f"""
Copyright (c) 2016-2024, {__author__}

Permission to use, copy, modify, and distribute this software and its
documentation for any purpose and without fee or royalty is hereby
granted, provided that the above copyright notice appear in all copies
and that both that copyright notice and this permission notice appear
in supporting documentation or portions thereof, including
modifications, that you make.
"""
__license__ = "MIT"
__all__ = [
    "BarCode",
    "BarCodePosition",
    "CharSet",
    "Chinese",
    "Command",
    "CodePage",
    "ThermalPrinter",
    "ThermalPrinterError",
]

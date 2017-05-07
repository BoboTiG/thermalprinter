#!/usr/bin/env python3
# coding: utf-8
''' Python module to manage the DP-EH600 thermal printer.

    This module is maintained by Mickaël Schoentgen <contact@tiger-222.fr>.
    Based on the work of Phil Burgess and Fried/Ladyada (Adafruit).

    Python 3+ only.

    Complete documentation:
        https://thermalprinter.readthedocs.io

    You can always get the latest version of this module at:
        https://github.com/BoboTiG/thermalprinter
    If that URL should fail, try contacting the author.
'''

from .constants import BarCode, BarCodePosition, CharSet, Chinese, Command, \
    CodePage
from .exceptions import ThermalPrinterError
from .thermalprinter import ThermalPrinter

__version__ = '0.1.7'
__author__ = 'Mickaël Schoentgen'
__copyright__ = '''
    Copyright (c) 2016-2017, Mickaël 'Tiger-222' Schoentgen

    Permission to use, copy, modify, and distribute this software and its
    documentation for any purpose and without fee or royalty is hereby
    granted, provided that the above copyright notice appear in all copies
    and that both that copyright notice and this permission notice appear
    in supporting documentation or portions thereof, including
    modifications, that you make.
'''
__license__ = 'MIT'
__all__ = ['BarCode', 'BarCodePosition', 'CharSet', 'Chinese', 'Command',
           'CodePage', 'ThermalPrinter', 'ThermalPrinterError']

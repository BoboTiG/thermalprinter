#!/usr/bin/env python3
# coding: utf-8
''' This is part of the Python's module to manage the DP-EH600 thermal printer.
    Source: https://github.com/BoboTiG/thermalprinter
'''

from .constants import BarCode, BarCodePosition, CharSet, Chinese, CodePage
from .thermalprinter import ThermalPrinter


def test_char(char):
    ''' Test one character with all possible code page. '''

    with ThermalPrinter() as printer:
        for codepage in list(CodePage):
            printer.out(
                '{}: {}'.format(codepage.name, char), codepage=codepage)


def ls(*constants):
    ''' Print constants values.

        >>> ls()
        # all constants printer

        >>> ls(Chinese)
        # print Chinese constants

        >>> ls(Chinese, CharSet)
        # print Chinese and CharSet constants
    '''

    # pylint: disable=invalid-name

    if not constants:
        constants = [BarCode, BarCodePosition, CharSet, Chinese, CodePage]

    for constant in constants:
        try:
            print('---CONST', constant.__name__)
            print(constant.__doc__.strip())
            for value in constant:
                print(value)
            print()
        except AttributeError:
            print('Unknown constant "{}".'.format(constant))

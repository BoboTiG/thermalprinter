#!/usr/bin/env python3
# coding: utf-8
''' This is part of the Python's module to manage the DP-EH600 thermal printer.
    Source: https://github.com/BoboTiG/thermalprinter
'''

from .constants import BarCode, BarCodePosition, CharSet, Chinese, CodePage, \
    CodePageConverted
from .exceptions import ThermalPrinterError
from .thermalprinter import ThermalPrinter


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
        constants = [BarCode, BarCodePosition, CharSet, Chinese, CodePage,
                     CodePageConverted]

    for constant in constants:
        try:
            print('---CONST', constant.__name__)
            print(constant.__doc__.strip())
            for value in constant:
                print(value)
            print()
        except AttributeError:
            print('Unknown constant "{}".'.format(constant))


def test_char(char):
    ''' Test one character with all possible code page. '''

    with ThermalPrinter() as printer:
        for codepage in list(CodePage):
            printer.out('{}: {}'.format(codepage.name, char),
                        codepage=codepage)


def testing(port='/dev/ttyAMA0', heat_time=80):
    ''' Print all possibilities.
        Optional argument: heat_time

        >>> from thermalprinter.utils import testing
        >>> testing()
        >>> testing(port='/dev/ttyS0', heat_time=120)
    '''

    try:
        with ThermalPrinter(port=port, heat_time=heat_time) as printer:
            try:
                from PIL import Image
                from os.path import abspath, dirname, realpath

                cwd = dirname(realpath(abspath(__file__)))
                printer.feed()
                printer.image(Image.open('{}/../gnu.png'.format(cwd)))
                printer.feed()
            except ImportError:
                print('Pillow module not installed, skip picture printing.')

            printer.barcode_height(80)
            printer.barcode_position(BarCodePosition.BELOW)
            printer.barcode_width(3)
            printer.barcode('012345678901', BarCode.EAN13)

            printer.out('Bold', bold=True)
            printer.out('现代汉语通用字表', chinese=True,
                        chinese_format=Chinese.UTF_8)
            printer.out('Double height', double_height=True)
            printer.out('Double width', double_width=True)
            printer.out('Inverse', inverse=True)
            printer.out('Rotate 90°', rotate=True,
                        codepage=CodePage.ISO_8859_1)
            printer.out('Strike', strike=True)
            printer.out('Underline', underline=1)
            printer.out('Upside down', upside_down=True)

            printer.out('Voilà !', justify='C', strike=True,
                        underline=2, codepage=CodePage.ISO_8859_1)

            printer.feed(2)
    except ThermalPrinterError as ex:
        print(ex)

#!/usr/bin/env python3
# coding: utf-8
''' This is part of the Python's module to manage the DP-EH600 thermal printer.
    Source: https://github.com/BoboTiG/thermalprinter
'''

from .constants import BarCode, BarCodePosition, Chinese, CodePage
from .exception import ThermalPrinterError
from .thermalprinter import ThermalPrinter


def tests():
    try:
        with ThermalPrinter() as printer:
            try:
                from PIL import Image
                printer.feed()
                printer.image(Image.open('gnu.png'))
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
            return 0
    except ThermalPrinterError as ex:
        print(ex)

    return 1


if __name__ == '__main__':
    exit(tests())

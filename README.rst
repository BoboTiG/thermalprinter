DP-EH600 thermal printer
========================

Python module to manage the DP-EH600 thermal printer.

This is a clean follow of the technical manual with few helpers. An example is better than thousand words:

.. code:: python

    from ThermalPrinter import *

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

        printer.println('Bold', bold=True)
        printer.println('Double height', double_height=True)
        printer.println('Double width', double_width=True)
        printer.println('Inverse', inverse=True)
        printer.println('Rotate 90°', rotate=True, codepage=CodePage.ISO_8859_1)
        printer.println('Strike', strike=True)
        printer.println('Underline', underline=1)
        printer.println('Upside down', upside_down=True)
        printer.println('现代汉语通用字表', chinese=True, chinese_format=Chinese.BIG5)

        printer.println('Voilà !', justify='C', strike=True, underline=2)

        printer.feed(2)

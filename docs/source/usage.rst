=====
Usage
=====

An example is better than a thousand words:

.. code-block:: python

    from PIL import Image
    from ThermalPrinter import *

    with ThermalPrinter(port="/dev/ttyAMA0") as printer:
        # Picture
        printer.image(Image.open("gnu.png"))

        # Bar codes
        printer.barcode_height(80)
        printer.barcode_position(BarCodePosition.BELOW)
        printer.barcode_width(3)
        printer.barcode("012345678901", BarCode.EAN13)

        # Styles
        printer.out("Bold", bold=True)
        printer.out("Double height", double_height=True)
        printer.out("Double width", double_width=True)
        printer.out("Inverse", inverse=True)
        printer.out("Rotate 90°", rotate=True, codepage=CodePage.ISO_8859_1)
        printer.out("Strike", strike=True)
        printer.out("Underline", underline=1)
        printer.out("Upside down", upside_down=True)

        # Chinese (almost all alphabets exist)
        printer.out("现代汉语通用字表", chinese=True, chinese_format=Chinese.UTF_8)
                    
        # Greek (excepted the ΐ character)
        printer.out("Στην υγειά μας!", codepage=CodePage.CP737)

        # Other characters
        printer.out(b"Cards \xe8 \xe9 \xea \xeb", codepage=CodePage.CP932)

        # Accents
        printer.out("Voilà !", justify="C", strike=True, underline=2, codepage=CodePage.ISO_8859_1)

        # Line feeds
        printer.feed(2)


Instance the class
==================

Import the module:

.. code-block:: python

    from thermalprinter import ThermalPrinter

So the module can be used as simply as:

.. code-block:: python

    with ThermalPrinter() as printer:
        # ...

Or:

.. code-block:: python

    printer = ThermalPrinter()

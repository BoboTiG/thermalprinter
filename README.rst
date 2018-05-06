DP-EH600 thermal printer
========================

.. image:: https://travis-ci.org/BoboTiG/thermalprinter.svg?branch=master
    :target: https://travis-ci.org/BoboTiG/thermalprinter

Python module to manage the DP-EH600 thermal printer (the one sold by AdaFruit).

- **Python 3+ only** and PEP8 compliant;
- this is a clean follow of the technical manual with few helpers;
- and there is a `complete, and beautiful, documentation <https://thermalprinter.readthedocs.io>`_ :)
- **contibutors** are welcome, check the `developer guide <https://thermalprinter.readthedocs.io/en/latest/developers.html>`_!

Installation
------------

As simple as:

.. code-block:: bash

    python3 -m pip install --upgrade --user thermalprinter


Usage
-----

An example is better than thousand words:

.. code-block:: python

    from PIL import Image
    from ThermalPrinter import *

    with ThermalPrinter(port='/dev/ttyAMA0') as printer:
        # Picture
        printer.image(Image.open('gnu.png'))

        # Bar codes
        printer.barcode_height(80)
        printer.barcode_position(BarCodePosition.BELOW)
        printer.barcode_width(3)
        printer.barcode('012345678901', BarCode.EAN13)

        # Styles
        printer.out('Bold', bold=True)
        printer.out('Double height', double_height=True)
        printer.out('Double width', double_width=True)
        printer.out('Inverse', inverse=True)
        printer.out('Rotate 90°', rotate=True, codepage=CodePage.ISO_8859_1)
        printer.out('Strike', strike=True)
        printer.out('Underline', underline=1)
        printer.out('Upside down', upside_down=True)

        # Chinese (almost all alphabets exist)
        printer.out('现代汉语通用字表', chinese=True,
                    chinese_format=Chinese.UTF_8)
                    
        # Greek (excepted the ΐ character)
        printer.out('Στην υγειά μας!', codepage=CodePage.CP737)

        # Accents
        printer.out('Voilà !', justify='C', strike=True,
                    underline=2, codepage=CodePage.ISO_8859_1)

        # Line feeds
        printer.feed(2)

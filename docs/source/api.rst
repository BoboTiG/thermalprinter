===
API
===

.. currentmodule:: thermalprinter

Class
=====

.. autoclass:: ThermalPrinter

Methods
=======

Barcodes
--------

.. automethod:: ThermalPrinter.barcode
.. automethod:: ThermalPrinter.barcode_height
.. automethod:: ThermalPrinter.barcode_left_margin
.. automethod:: ThermalPrinter.barcode_position
.. automethod:: ThermalPrinter.barcode_width
.. automethod:: ThermalPrinter.validate_barcode

Images
------

.. automethod:: ThermalPrinter.image

Text Styling
------------

.. automethod:: ThermalPrinter.bold
.. automethod:: ThermalPrinter.char_spacing
.. automethod:: ThermalPrinter.double_height
.. automethod:: ThermalPrinter.double_width
.. automethod:: ThermalPrinter.inverse
.. automethod:: ThermalPrinter.justify
.. automethod:: ThermalPrinter.left_margin
.. automethod:: ThermalPrinter.line_spacing
.. automethod:: ThermalPrinter.rotate
.. automethod:: ThermalPrinter.size
.. automethod:: ThermalPrinter.strike
.. automethod:: ThermalPrinter.underline
.. automethod:: ThermalPrinter.upside_down

Encoding and Charsets
---------------------

.. automethod:: ThermalPrinter.charset
.. automethod:: ThermalPrinter.codepage

Chinese
-------

.. automethod:: ThermalPrinter.chinese
.. automethod:: ThermalPrinter.chinese_format

Printing
--------

.. automethod:: ThermalPrinter.feed
.. automethod:: ThermalPrinter.out

Printer State
-------------

.. automethod:: ThermalPrinter.offline
.. automethod:: ThermalPrinter.online
.. automethod:: ThermalPrinter.sleep
.. automethod:: ThermalPrinter.status
.. automethod:: ThermalPrinter.status_to_dict
.. automethod:: ThermalPrinter.reset
.. automethod:: ThermalPrinter.test
.. automethod:: ThermalPrinter.wake

Special Methods
---------------

.. automethod:: ThermalPrinter.flush
.. automethod:: ThermalPrinter.init
.. automethod:: ThermalPrinter.send_command
.. automethod:: ThermalPrinter.to_bytes

Attributes
==========

All these attributes are **read-only**.

.. autoproperty:: ThermalPrinter.feeds
.. autoproperty:: ThermalPrinter.has_paper
.. autoproperty:: ThermalPrinter.is_online
.. autoproperty:: ThermalPrinter.is_sleeping
.. autoproperty:: ThermalPrinter.lines
.. autoproperty:: ThermalPrinter.max_column

Exceptions
==========

.. module:: thermalprinter.exceptions

.. autoexception:: ThermalPrinterError
.. autoexception:: ThermalPrinterCommunicationError
.. autoexception:: ThermalPrinterValueError

Constants
=========

.. module:: thermalprinter.constants

Barcode Types
-------------

.. autoenum:: BarCode

Barcode Positions
-----------------

.. autoenum:: BarCodePosition

Characters Sets
---------------

.. autoenum:: CharSet

Chinese Formats
---------------

.. autoenum:: Chinese

Code Pages
----------

.. autoenum:: CodePage

Code Pages Fallback
-------------------

.. autoenum:: CodePageConverted

.. note::

    If you find a better fit for one of the code page below, `open an issue <https://github.com/BoboTiG/thermalprinter/issues>`_ please (or better: `send a patch <https://github.com/BoboTiG/thermalprinter/pulls>`_) 🤗

Commands
--------

.. autoenum:: Command

Text Justification
------------------

.. autoenum:: Justify

Text Size
---------

.. autoenum:: Size

Text Underline
--------------

.. autoenum:: Underline

Other
-----

.. autodata:: DEFAULT_BARCODE_HEIGHT
.. autodata:: DEFAULT_BARCODE_WIDTH
.. autodata:: DEFAULT_BAUDRATE
.. autodata:: DEFAULT_HEAT_INTERVAL
.. autodata:: DEFAULT_HEAT_TIME
.. autodata:: DEFAULT_LINE_SPACING
.. autodata:: DEFAULT_MOST_HEATED_POINT
.. autodata:: DEFAULT_PORT
.. autodata:: MAX_IMAGE_WIDTH

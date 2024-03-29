===
API
===

.. currentmodule:: thermalprinter

Class
=====

.. autoclass:: ThermalPrinter

Methods
=======

Bar codes
---------

.. automethod:: ThermalPrinter.barcode
.. automethod:: ThermalPrinter.barcode_height
.. automethod:: ThermalPrinter.barcode_left_margin
.. automethod:: ThermalPrinter.barcode_position
.. automethod:: ThermalPrinter.barcode_width

Images
------

.. automethod:: ThermalPrinter.image

Text styling
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

Encoding and charsets
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

Printer state
-------------

.. automethod:: ThermalPrinter.offline
.. automethod:: ThermalPrinter.online
.. automethod:: ThermalPrinter.sleep
.. automethod:: ThermalPrinter.status
.. automethod:: ThermalPrinter.reset
.. automethod:: ThermalPrinter.test
.. automethod:: ThermalPrinter.wake

Special methods
---------------

.. automethod:: ThermalPrinter.flush
.. automethod:: ThermalPrinter.send_command
.. automethod:: ThermalPrinter.to_bytes

Attributes
==========

All these attributes are **read-only**.

.. autoproperty:: ThermalPrinter.feeds
.. autoproperty:: ThermalPrinter.is_online
.. autoproperty:: ThermalPrinter.is_sleeping
.. autoproperty:: ThermalPrinter.lines
.. autoproperty:: ThermalPrinter.max_column

Exceptions
==========

.. module:: thermalprinter.exceptions

.. autoexception:: ThermalPrinterError
.. autoexception:: ThermalPrinterCommunicationError
.. autoexception:: ThermalPrinterConstantError
.. autoexception:: ThermalPrinterValueError

Constants
=========

.. module:: thermalprinter.constants

Bar codes types
---------------

.. autoenum:: BarCode

Bar codes positions
-------------------

.. autoenum:: BarCodePosition

Characters sets
---------------

.. autoenum:: CharSet

Chinese formats
---------------

.. autoenum:: Chinese

Code pages
----------

.. autoenum:: CodePage

Code pages fallback
-------------------

.. autoenum:: CodePageConverted

If you find a better fit for one of the code page below, `open an issue <https://github.com/BoboTiG/thermalprinter/issues>`_ please (or `send a patch <https://github.com/BoboTiG/thermalprinter/pulls>`_).

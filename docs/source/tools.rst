=====
Tools
=====

.. module:: thermalprinter.tools

Few helpers, and they are free :)

Constants
=========

.. autofunction:: ls

Tests
=====

.. autofunction:: printer_tests

Code pages
==========

.. autofunction:: print_char

Data validation
===============

.. module:: thermalprinter.validate

These are special functions to handle data validation.
As it could take a lot of lines and logic, we prefered create them outsite the class to keep a light code for every ``ThermalPrinter``'s methods.

.. autofunction:: validate_barcode
.. autofunction:: validate_barcode_position
.. autofunction:: validate_charset
.. autofunction:: validate_chinese_format
.. autofunction:: validate_codepage

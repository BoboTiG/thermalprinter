=====
Tools
=====

Few helpers, and they are free :)

Constants
=========

.. module:: thermalprinter.tools

.. function:: ls(\*constants)

    :param list \*constants: constants to print.

    Print a list of constants and their values.

        >>> ls()
        All constants will be printed here.

    You can print only constants you want too::

        >>> from thermalprinter.constants import Chinese, CodePage

        >>> ls(Chinese)
        Chinese values will be prited here.

        >>> ls(Chinese, CodePage)
        Chinese and CodePage values will be prited here.


Tests
=====

.. function:: testing(port='/dev/ttyAMA0', heat_time=80)

    :param str port: serial port to use, known as the device name.
    :param int heat_time: printer heat time.

    Send to the printer several insctructions to test every printing functions.


Code pages
==========

.. function:: test_char(char)

    :param bytes char: bytes to print.

    Test one character with all possible code page. Say you are looking for the good code page to print a sequence, you can print it using every code pages::

        >>> test_char(b'现')

    This function is as simple as::

        for codepage in list(CodePage):
            printer.out('{}: {}'.format(codepage.name, char),
                        codepage=codepage)


Data validation
===============

These are special functions to handle data validation. As it could take a lot of lines and logic, we prefered create them outsite the class to keep a light code for every ``ThermalPrinter``'s methods.

.. module:: thermalprinter.validate

.. function:: validate_barcode(data, barcode_type) -> None

        :param mixed data: data to print.
        :param BarCode barecode_type: bar code type to use.
        :exception ThermalPrinterValueError: On incorrect ``data``'s type or value.
        :exception ThermalPrinterConstantError: On bad ``barecode_type``'s type.

        Validate data against the bar code type.

.. function:: validate_barcode_position(position) -> None

        :param BarCodePosition position: the position to use.
        :exception ThermalPrinterConstantError: On bad ``position``'s type.

        Validate a bar code position.

.. function:: validate_charset(charset) -> None

        :param CharSet charset: new charset to use.
        :exception ThermalPrinterConstantError: On bad ``charset``'s type.

        Validate a charset.

.. function:: validate_chinese_format(fmt) -> None

        :param Chinese fmt: new format to use.
        :exception ThermalPrinterConstantError: On bad ``fmt``'s type.

        Validate a Chinese format.

.. function:: validate_codepage(codepage) -> None

        :param CodePage codepage: new code page to use.
        :exception ThermalPrinterConstantError: On bad ``codepage``'s type.

        Validate a code page.

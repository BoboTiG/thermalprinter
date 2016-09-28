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

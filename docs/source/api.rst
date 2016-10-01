==================
ThermalPrinter API
==================

.. module:: thermalprinter

Class
=====

.. class:: ThermalPrinter

    .. method:: __init__(port='/dev/ttyAMA0', baudrate=19200, \*\*kwargs)

        :param str port:
            Serial port to use, known as the device name.

        :param int baudrate:
            Baud rate such as 9600 or 115200 etc.

        :param dict \*\*kwargs:
            Additionnal optional arguments:

            - ``heat_time`` (int): printer heat time (default: ``80``);
            - ``heat_interval`` (int): printer heat time interval (default: ``12``);
            - ``most_heated_point`` (int): for the printer, the most heated point (default: ``3``).

        :exception ThermalPrinterValueError: On incorrect argument's type or value.


Methods
=======

Bar codes
---------

.. class:: ThermalPrinter

    .. method:: barcode(data, barecode_type) -> None

        :param mixed data: data to print.
        :param BarCode barecode_type: bar code type to use.
        :exception ThermalPrinterValueError: On incorrect ``data``'s type or value.
        :exception ThermalPrinterConstantError: On bad ``barecode_type``'s type.

        Bar code printing. All checks are done to ensure the data validity.


    .. method:: barcode_height(height=162) -> None

        :param int height: bar code height (min=1, max=255).
        :exception ThermalPrinterValueError: On incorrect ``height``'s type or value.

        Set the bar code height.


    .. method:: barcode_left_margin(margin=0) -> None

        :param int margin: left margin (min=0, max=255).
        :exception ThermalPrinterValueError: On incorrect ``margin``'s type or value.

        Set the left margin of the bar code.


    .. method:: barcode_position(position=BarCodePosition.HIDDEN) -> None

        :param BarCodePosition position: the position to use.
        :exception ThermalPrinterConstantError: On bad ``position``'s type.

        Set the position of the text relative to the bar code.


    .. method:: barcode_width(width=3) -> None

        :param int width: bar code with (min=2, max=6).
        :exception ThermalPrinterValueError: On incorrect ``width``'s type or value.

        Set the bar code width.


Images
------

.. class:: ThermalPrinter

    .. method:: image(image) -> None

        :param Image image: the image to print.
        :exception ThermalPrinterValueError: On bad ``image``'s type.

        Print Image. Requires Python Imaging Library.
        Image will be cropped to 384 pixels width if
        necessary, and converted to 1-bit w/diffusion dithering.
        For any other behavior (scale, B&W threshold, etc.), use
        the Imaging Library to perform such operations before
        passing the result to this function.

        Max width: 384px.

            >>> from PIL import Image
            >>> printer.image(Image.open('picture.png'))


Text styling
------------

.. class:: ThermalPrinter

    .. method:: bold(state=False) -> None

        :param bool state: new state.

        Turn emphasized mode on/off.


    .. method:: char_spacing(spacing=0) -> None

        :param int spacing: spacing to use (min=0, max=255).
        :exception ThermalPrinterValueError: On incorrect ``spacing``'s type or value.

        Set the right character spacing.


    .. method:: double_height(state=False) -> None

        :param bool state: new state.

        Set double height mode.


    .. method:: double_width(state=False) -> None

        :param bool state: new state.

        Select double width mode.


    .. method:: inverse(state=False) -> None

        :param bool state: new state.

        Turn white/black reverse printing mode.


    .. method:: justify(value='L') -> None

        :param str value: the new justification.
        :exception ThermalPrinterValueError: On incorrect ``value``'s type or value.

        Set text justification:

            - left (``L``)
            - center (``C``)
            - right (``R``)


    .. method:: left_margin(margin=0) -> None

        :param int margin: the new margin (min=0, max=47).
        :exception ThermalPrinterValueError: On incorrect ``margin``'s type or value.

        Set the left margin.


    .. method:: line_spacing(spacing=30) -> None

        :param int spacing: the new spacing (min=0, max=255).
        :exception ThermalPrinterValueError: On incorrect ``spacing``'s type or value.

        Set line spacing.


    .. method:: rotate(state=False) -> None

        :param bool state: new state.

        Turn on/off clockwise rotation of 90°.


    .. method:: size(value='S') -> None

        :param str value: the new text size.
        :exception ThermalPrinterValueError: On incorrect ``value``'s type or value.

        Set text size:

            - small (``S``)
            - medium: double height (``M``)
            - large: double width and height (``L``)

        This method affects :attr:`max_column`.


    .. method:: strike(state=False) -> None

        :param bool state: new state.

        Turn on/off double-strike mode.


    .. method:: underline(weight=0) -> None

        :param int weight: the underline's weight (min=0, max=2).
        :exception ThermalPrinterValueError: On incorrect ``weight``'s type or value.

        Turn underline mode on/off:

            - 0: turns off underline mode
            - 1: turns on underline mode (1 dot thick)
            - 2: turns on underline mode (2 dots thick)


    .. method:: upside_down(state=False) -> None

        :param bool state: new state.

        Turns on/off upside-down printing mode.


Encoding and charsets
---------------------

.. class:: ThermalPrinter

    .. method:: charset(charset=CharSet.USA) -> None

        :param CharSet charset: new charset to use.
        :exception ThermalPrinterConstantError: On bad ``charset``'s type.

        Select an internal character set.


    .. method:: codepage(codepage=CodePage.CP437) -> None

        :param CodePage codepage: new code page to use.
        :exception ThermalPrinterConstantError: On bad ``codepage``'s type.

        Select character code table.


Chinese
-------

.. class:: ThermalPrinter

    .. method:: chinese(state=False) -> None

        :param bool state: new state.

        Select/cancel Chinese mode.


    .. method:: chinese_format(fmt=Chinese.GBK) -> None

        :param Chinese fmt: new format to use.
        :exception ThermalPrinterConstantError: On bad ``fmt``'s type.

        Selection of the Chinese format.


Printing
--------

.. class:: ThermalPrinter

    .. method:: feed(number=1) -> None

        :param int number: number of lines.
        :exception ThermalPrinterValueError: On incorrect ``number``'s type or value.

        Feeds by the specified number of lines (min=0, max=255).


    .. method:: out(data, line_feed=True, \*\*kwargs) -> None

        :param mixed data: the data to print.
        :param bool line_feed: send a line break after the printed data.
        :param dict \*\*kwargs: additional styles to apply.

        Send a line to the printer.

        You can pass formatting instructions directly via arguments::

            >>> printer.out(data, justify='C', inverse=True)

        This will prevent you to do::

            >>> printer.justify('C')
            >>> printer.inverse(True)
            >>> printer.out(data)
            >>> printer.inverse(False)
            >>> printer.justify('L')


Printer state
-------------

.. class:: ThermalPrinter

    .. method:: offline() -> None

        Take the printer offline. Print commands sent after this
        will be ignored until :attr:`offline()` is called.


    .. method:: online() -> None

        Take the printer online. Subsequent print commands will be obeyed.


    .. method:: sleep(seconds=1) -> None

        :param int seconds: value to pass to the printer (min=0, unit=sec).
        :exception ThermalPrinterValueError: On incorrect ``seconds``'s type or value.

        Put the printer into a low-energy state.


    .. method:: status() -> dict

        Check the printer status. If RX pin is not connected, all values
        will be set to True.

        Return a dict:

            - movement: ``False`` if the movement is not connected;
            - paper: ``False`` is no paper;
            - temp: ``False`` if the temperature exceeds 60°C;
            - voltage: ``False`` if the voltage is higher than 9.5V.


    .. method:: reset() -> None

        Reset the printer to factory defaults.


    .. method:: test() -> None

        Print the test page (contains printer's settings).


    .. method:: wake() -> None

        Wake up the printer.


Special methods
---------------

.. class:: ThermalPrinter

    .. method:: send_command(\*args) -> None

        :param list \*args: command and arguments for the printer.

        Raw byte-writing.


    .. method:: to_bytes(data) -> bytes

        :param mixed data: any type of data to print.

        Convert data before sending to the printer.


Attributes
==========

All these attributes are **read-only**.

.. class:: ThermalPrinter

    .. attribute:: feeds

        :getter: Number of printed line feeds since the start of the script.
        :type: int
        :exception ThermalPrinterAttributeError: When trying to assign a value.


    .. attribute:: is_online

        :getter: The printer is online.
        :type: bool
        :exception ThermalPrinterAttributeError: When trying to assign a value.


    .. attribute:: is_sleeping

        :getter: The printer is sleeping.
        :type: bool
        :exception ThermalPrinterAttributeError: When trying to assign a value.


    .. attribute:: lines

        :getter: Number of printed lines since the start of the script.
        :type: int
        :exception ThermalPrinterAttributeError: When trying to assign a value.


    .. attribute:: max_column

        :getter: Number of printable characters on one line.
        :type: int
        :exception ThermalPrinterAttributeError: When trying to assign a value.


Exceptions
==========

.. exception:: ThermalPrinterError

    Base class for thermal printer exceptions.

.. exception:: ThermalPrinterAttributeError

    Exception that is raised when trying to assign something to a read-only attribute.

.. exception:: ThermalPrinterConstantError

    Exception that is raised on inexistant or out of range constant.

.. exception:: ThermalPrinterValueError

    Exception that is raised on incorrect type or value passed to any method.


Constants
=========

Bar codes types
---------------

.. data:: BarCode.UPC_A
.. data:: BarCode.UPC_E
.. data:: BarCode.JAN13
.. data:: BarCode.JAN8
.. data:: BarCode.CODE39
.. data:: BarCode.ITF
.. data:: BarCode.CODABAR
.. data:: BarCode.CODE93
.. data:: BarCode.CODE128

Bar codes positions
-------------------

.. data:: BarCodePosition.HIDDEN
.. data:: BarCodePosition.ABOVE
.. data:: BarCodePosition.BELOW
.. data:: BarCodePosition.BOTH


Characters sets
---------------

.. data:: CharSet.USA
.. data:: CharSet.FRANCE
.. data:: CharSet.GERMANY
.. data:: CharSet.UK
.. data:: CharSet.DENMARK
.. data:: CharSet.SWEDEN
.. data:: CharSet.ITALY
.. data:: CharSet.SPAIN
.. data:: CharSet.JAPAN
.. data:: CharSet.NORWAY
.. data:: CharSet.DENMARK2
.. data:: CharSet.SPAIN2
.. data:: CharSet.LATIN_AMERICAN
.. data:: CharSet.KOREA
.. data:: CharSet.SLOVENIA
.. data:: CharSet.CHINA


Chinese formats
---------------

.. data:: Chinese.GBK
.. data:: Chinese.UTF_8
.. data:: Chinese.BIG5

Code pages
----------

.. data:: CodePage.CP437

    the United States of America, European standard

.. data:: CodePage.CP932

    Katakana

.. data:: CodePage.CP850

    Multi language

.. data:: CodePage.CP860

    Portuguese

.. data:: CodePage.CP863

    Canada, French

.. data:: CodePage.CP865

    Western Europe

.. data:: CodePage.CYRILLIC

    The Slavic language

.. data:: CodePage.CP866

    The Slavic 2

.. data:: CodePage.MIK

    The Slavic / Bulgaria

.. data:: CodePage.CP755

    Eastern Europe, Latvia 2

.. data:: CodePage.IRAN

    Iran, Persia

.. data:: CodePage.CP862

    Hebrew

.. data:: CodePage.CP1252

    Latin 1 [WCP1252]

.. data:: CodePage.CP1253

    Greece [WCP1253]

.. data:: CodePage.CP852

    Latina 2

.. data:: CodePage.CP858

    A variety of language Latin 1 + Europe

.. data:: CodePage.IRAN2

    Persian

.. data:: CodePage.LATVIA
.. data:: CodePage.CP864

    Arabic

.. data:: CodePage.ISO_8859_1

    Western Europe

.. data:: CodePage.CP737

    Greece

.. data:: CodePage.CP1257

    The Baltic Sea

.. data:: CodePage.THAI

    Thai Wen

.. data:: CodePage.CP720

    Arabic

.. data:: CodePage.CP855
.. data:: CodePage.CP857

    Turkish

.. data:: CodePage.CP1250

    Central Europe [WCP1250]

.. data:: CodePage.CP775
.. data:: CodePage.CP1254

    Turkish [WCP1254]

.. data:: CodePage.CP1255

    Hebrew [WCP1255]

.. data:: CodePage.CP1256

    Arabic [WCP1256]

.. data:: CodePage.CP1258

    Vietnamese [WCP1258]

.. data:: CodePage.ISO_8859_2

    Latin 2

.. data:: CodePage.ISO_8859_3

    Latin 3

.. data:: CodePage.ISO_8859_4

    Baltic languages

.. data:: CodePage.ISO_8859_5

    The Slavic language

.. data:: CodePage.ISO_8859_6

    Arabic

.. data:: CodePage.ISO_8859_7

    Greece

.. data:: CodePage.ISO_8859_8

    Hebrew

.. data:: CodePage.ISO_8859_9

    Turkish

.. data:: CodePage.ISO_8859_15

    : Latin 9

.. data:: CodePage.THAI2

    Thai Wen 2

.. data:: CodePage.CP856
.. data:: CodePage.CP874

Code pages fallback
-------------------

Certain code pages are not available on Python, so we use a little translation table.
If you find a better fit for one of the code page below, `open an issue <https://github.com/BoboTiG/thermalprinter/issues>`_ please (or `send a patch <https://github.com/BoboTiG/thermalprinter/pulls>`_).

.. data:: CodePageConverted.MIK

    ISO8859-5

.. data:: CodePageConverted.CP755

    UTF-8

.. data:: CodePageConverted.IRAN

    UTF-8

.. data:: CodePageConverted.IRAN2

    UTF-8

.. data:: CodePageConverted.LATVIA

    UTF-8

.. data:: CodePageConverted.THAI

    ISO8859-11

.. data:: CodePageConverted.THAI2

    UTF-8

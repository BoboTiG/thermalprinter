DP-EH600 thermal printer
========================

Python module to manage the DP-EH600 thermal printer. **Python 3+ only** and PEP8 compliant.

This is a clean follow of the technical manual with few helpers. An example is better than thousand words:

.. code:: python

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
        printer.println('Bold', bold=True)
        printer.println('Double height', double_height=True)
        printer.println('Double width', double_width=True)
        printer.println('Inverse', inverse=True)
        printer.println('Rotate 90°', rotate=True, codepage=CodePage.ISO_8859_1)
        printer.println('Strike', strike=True)
        printer.println('Underline', underline=1)
        printer.println('Upside down', upside_down=True)

        # Chinese (almost all alphabets exist)
        printer.println('现代汉语通用字表', chinese=True, chinese_format=Chinese.UTF_8)

        # Accents
        printer.println('Voilà !', justify='C', strike=True, underline=2, codepage=CodePage.ISO_8859_1)

        # Line feeds
        printer.feed(2)


Installation
============

.. code:: shell

    $ git clone https://github.com/BoboTiG/thermalprinter.git


Testing
=======

Checking code with `pytest`:

.. code:: shell

    $ py.test-3 tests

Testing printing functions:

.. code:: python

    # Testing all kind of avilable stuff:
    >>> from thermalprinter.tests import tests
    >>> tests()
    >>> tests(heat_time=120)

    # Print printer test page
    from thermalprinter import ThermalPrinter
    with ThermalPrinter() as printer:
        printer.test()


Instance the class
==================

So the module can be used as simply as:

.. code:: python

    from thermalprinter import ThermalPrinter

    with ThermalPrinter() as printer:
        # ...


Arguments
=========

All args are optional:

- `port`: serial port to use, know as device name (default: '/dev/ttyAMA0);
- `baudrate`: baud rate such as 9600 or 115200 (default: 19200);
- `heat_time`: for the printer, heat time (default: 80);
- `heat_interval`: for the printer, heat time interval (default: 12);
- `most_heated_point`: for the printer, the most heated point (default: 3).


Errors
======

If an error occures, the `ThermalPrinterError` parent exception is raised. There
are two children exceptions:

- `ThermalPrinterConstantError` for exceptions impacting a constant;
- `ThermalPrinterValueError` for exceptions impacting a value.


Constants
=========

.. code:: python

    >>> from thermalprinter.helpers import ls
    >>> ls()
    ---CONST BarCode
    Available bar code types:
    UPC_A   value: 65, 11 <= len(data) <=  12
    UPC_E   value: 66, 11 <= len(data) <=  12
    JAN13   value: 67, 12 <= len(data) <=  13
    JAN8    value: 68,  7 <= len(data) <=   8
    CODE39  value: 69,  1 <= len(data) <= 255
    ITF     value: 70,  1 <= len(data) <= 255
    CODABAR value: 71,  1 <= len(data) <= 255
    CODE93  value: 72,  1 <= len(data) <= 255
    CODE128 value: 73,  2 <= len(data) <= 255

    ---CONST BarCodePosition
    Available bar code positions:
    HIDDEN value: 0
    ABOVE  value: 1
    BELOW  value: 2
    BOTH   value: 3

    ---CONST CharSet
    Available internal character sets:
    USA            value:  0
    FRANCE         value:  1
    GERMANY        value:  2
    UK             value:  3
    DENMARK        value:  4
    SWEDEN         value:  5
    ITALY          value:  6
    SPAIN          value:  7
    JAPAN          value:  8
    NORWAY         value:  9
    DENMARK2       value: 10
    SPAIN2         value: 11
    LATIN_AMERICAN value: 12
    KOREA          value: 13
    SLOVENIA       value: 14
    CHINA          value: 15

    ---CONST Chinese
    Available Chinese formats:
    GBK   value: 0
    UTF_8 value: 1
    BIG5  value: 3

    ---CONST CodePage
    Available character code tables:
    CP437       value:  0, desc: the United States of America, European standard
    CP932       value:  1, desc: Katakana
    CP850       value:  2, desc: Multi language
    CP860       value:  3, desc: Portuguese
    CP863       value:  4, desc: Canada, French
    CP865       value:  5, desc: Western Europe
    CYRILLIC    value:  6, desc: The Slavic language
    CP866       value:  7, desc: The Slavic 2
    MIK         value:  8, desc: The Slavic / Bulgaria
    CP755       value:  9, desc: Eastern Europe, Latvia 2
    IRAN        value: 10, desc: Iran, Persia
    CP862       value: 15, desc: Hebrew
    CP1252      value: 16, desc: Latin 1 [WCP1252]
    CP1253      value: 17, desc: Greece [WCP1253]
    CP852       value: 18, desc: Latina 2
    CP858       value: 19, desc: A variety of language Latin 1 + Europe
    IRAN2       value: 20, desc: Persian
    LATVIA      value: 21, desc:
    CP864       value: 22, desc: Arabic
    ISO_8859_1  value: 23, desc: Western Europe
    CP737       value: 24, desc: Greece
    CP1257      value: 25, desc: The Baltic Sea
    THAI        value: 26, desc: Thai Wen
    CP720       value: 27, desc: Arabic
    CP855       value: 28, desc:
    CP857       value: 29, desc: Turkish
    CP1250      value: 30, desc: Central Europe [WCP1250]
    CP775       value: 31, desc:
    CP1254      value: 32, desc: Turkish [WCP1254]
    CP1255      value: 33, desc: Hebrew [WCP1255]
    CP1256      value: 34, desc: Arabic [WCP1256]
    CP1258      value: 35, desc: Vietnamese [WCP1258]
    ISO_8859_2  value: 36, desc: Latin 2
    ISO_8859_3  value: 37, desc: Latin 3
    ISO_8859_4  value: 38, desc: Baltic languages
    ISO_8859_5  value: 39, desc: The Slavic language
    ISO_8859_6  value: 40, desc: Arabic
    ISO_8859_7  value: 41, desc: Greece
    ISO_8859_8  value: 42, desc: Hebrew
    ISO_8859_9  value: 43, desc: Turkish
    ISO_8859_15 value: 44, desc: Latin 9
    THAI2       value: 45, desc: Thai Wen 2
    CP856       value: 46, desc:
    CP874       value: 47, desc:

    ---CONST CodePageConverted
    Some code pages are not available in Python, use these instead:
    MIK         fallback: iso8859-5
    CP755       fallback: utf-8
    IRAN        fallback: utf-8
    IRAN2       fallback: utf-8
    LATVIA      fallback: utf-8
    THAI        fallback: iso8859-11
    THAI2       fallback: utf-8

    >>> from thermalprinter.constants import Chinese
    >>> ls(Chinese)
    ---CONST Chinese
    Available Chinese formats:
    GBK   value: 0
    UTF_8 value: 1
    BIG5  value: 3


----

API
===

**barcode**

.. code:: python

    >>> barcode(data, bc_type)
    ''' Bar code printing.
        `bc_type` is a value from `BarCode`. All checks are done to ensure
        the data validity.
    '''

**barcode_height**

.. code:: python

    >>> barcode_height(height=80)
    ''' Set bar code height.
        1 <= `height` <= 255
    '''

**barcode_left_margin**

.. code:: python

    >>> barcode_left_margin(margin=0)
    ''' Set the bar code printed on the left spacing.
        0 <= `margin` <= 255
    '''

**barcode_position**

.. code:: python

    >>> barcode_position(position=BarCodePosition.HIDDEN)
    ''' Set bar code position.
        `position` is a value from `BarCodePosition`.
    '''

**barcode_width**

.. code:: python

    >>> barcode_width(width=2)
    ''' Set bar code width.
        2 <= `width` <= 6
    '''

**bold**

.. code:: python

    >>> bold(state=False)
    ''' Turn emphasized mode on/off. '''

**charset**

.. code:: python

    >>> charset(charset=CharSet.USA)
    ''' Select an internal character set.
        `charset` is a value from `CharSet`.
    '''

**char_spacing**

.. code:: python

    >>> char_spacing(spacing=0)
    ''' Set the right character spacing.
        0 <= `spacing` <= 255
    '''

**chinese**

.. code:: python

    >>> chinese(state=False)
    ''' Select/cancel Chinese mode. '''

**chinese_format**

.. code:: python

    >>> chinese_format(fmt=Chinese.GBK)
    ''' Selection of the Chinese format.
        `fmt` is a value from `Chinese`.
    '''

**codepage**

.. code:: python

    >>> codepage(codepage=CodePage.CP437)
    ''' Select character code table.
        `codepage` is a value from `CodePage`.
    '''

**double_height**

.. code:: python

    >>> double_height(state=False)
    ''' Set double height mode. '''

**double_width**

.. code:: python

    >>> double_width(state=False)
    ''' Select double width mode. '''

**feed**

.. code:: python

    >>> feed(number=1)
    ''' Feeds by the specified number of lines.
        0 <= `number` <= 255
    '''

**image**

.. code:: python

    >>> image(image)
    ''' Print Image. Requires Python Imaging Library.
        Image will be cropped to 384 pixels width if
        necessary, and converted to 1-bit w/diffusion dithering.
        For any other behavior (scale, B&W threshold, etc.), use
        the Imaging Library to perform such operations before
        passing the result to this function.

        Max width: 384px.
    '''

**inverse**

.. code:: python

    >>> inverse(state=False)
    ''' Turn white/black reverse printing mode. '''

**justify**

.. code:: python

    >>> justify(value='L')
    ''' Set text justification.
        `value` can be one of:
            'L': align left
            'C': center text
            'R': align right
    '''

**left_margin**

.. code:: python

    >>> left_margin(margin=0)
    ''' Set the left margin.
        0 <= `margin` <= 47
    '''

**line_spacing**

.. code:: python

    >>> line_spacing(spacing=30)
    ''' Set line spacing.
        0 <= `spacing` <= 255
    '''

**offline**

.. code:: python

    >>> offline()
    ''' Take the printer offline. Print commands sent after this
        will be ignored until 'online' is called.
    '''

**online**

.. code:: python

    >>> online()
    ''' Take the printer online.
        Subsequent print commands will be obeyed.
    '''

**out**

.. code:: python

    >>> out(data, line_feed=True, **kwargs)
    ''' Send a line to the printer.

        You can pass formatting instructions directly via an argument:
            println(text, justify='C', inverse=True)

        This will prevent you to do:
           justify('C')
           inverse(True)
           println(text)
           inverse()
           justify()
    '''

**print_char**

.. code:: python

    >>> print_char(char='', number=1, codepage=None)
    ''' Print one character one or several times in a given code page. '''

**rotate**

.. code:: python

    >>> rotate(state=False)
    ''' Turn on/off clockwise rotation of 90°. '''

**size**

.. code:: python

    >>> size(value='S')
    ''' Set text size.
        `value` can be one of:
            'S': default
            'M': double height
            'L': double width and height
    '''

**sleep**

.. code:: python

    >>> sleep(seconds=1)
    ''' Put the printer into a low-energy state. '''

**status** => dict

.. code:: python

    >>> status()
    ''' Check the printer status. If RX pin is not connected, all values
        will be set to True.

        Return a dict:
            movement: False if the movement is not connected
               paper: False is no paper
                temp: False if the temperature exceeds 60°C
             voltage: False if the voltage is higher than 9.5V
    '''

**strike**

.. code:: python

    >>> strike(state=False)
    ''' Turn on/off double-strike mode. '''

**reset**

.. code:: python

    >>> reset()
    ''' Reset the printer to factory defaults. '''

**test**

.. code:: python

    >>> test()
    ''' Print settings as test. '''

**underline**

.. code:: python

    >>> underline(weight=0)
    ''' Turn underline mode on/off.
        `weight` can be one of:
            0: turns off underline mode
            1: turns on underline mode (1 dot thick)
            2: turns on underline mode (2 dots thick)
    '''

**upside_down**

.. code:: python

    >>> upside_down(state=False)
    ''' Turns on/off upside-down printing mode. '''

**wake**

.. code:: python

    >>> wake()
    ''' Wake up the printer. '''

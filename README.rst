DP-EH600 thermal printer
========================

Python module to manage the DP-EH600 thermal printer. **Python 3+ only** and PEP8 compliant.

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
        printer.println('现代汉语通用字表', chinese=True, chinese_format=Chinese.UTF_8)

        printer.println('Voilà !', justify='C', strike=True, underline=2, codepage=CodePage.ISO_8859_1)

        printer.feed(2)


Installation
============

.. code:: shell

    $ git clone https://github.com/BoboTiG/thermalprinter.git


Testing
=======

.. code:: python

    from thermalprinter.tests import tests

    tests()


Instance the class
==================

So the module can be used as simply as:

.. code:: python

    from thermalprinter import ThermalPrinter

    with ThermalPrinter as printer:
        # ...


Errors
======

If an error occures, the `ThermalPrinterError` exception is raised.


----

API
===

**barcode**

.. code:: python

    >>> barcode(bc_type)
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

    >>> barcode_position(position=None)
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

    >>> bold(state=True)
    ''' Turn emphasized mode on/off. '''

**charset**

.. code:: python

    >>> charset(charset=None)
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

    >>> chinese(state=True)
    ''' Select/cancel Chinese mode. '''

**chinese_format**

.. code:: python

    >>> chinese_format(fmt=None)
    ''' Selection of the Chinese format.
        `fmt` is a value from `Chinese`.
    '''

**codepage**

.. code:: python

    >>> codepage(codepage=None)
    ''' Select character code table.
        `codepage` is a value from `CodePage`.
    '''

**double_height**

.. code:: python

    >>> double_height(state=True)
    ''' Set double height mode. '''

**double_width**

.. code:: python

    >>> double_width(state=True)
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

    >>> inverse(state=True)
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

**print_char**

.. code:: python

    >>> print_char(char='', number=1, codepage=None)
    ''' Print one character one or several times in a given code page. '''

**println**

.. code:: python

    >>> println(data, line_feed=True, **kwargs)
    ''' Send a line to the printer.

        You can pass formatting instructions directly via an argument:
            println(text, justify='C', inverse=True)

        This will prevent you to do:
           justify('C')
           inverse(True)
           println(text)
           inverse(False)
           justify('L')
    '''

**rotate**

.. code:: python

    >>> rotate(state=True)
    ''' Turn on/off clockwise rotation of 90°. '''

**set_defaults**

.. code:: python

    >>> set_defaults()
    ''' Reset formatting parameters. '''

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

    >>> strike(state=True)
    ''' Turn on/off double-strike mode. '''

**test**

.. code:: python

    >>> test()
    ''' Print settings as test. '''

**underline**

.. code:: python

    >>> underline(weight=1)
    ''' Turn underline mode on/off.
        `weight` can be one of:
            0: turns off underline mode
            1: turns on underline mode (1 dot thick)
            2: turns on underline mode (2 dots thick)
    '''

**upside_down**

.. code:: python

    >>> upside_down(state=True)
    ''' Turns on/off upside-down printing mode. '''

**wake**

.. code:: python

    >>> wake()
    ''' Wake up the printer. '''

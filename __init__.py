#!/usr/bin/env python
# coding: utf-8
''' Python module to manage the DP-EH600 thermal printer.

    This module is maintained by Mickaël Schoentgen <mickael@jmsinfo.co>.
    Based on the work of Phil Burgess and Fried/Ladyada (Adafruit).

    Python 3+ only.
    Dependencies:
        python3-serial
        python3-pillow (for pictures printing)
        cchardet (pip3)

    usermod -G dialout -a $USER

    You can always get the latest version of this module at:
        https://github.com/BoboTiG/thermalprinter
    If that URL should fail, try contacting the author.
'''

from enum import Enum
from time import sleep, time

from cchardet import detect
from serial import Serial

__all__ = ['BarCode', 'Command', 'ThermalPrinter']


__version__ = '1.0.0-dev'
__author__ = 'Mickaël Schoentgen'
__copyright__ = '''
    Copyright (c) 2016, Mickaël Schoentgen

    Permission to use, copy, modify, and distribute this software and its
    documentation for any purpose and without fee or royalty is hereby
    granted, provided that the above copyright notice appear in all copies
    and that both that copyright notice and this permission notice appear
    in supporting documentation or portions thereof, including
    modifications, that you make.
'''
__license__ = 'MIT'


def convert_encoding(data, is_raw=False, is_image=False, new='latin-1'):
    ''' Convert data before sending to the printer. '''

    if isinstance(data, (bool, int)):
        if is_raw:
            data = chr(data)
        else:
            data = str(data)
    elif isinstance(data, bytes):
        current = detect(data)['encoding']
        if new.lower() != current.lower():
            data = data.decode(current, data).encode(new)
    if is_image:
        return data.encode(new, 'replace')
    return data.encode('cp1252', 'replace')


class Command(Enum):
    ''' ASCII character codes used to send commands. '''

    ASCII_DC2 = 18
    ASCII_ESC = 27
    ASCII_FS = 28
    ASCII_GS = 29


class BarCode(Enum):
    ''' Available barcode types. '''

    # UPC_A = 0
    # UPC_E = 1
    # EAN13 = 2
    # EAN8 = 3
    # CODE39 = 4
    I25 = 5
    CODEBAR = 6
    CODE93 = 7
    CODE128 = 8
    CODE11 = 9
    MSI = 10


class ThermalPrinter(Serial):
    ''' I talk to printers. Easy! '''

    # pylint: disable=too-many-ancestors
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-public-methods

    resume_time = 0.0
    byte_time = 0.0
    dot_print_time = 0.033
    dot_feed_time = 0.0025
    prev_byte = '\n'
    column = 0
    max_column = 32
    char_height = 24
    line_spacing = 6
    barcode_height = 50
    print_mode = 0

    def __init__(self, port='/dev/ttyAMA0', baudrate=19200):
        ''' Print init. '''

        self.heat_time = 80
        self.heat_dots = 7
        self.heat_interval = 2
        self.baud_rate = baudrate
        self.fw_ver = 269
        super().__init__(port=port, baudrate=baudrate, timeout=10)
        self.reset()
        self.set_default()

    def timeout_set(self, delay):
        ''' Sets estimated completion time for a just-issued task.

            Because there's no flow control between the printer and computer,
            special care must be taken to avoid overrunning the printer's
            buffer.  Serial output is throttled based on serial speed as well
            as an estimate of the device's print and feed rates (relatively
            slow, being bound to moving parts and physical reality).  After
            an operation is issued to the printer (e.g. bitmap print), a
            timeout is set before which any other printer operations will be
            suspended.  This is generally more efficient than using a delay
            in that it allows the calling code to continue with other duties
            (e.g. receiving or decoding an image) while the printer
            physically completes the task.
        '''

        self.resume_time = time() + delay

    def timeout_wait(self):
        ''' Waits (if necessary) for the prior task to complete. '''

        while (time() - self.resume_time) < 0:
            pass

    def set_times(self, print_time, feed_time):
        ''' Printer performance may vary based on the power supply voltage,
            thickness of paper, phase of the moon and other seemingly random
            variables.  This method sets the times (in microseconds) for the
            paper to advance one vertical 'dot' when printing and feeding.

            For example, in the default initialized state, normal-sized text
            is 24 dots tall and the line spacing is 32 dots, so the time for
            one line to be issued is approximately 24 * print time + 8 * feed
            time.  The default print and feed times are based on a random
            test unit, but as stated above your reality may be influenced by
            many factors.  This lets you tweak the timing to avoid excessive
            delays and/or overrunning the printer buffer.

            Units are in microseconds.
        '''

        self.dot_print_time = print_time / 1000000.0
        self.dot_feed_time = feed_time / 1000000.0

    def write_bytes(self, *args):
        ''' 'Raw' byte-writing. '''

        self.timeout_wait()
        self.timeout_set(len(args) * self.byte_time)
        for data in args:
            data = convert_encoding(data, is_raw=True)
            super().write(data)

    def println(self, line):
        ''' Send a line to the printer. '''

        # enc = convert_encoding(line)
        # print(type(line), line, type(enc), enc)
        super().write(convert_encoding(line))
        super().write(b'\n')

    def reset(self):
        ''' Reset printer settings. '''

        self.prev_byte = '\n'  # Treat as if prior line is blank
        self.column = 0
        self.max_column = 32
        self.char_height = 24
        self.line_spacing = 6
        self.barcode_height = 50
        self.write_bytes(Command.ASCII_ESC.value, 64)
        # Configure tab stops on recent printers
        self.write_bytes(Command.ASCII_ESC.value, 'D')  # Set tab stops ...
        self.write_bytes(4, 8, 12, 16)  # ... every 4 columns,
        self.write_bytes(20, 24, 28, 0)  # 0 marks end-of-list.

    def set_default(self):
        ''' Reset text formatting parameters. '''

        self.online()
        self.justify('L')
        self.inverse_off()
        self.double_height_off()
        self.set_line_height(32)
        self.bold_off()
        self.underline_off()
        self.set_barcode_height(50)
        self.set_size('S')

    def test(self):
        ''' Print settings as test. '''

        self.write_bytes(Command.ASCII_DC2.value, 84)
        self.timeout_set(self.dot_print_time * 24 * 26 + self.dot_feed_time *
                         (8 * 26 + 32))

    def print_barcode(self, text, bc_type):
        ''' Barcode printing. '''

        if not 5 <= bc_type <= 10:
            print('Error: 5 <= bc_type <= 10.')
            return
        self.write_bytes(Command.ASCII_GS.value, 72, 2,  # Label below barcode
                         Command.ASCII_GS.value, 119, 3,  # Barcode width
                         Command.ASCII_GS.value, 107, bc_type)  # Barcode type
        # Print string
        self.timeout_set((self.barcode_height + 40) * self.dot_print_time)
        super().write(convert_encoding(text, is_raw=True, is_image=True))
        self.timeout_wait()
        self.prev_byte = '\n'
        self.feed(2)

    def set_barcode_height(self, val=50):
        ''' Set the barcode height. '''

        val = max(1, val)
        self.barcode_height = val
        self.write_bytes(Command.ASCII_GS.value, 104, val)

    def set_print_mode(self, mask):
        ''' Set the print mode. '''

        self.print_mode |= mask
        self.write_print_mode()
        if self.print_mode & 16:
            self.char_height = 48
        else:
            self.char_height = 24

    def unset_print_mode(self, mask):
        ''' Unset the print mode.  '''

        self.print_mode &= ~mask
        self.write_print_mode()
        if self.print_mode & 16:
            self.char_height = 48
        else:
            self.char_height = 24

    def write_print_mode(self):
        ''' Write the print mode. '''

        self.write_bytes(Command.ASCII_ESC.value, 33, self.print_mode)

    def normal(self):
        ''' Set the print mode to normal. '''

        self.print_mode = 0
        self.write_print_mode()

    def inverse_on(self):
        ''' Set inverse mode. '''

        self.write_bytes(Command.ASCII_GS.value, 'B', 1)

    def inverse_off(self):
        ''' Unset inverse mode. '''

        self.write_bytes(Command.ASCII_GS.value, 'B', 0)

    def double_height_on(self):
        ''' Set double height mode. '''

        self.set_print_mode(16)

    def double_height_off(self):
        ''' Unset double height mode. '''

        self.unset_print_mode(16)

    def double_width_on(self):
        ''' Set double width mode. '''

        self.max_column = 16
        self.write_bytes(Command.ASCII_ESC.value, 14, 1)

    def double_width_off(self):
        ''' Unset double width mode. '''

        self.max_column = 32
        self.write_bytes(Command.ASCII_ESC.value, 20, 1)

    def strike_on(self):
        ''' Set strike mode. '''

        self.write_bytes(Command.ASCII_ESC.value, 'G', 1)

    def strike_off(self):
        ''' Unset strike mode. '''

        self.write_bytes(Command.ASCII_ESC.value, 'G', 0)

    def bold_on(self):
        ''' Set bold mode. Actually can be also set using set_print_mode. '''

        self.write_bytes(Command.ASCII_ESC.value, 'E', 1)

    def bold_off(self):
        ''' Unset bold mode. '''

        self.write_bytes(Command.ASCII_ESC.value, 'E', 0)

    def justify(self, value='L'):
        ''' Set text justification. '''

        value = value.upper()
        pos = 0
        if value == 'C':
            pos = 1
        elif value == 'R':
            pos = 2
        self.write_bytes(Command.ASCII_ESC.value, 'a', pos)

    def feed(self, number=1):
        ''' Feeds by the specified number of lines. '''

        if self.fw_ver >= 270:  # Does not work with v2.69
            self.write_bytes(Command.ASCII_ESC.value, 'd', number)
            self.timeout_set(number * self.dot_feed_time * self.char_height)
            self.prev_byte = '\n'
            self.column = 0
        else:
            # Feed manually; old firmware feeds excess lines
            while number:
                super().write(b'\n')
                number -= 1

    def feed_rows(self, rows):
        ''' Feeds by the specified number of individual pixel rows
            WARN: does not work whith mine v2.69
        '''

        self.write_bytes(Command.ASCII_ESC.value, 74, rows)
        self.timeout_set(rows * self.dot_feed_time)

    def flush(self):
        ''' Flush. '''

        self.write_bytes(12)

    def set_size(self, value='S'):
        ''' Set text size. '''

        value = value.upper()
        size = 0x00
        self.char_height = 24
        self.max_column = 32
        if value == 'L':  # Large: double width and height
            size = 0x11
            self.char_height = 48
            self.max_column = 16
        elif value == 'M':  # Medium: double height
            size = 0x01
            self.char_height = 48
            self.max_column = 32

        self.write_bytes(Command.ASCII_GS.value, 33, size)
        self.prev_byte = '\n'  # Setting the size adds a linefeed

    def underline_on(self, weight=1):
        ''' Underlines of different weights can be produced:
            0 - no underline
            1 - normal underline
            2 - thick underline
        '''

        if not 0 <= weight <= 2:
            weight = 2
        self.write_bytes(Command.ASCII_ESC.value, '-', weight)

    def underline_off(self):
        ''' Unset underline mode. '''

        self.underline_on(0)

    def print_image(self, image):
        ''' Print Image. Requires Python Imaging Library. This is
            specific to the Python port and not present in the Arduino
            library. Image will be cropped to 384 pixels width if
            necessary, and converted to 1-bit w/diffusion dithering.
            For any other behavior (scale, B&W threshold, etc.), use
            the Imaging Library to perform such operations before
            passing the result to this function.

            Max width: 384px.

            Returns the number of printed lines.
        '''

        # pylint: disable=R0914

        if image.mode != '1':
            image = image.convert('1')

        width = min(image.size[0], 384)
        height = image.size[1]
        row_bytes = int((width + 7) / 8)
        row_bytes_clipped = 48 if row_bytes >= 48 else row_bytes
        bitmap = bytearray(row_bytes * height)
        pixels = image.load()

        for col in range(height):
            offset = col * row_bytes
            row = 0
            for pad in range(row_bytes):
                sum_ = 0
                bit = 128
                while bit > 0:
                    if row >= width:
                        break
                    if pixels[row, col] == 0:
                        sum_ |= bit
                    row += 1
                    bit >>= 1
                bitmap[offset + pad] = sum_

        idx = 0
        lines = 0
        for row_start in range(0, height, 255):
            chunk_height = min(height - row_start, 255)
            self.write_bytes(Command.ASCII_DC2.value, 42, chunk_height,
                             row_bytes_clipped)
            for _ in range(chunk_height):
                for _ in range(row_bytes_clipped):
                    super().write(convert_encoding(bitmap[idx],
                                                   is_raw=True,
                                                   is_image=True))
                    lines += 1
                    idx += 1
                idx += row_bytes - row_bytes_clipped
        self.prev_byte = '\n'
        return lines

    def offline(self):
        ''' Take the printer offline. Print commands sent after this
            will be ignored until 'online' is called.
        '''

        self.write_bytes(Command.ASCII_ESC.value, 61, 0)

    def online(self):
        ''' Take the printer online.
            Subsequent print commands will be obeyed.
        '''

        self.write_bytes(Command.ASCII_ESC.value, 61, 1)

    def sleep(self, seconds=1):
        ''' Put the printer into a low-energy state. '''

        if seconds > 0:
            sleep(seconds)
        self.write_bytes(Command.ASCII_ESC.value, '8', seconds, seconds >> 8)

    def wake(self):
        ''' Wake up the printer. '''

        self.timeout_set(0)
        self.write_bytes(255)
        sleep(0.05)  # Sleep 50ms as in documentation
        self.sleep(0)  # SLEEP OFF - IMPORTANT!

    def has_paper(self):
        ''' Check the status of the paper using the printers self reporting
            ability. Doesn't match the datasheet...
            Returns True for paper, False for no paper.
        '''

        self.write_bytes(Command.ASCII_ESC.value, 118, 0)
        # Bit 2 of response seems to be paper status
        try:
            stat = ord(self.read(1)) & 0b00000100
        except TypeError:
            return True
        # If set, we have paper; if clear, no paper
        return stat == 0

    def set_line_height(self, val=32):
        ''' Set line height.

            The printer doesn't take into account the current text
            height when setting line height, making this more akin
            to inter-line spacing. Default line spacing is 30
            (char height of 24, line spacing of 6).
        '''

        val = max(24, val)
        self.line_spacing = val - 24
        self.write_bytes(Command.ASCII_ESC.value, '3', val)

    def tab(self):
        ''' Tabulation. '''

        super().write(b'\t')
        self.column = (self.column + 4) % self.max_column

    def set_char_spacing(self, spacing):
        ''' Set character spacing. '''

        self.write_bytes(Command.ASCII_ESC.value, ' ', spacing)


def tests():
    ''' Tests. '''

    from PIL import Image

    printer = ThermalPrinter()

    # printer.test()

    printer.feed()
    printer.print_image(Image.open('gnu.png'))
    printer.feed()

    printer.bold_on()
    printer.println('Bold')
    printer.bold_off()

    printer.double_height_on()
    printer.println('Double height')
    printer.double_height_off()

    printer.double_width_on()
    printer.println('Double width')
    printer.double_width_off()

    printer.inverse_on()
    printer.println('Inverse')
    printer.inverse_off()

    printer.strike_on()
    printer.println('Strike')
    printer.strike_off()

    printer.tab()
    printer.println('Tabulation')

    printer.underline_on()
    printer.println('Underline')
    printer.underline_off()

    printer.println('A boolean centered:')
    printer.justify('C')
    printer.println(True)

    printer.justify('L')
    printer.println('An integer on the right:')
    printer.justify('R')
    printer.println(42)

    printer.justify('L')
    printer.print_barcode('0123456789', BarCode.I25.value)

    return 0


if __name__ == '__main__':
    exit(tests())

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

__all__ = ['BarCode', 'CharSet', 'Command', 'CodePage', 'ThermalPrinter']


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


class BarCode(Enum):
    ''' Available barcode types.
        (code, (min len(text), max len(text)))
    '''

    UPC_A = (65, (11, 12))
    UPC_E = (66, (11, 12))
    JAN13 = (67, (12, 13))
    EAN13 = (67, (12, 13))
    JAN8 = (68, (7, 8))
    EAN8 = (68, (7, 8))
    CODE39 = (69, (1, 255))
    ITF = (70, (1, 255))
    CODABAR = (71, (1, 255))
    CODE93 = (72, (1, 255))
    CODE128 = (73, (2, 255))


class CharSet(Enum):
    ''' Internal character sets. '''

    USA = 0
    FRANCE = 1
    GERMANY = 2
    UK = 3
    DENMARK = 4
    SWEDEN = 5
    ITALY = 6
    SPAIN = 7
    JAPAN = 8
    NORWAY = 9
    DENMARK2 = 10
    SPAIN2 = 11
    LATIN_AMERICAN = 12
    KOREA = 13
    SLOVENIA = 14
    CHINA = 15


class CodePage(Enum):
    ''' Character Code Tables.
        (code, description)
    '''

    CP437 = (0, 'the United States of America, European standard')
    KATAKANA = (1, 'Katakana')
    CP850 = (2, 'Multi language')
    CP860 = (3, 'Portuguese')
    CP863 = (4, 'Canada, French')
    CP865 = (5, 'Western Europe')
    CYRILLIC = (6, 'The Slavic language')
    WCP1251 = (6, 'The Slavic language')
    CP866 = (7, 'The Slavic 2')
    MIK = (8, 'The Slavic / Bulgaria')
    CP755 = (9, 'Eastern Europe, Latvia 2')
    IRAN = (10, 'Iran, Persia')
    CP862 = (15, 'Hebrew')
    WCP1252 = (16, 'Latin 1')
    WCP1253 = (17, 'Greece')
    CP852 = (18, 'Latina 2')
    CP858 = (19, 'A variety of language Latin 1 + Europe')
    IRAN2 = (20, 'Persian')
    LATVIA = (21, '')
    CP864 = (22, 'Arabic')
    ISO_8859_1 = (23, 'Western Europe')
    CP737 = (24, 'Greece')
    WCP1257 = (25, 'The Baltic Sea')
    THAI = (26, 'Thai Wen')
    CP720 = (27, 'Arabic')
    CP855 = (28, '')
    CP857 = (29, 'Turkish')
    WCP1250 = (30, 'Central Europe')
    CP775 = (31, '')
    WCP1254 = (32, 'Turkish')
    WCP1255 = (33, 'Hebrew')
    WCP1256 = (34, 'Arabic')
    WCP1258 = (35, 'Vietnamese')
    ISO_8859_2 = (36, 'Latin 2')
    ISO_8859_3 = (37, 'Latin 3')
    ISO_8859_4 = (38, 'Baltic languages')
    ISO_8859_5 = (39, 'The Slavic language')
    ISO_8859_6 = (40, 'Arabic')
    ISO_8859_7 = (41, 'Greece')
    ISO_8859_8 = (42, 'Hebrew')
    ISO_8859_9 = (43, 'Turkish')
    ISO_8859_15 = (44, 'Latin 9')
    THAI2 = (45, 'Thai Wen 2')
    CP856 = (46, '')
    CP874 = (47, '')


class Command(Enum):
    ''' Codes used to send commands. '''

    DC2 = 18
    ESC = 27
    FS = 28
    GS = 29


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

    def barcode(self, text, bc_type):
        ''' Barcode printing. '''

        if not isinstance(bc_type, BarCode):
            bcodes = ', '.join([barcode.name for barcode in BarCode])
            raise ValueError('Valid barcodes are: {}.'.format(bcodes))

        code, (min_, max_) = bc_type.value
        if not min_ <= len(text) <= max_:
            err = 'Should be {} <= len(text) <= {}.'.format(min_, max_)
            raise ValueError(err)
        elif bc_type is BarCode.ITF and not even(len(text)):
            raise ValueError('len(text) must be even.')

        self._write_bytes(
            Command.GS, 72, 2,  # Label below barcode
            Command.GS, 107, code, len(text), text)
        self._timeout_wait()
        self._timeout_set((self.barcode_height + 40) * self.dot_print_time)
        self.prev_byte = '\n'

    def bold(self, state=1):
        ''' Turn emphasized mode on/off. '''

        if state != 1:
            state = 0
        self._write_bytes(Command.ESC, 69, state)

    def double_height(self, state=1):
        ''' Set double height mode. '''

        if state == 1:
            self._set_print_mode(16)
        else:
            self._unset_print_mode(16)

    def double_width(self, state=1):
        ''' Select Double Width mode. '''

        if state == 1:
            self.max_column = 16
            self._write_bytes(Command.ESC, 14, 1)
        else:
            self.max_column = 32
            self._write_bytes(Command.ESC, 20, 1)

    def feed(self, number=1):
        ''' Feeds by the specified number of lines. '''

        if not 0 <= number <= 255:
            number = 0
        self._write_bytes(Command.ESC, 100, number)
        self._timeout_set(number * self.dot_feed_time * self.char_height)
        self.prev_byte = '\n'
        self.column = 0

    def flush(self):
        ''' Flush. '''

        self._write_bytes(12)

    def has_paper(self):
        ''' Check the status of the paper using the printers self reporting
            ability. Doesn't match the datasheet...
            Returns True for paper, False for no paper.
        '''

        self._write_bytes(Command.ESC, 118, 0)
        # Bit 2 of response is paper status
        try:
            stat = ord(self.read(1)) & 0b00000100
        except TypeError:
            return True
        # If set, we have paper; if clear, no paper
        return stat == 0

    def image(self, image):
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
            self._write_bytes(Command.DC2, 42, chunk_height,
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

    def inverse(self, state=1):
        ''' Turn white/black reverse printing mode. '''

        if state != 1:
            state = 0
        self._write_bytes(Command.GS, 66, state)

    def is_pinned(self):
        ''' TODO FIX. Transmit peripheral devices status. '''

        self._write_bytes(Command.ESC, 117, 0)
        # Bit 1 of response is drawer kick out connector pin 3
        try:
            stat = ord(self.read(1)) & 0b00000001
        except TypeError:
            return True
        # If set, we have paper; if clear, no paper
        return stat == 0

    def justify(self, value='L'):
        ''' Set text justification. '''

        value = value.upper()
        if value == 'C':
            pos = 1
        elif value == 'R':
            pos = 2
        else:
            pos = 0
        self._write_bytes(Command.ESC, 97, pos)

    def println(self, line):
        ''' Send a line to the printer. '''

        super().write(convert_encoding(line))
        super().write(b'\n')

    def offline(self):
        ''' Take the printer offline. Print commands sent after this
            will be ignored until 'online' is called.
        '''

        self._write_bytes(Command.ESC, 61, 0)

    def online(self):
        ''' Take the printer online.
            Subsequent print commands will be obeyed.
        '''

        self._write_bytes(Command.ESC, 61, 1)

    def reset(self):
        ''' Reset printer settings. '''

        self.prev_byte = '\n'
        self.column = 0
        self.max_column = 32
        self.char_height = 24
        self.line_spacing = 6
        self.barcode_height = 50
        self._write_bytes(Command.ESC, 64)
        self._write_bytes(Command.ESC, 68, 9, 17, 25, 33, 0)  # Tabulations

    def rotate(self, state=1):
        ''' Turn on/off clockwise rotation of 90°. '''

        if state != 1:
            state = 0
        self._write_bytes(Command.ESC, 86, state)

    def set_barcode_height(self, val=50):
        ''' Set bar code height. '''

        val = min(max(1, val), 255)
        self.barcode_height = val
        self._write_bytes(Command.GS, 104, val)

    def set_charset(self, charset):
        ''' Select an internal character set. '''

        if not isinstance(charset, CharSet):
            err = 'Valid charsets are: {}.'.format(
                ', '.join([cset.name for cset in CharSet]))
            raise ValueError(err)

        self._write_bytes(Command.ESC, 82, charset.value)

    def set_codepage(self, codepage):
        ''' Select character code table. '''

        if not isinstance(codepage, CodePage):
            codes = ''
            last = list(CodePage)[-1]
            for cpage in CodePage:
                sep = '.' if cpage is last else ', '
                _, name = cpage.value
                if name:
                    codes += '{} ({}){}'.format(cpage.name, name, sep)
                else:
                    codes += '{}{}'.format(cpage.name, sep)
            raise ValueError('Valid codepages are: {}'.format(codes))

        value, _ = codepage.value
        self._write_bytes(Command.ESC, 116, value)

    def set_default(self):
        ''' Reset text formatting parameters. '''

        self.online()
        self.justify('L')
        self.inverse(0)
        self.double_height(0)
        self.set_line_height(32)
        self.bold(0)
        self.underline(0)
        self.set_barcode_height(50)
        self.set_size('S')

    def set_char_spacing(self, spacing=0):
        ''' Set the right character spacing. '''

        if not 0 <= spacing <= 255:
            spacing = 0
        self._write_bytes(Command.ESC, 32, spacing)

    def set_left_spacing(self, spacing=0):
        ''' Set the left spacing. '''

        if not 0 <= spacing <= 47:
            spacing = 0
        self._write_bytes(Command.ESC, 66, spacing)

    def set_line_height(self, val=32):
        ''' Set line height.

            The printer doesn't take into account the current text
            height when setting line height, making this more akin
            to inter-line spacing. Default line spacing is 30
            (char height of 24, line spacing of 6).
        '''

        val = max(24, val)
        self.line_spacing = val - 24
        self._write_bytes(Command.ESC, '3', val)

    def set_line_spacing(self, spacing=30):
        ''' Set line spacing. '''

        if not 0 <= spacing <= 255:
            spacing = 30
        self._write_bytes(Command.ESC, 51, spacing)

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

        self._write_bytes(Command.GS, 33, size)
        self.prev_byte = '\n'  # Setting the size adds a linefeed

    def sleep(self, seconds=1):
        ''' Put the printer into a low-energy state. '''

        if seconds > 0:
            sleep(seconds)
        self._write_bytes(Command.ESC, '8', seconds, seconds >> 8)

    def strike(self, state=1):
        ''' Turn on/off double-strike mode. '''

        if state != 1:
            state = 0
        self._write_bytes(Command.ESC, 71, state)

    def tab(self):
        ''' Tabulation. '''

        super().write(b'\t')
        self.column = (self.column + 4) % self.max_column

    def test(self):
        ''' Print settings as test. '''

        self._write_bytes(Command.DC2, 84)
        self._timeout_set(self.dot_print_time * 24 * 26 + self.dot_feed_time *
                         (8 * 26 + 32))

    def underline(self, weight=1):
        ''' Turn underline mode on/off.
            0: turns off underline mode
            1: turns on underline mode (1 dot thick)
            2: turns on underline mode (2 dots thick)
        '''

        if not 0 < weight <= 2:
            weight = 0
        self._write_bytes(Command.ESC, 45, weight)

    def upside_down(self, state=1):
        ''' Turns on/off upside-down printing mode. '''

        if state != 1:
            state = 0
        self._write_bytes(Command.ESC, 123, state)

    def wake(self):
        ''' Wake up the printer. '''

        self._timeout_set(0)
        self._write_bytes(255)
        sleep(0.05)  # Sleep 50ms as in documentation
        self.sleep(0)  # SLEEP OFF - IMPORTANT!

    # Private methods

    def _set_print_mode(self, mask):
        ''' Set the print mode. '''

        self.print_mode |= mask
        self._write_print_mode()
        if self.print_mode & 16:
            self.char_height = 48
        else:
            self.char_height = 24

    def _timeout_set(self, delay):
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

    def _timeout_wait(self):
        ''' Waits (if necessary) for the prior task to complete. '''

        while (time() - self.resume_time) < 0:
            pass

    def _unset_print_mode(self, mask):
        ''' Unset the print mode.  '''

        self.print_mode &= ~mask
        self._write_print_mode()
        if self.print_mode & 16:
            self.char_height = 48
        else:
            self.char_height = 24

    def _write_bytes(self, *args):
        ''' 'Raw' byte-writing. '''

        self._timeout_wait()
        self._timeout_set(len(args) * self.byte_time)
        for data in args:
            if isinstance(data, Command):
                data = data.value
            super().write(convert_encoding(data, is_raw=True))

    def _write_print_mode(self):
        ''' Write the print mode. '''

        self._write_bytes(Command.ESC, 33, self.print_mode)


def tests():
    ''' Tests. '''

    from PIL import Image

    printer = ThermalPrinter()

    # printer.test()

    printer.feed()
    printer.image(Image.open('gnu.png'))
    printer.feed()

    printer.bold()
    printer.println('Bold')
    printer.bold(0)

    printer.double_height()
    printer.println('Double height')
    printer.double_height(0)

    printer.double_width()
    printer.println('Double width')
    printer.double_width(0)

    printer.inverse()
    printer.println('Inverse')
    printer.inverse(0)

    printer.rotate()
    printer.println('Rotate 90°')
    printer.rotate(0)

    printer.strike()
    printer.println('Strike')
    printer.strike(0)

    printer.tab()
    printer.println('Tabulation')

    printer.underline()
    printer.println('Underline')
    printer.underline(0)

    printer.upside_down()
    printer.println('Upside down')
    printer.upside_down(0)

    printer.println('A boolean centered:')
    printer.justify('C')
    printer.println(True)

    printer.justify('L')
    printer.println('An integer on the right:')
    printer.justify('R')
    printer.println(42)

    printer.justify('L')
    printer.barcode('012345678901', BarCode.EAN13)

    printer.println("Voilà, c'est terminé !")
    printer.feed(2)
    return 0


if __name__ == '__main__':
    exit(tests())

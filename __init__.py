#!/usr/bin/env python
# coding: utf-8
''' Python module to manage the DP-EH600 thermal printer.

    This module is maintained by Mickaël Schoentgen <mickael@jmsinfo.co>.
    Based on the work of Phil Burgess and Fried/Ladyada (Adafruit).

    Python 3+ only.
    Dependencies:
        pyserial
        cchardet

    usermod -G dialout -a $USER

    You can always get the latest version of this module at:
        https://github.com/BoboTiG/thermalprinter
    If that URL should fail, try contacting the author.
'''

from enum import Enum
from time import sleep, time

from cchardet import detect
from serial import Serial

__all__ = ['BarCode', 'BarCodePosition', 'CharSet', 'Command', 'CodePage',
           'ThermalPrinter']


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
    ''' Available bar code types.
        (code, (min len(text), max len(text)), allowed_chars)
    '''

    UPC_A = (65, (11, 12), 0)
    UPC_E = (66, (11, 12), 0)
    JAN13 = (67, (12, 13), 0)
    EAN13 = (67, (12, 13), 0)
    JAN8 = (68, (7, 8), 0)
    EAN8 = (68, (7, 8), 0)
    CODE39 = (69, (1, 255), 1)
    ITF = (70, (1, 255), 0)
    CODABAR = (71, (1, 255), 2)
    CODE93 = (72, (1, 255), 3)
    CODE128 = (73, (2, 255), 3)


class BarCodePosition(Enum):
    ''' Available bar code positions.
        (code, explication)
    '''

    HIDDEN = 0
    ABOVE = 1
    BELOW = 2
    BOTH = 3


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

    max_column = 32

    def __init__(self, port='/dev/ttyAMA0', baudrate=19200):
        ''' Print init. '''

        self._baudrate = baudrate
        super().__init__(port=port, baudrate=self._baudrate)
        sleep(0.5)
        self.reset(start=True)
        self.set_defaults()

    def __enter__(self):
        ''' `with ThermalPrinter() as printer:` '''

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        ''' `with ThermalPrinter() as printer:` '''

        self.close()

    def barcode(self, data, bc_type):
        ''' Bar code printing. '''

        def _range1(a=48, b=57):
            return [n for n in range(a, b + 1)]

        def _range2():
            range_ = [32, 36, 37, 43]
            range_.extend(_range1(45, 57))
            range_.extend(_range1(65, 90))
            return range_

        def _range3():
            range_ = [36, 43]
            range_.extend(_range1(45, 58))
            range_.extend(_range1(65, 68))
            return range_

        def _range4():
            return _range1(0, 127)

        ranges_ = [_range1, _range2, _range3, _range4]

        if not isinstance(bc_type, BarCode):
            err = ', '.join([barcode.name for barcode in BarCode])
            raise ValueError('Valid bar codes are: {}.'.format(err))

        code, (min_, max_), range_type = bc_type.value
        data_len = len(data)
        range_ = ranges_[range_type]()

        if not min_ <= data_len <= max_:
            err = '[{}] Should be {} <= len(data) <= {} (current: {}).'.format(
                bc_type.name, min_, max_, data_len)
            raise ValueError(err)
        elif bc_type is BarCode.ITF and data_len % 2 != 0:
            raise ValueError('[ITF] len(data) must be even.')

        if not all(ord(char) in range_ for char in data):
            if range_type != 3:
                valid = map(chr, range_)
            else:
                valid = map(hex, range_)
            err = '[{}] Valid characters: {}.'.format(
                bc_type.name, ', '.join(valid))
            raise ValueError(err)

        self._write_bytes(Command.GS, 107, code, data_len, data)
        self._timeout_wait()
        self._timeout_set((self._barcode_height + self._line_spacing) * self._dot_print_time)
        self.prev_byte = '\n'

    def bold(self, state=True):
        ''' Turn emphasized mode on/off. '''

        state = bool(state)
        if state is not self._bold:
            self._bold = state
            self._write_bytes(Command.ESC, 69, int(state))

    def double_height(self, state=True):
        ''' Set double height mode. '''

        state = bool(state)
        if state is not self._double_height:
            self._double_height = state
            self._set_print_mode(16) if state else self._unset_print_mode(16)

    def double_width(self, state=True):
        ''' Select Double Width mode. '''

        state = bool(state)
        if state is not self._double_width:
            self._double_width = state
            if state:
                self.max_column = 16
            else:
                self.max_column = 32
            self._write_bytes(Command.ESC, 14 if state else 20, 1)

    def feed(self, number=1):
        ''' Feeds by the specified number of lines. '''

        if not 0 <= number <= 255:
            return

        self._write_bytes(Command.ESC, 100, number)
        self._timeout_set(number * self._dot_feed_time * self._char_height)
        self._prev_byte = '\n'
        self._column = 0

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
                    self.write(convert_encoding(bitmap[idx],
                                                is_raw=True,
                                                is_image=True))
                    lines += 1
                    idx += 1
                idx += row_bytes - row_bytes_clipped
        self._prev_byte = '\n'
        return lines

    def inverse(self, state=True):
        ''' Turn white/black reverse printing mode. '''

        state = bool(state)
        if state is not self._inverse:
            self._inverse = state
            self._write_bytes(Command.GS, 66, int(state))

    def justify(self, value='L'):
        ''' Set text justification. '''

        value = value.upper()
        if value != self._justify:
            self._justify = value
            if value == 'C':
                pos = 1
            elif value == 'R':
                pos = 2
            else:
                pos = 0
            self._write_bytes(Command.ESC, 97, pos)

    def println(self, line):
        ''' Send a line to the printer. '''

        if line:
            self.write(convert_encoding(line))
            self.write(b'\n')

    def offline(self):
        ''' Take the printer offline. Print commands sent after this
            will be ignored until 'online' is called.
        '''

        if self._is_online:
            self._is_online = False
            self._write_bytes(Command.ESC, 61, 0)

    def online(self):
        ''' Take the printer online.
            Subsequent print commands will be obeyed.
        '''

        if not self._is_online:
            self._is_online = True
            self._write_bytes(Command.ESC, 61, 1)

    def reset(self, start=False):
        ''' Reset printer settings. '''

        # Reset vars
        self._byte_time = 11.0 / float(self._baudrate)
        self._dot_feed_time = 0.0025
        self._dot_print_time = 0.033
        self._resume_time = 0.0

        self.max_column = 32
        self._barcode_height = 0
        self._barcode_left_margin = 0
        self._barcode_position = None
        self._barcode_width = 0
        self._bold = None
        self._charset = None
        self._char_spacing = 0
        self._char_height = 24
        self._codepage = None
        self._column = 0
        self._double_height = None
        self._double_width = None
        self._inverse = None
        self._is_online = True
        self._is_sleeping = False
        self._justify = ''
        self._left_margin = 0
        self._line_spacing = 0
        self._prev_byte = '\n'
        self._print_mode = 0
        self._rotate = None
        self._size = ''
        self._strike = None
        self._underline = -1
        self._upside_down = None

        # Reset command does not clear the receive buffer, so we do it manually
        self.reset_input_buffer()
        self.reset_output_buffer()
        if not start:
            self._write_bytes(Command.ESC, 64)  # Reset

        # Reset print parameters
        self._write_bytes(Command.ESC, 55,
                          3,    # The most heated pojnt (default: 9)
                          80,   # Heat time (default: 80)
                          12)   # Heat time interval (default: 2)

    def rotate(self, state=True):
        ''' Turn on/off clockwise rotation of 90°. '''

        state = bool(state)
        if state is not self._rotate:
            self._rotate = state
            self._write_bytes(Command.ESC, 86, int(state))

    def set_barcode_height(self, val=80):
        ''' Set bar code height. '''

        if not 1 <= val <= 255:
            val = 80

        if val != self._barcode_height:
            self._barcode_height = val
            self._write_bytes(Command.GS, 104, val)

    def set_barcode_left_margin(self, val=0):
        ''' Set the bar code printed on the left spacing. '''

        if not 0 <= val <= 255:
            val = 0

        if val != self._barcode_left_margin:
            barcode_left_margin = val
            self._write_bytes(Command.GS, 120, val)

    def set_barcode_position(self, bc_pos=BarCodePosition.BELOW):
        ''' Set bar code position. '''

        if not isinstance(bc_pos, BarCodePosition):
            err = ', '.join([pos.name for pos in BarCodePosition])
            raise ValueError('Valid positions are: {}.'.format(err))

        if bc_pos is not self._barcode_position:
            self._barcode_position = bc_pos
            self._write_bytes(Command.GS, 72, bc_pos.value)

    def set_barcode_width(self, width=2):
        ''' Set bar code width. '''

        if not 2 <= width <= 6:
            width = 2

        if width != self._barcode_width:
            self._barcode_width = width
            self._write_bytes(Command.GS, 119, width)

    def set_charset(self, charset):
        ''' Select an internal character set. '''

        if not isinstance(charset, CharSet):
            err = 'Valid charsets are: {}.'.format(
                ', '.join([cset.name for cset in CharSet]))
            raise ValueError(err)

        if charset is not self._charset:
            self._charset = charset
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

        if codepage is not self._codepage:
            self._codepage = codepage
            value, _ = codepage.value
            self._write_bytes(Command.ESC, 116, value)

    def set_defaults(self):
        ''' Reset formatting parameters. '''

        self.online()
        self.bold(False)
        self.double_height(False)
        self.inverse(False)
        self.justify()
        self.rotate(False)
        self.set_char_spacing()
        self.set_line_spacing()
        self.set_left_margin()
        self.set_size()
        self.strike(False)
        self.underline(False)
        self.upside_down(False)

    def set_char_spacing(self, spacing=0):
        ''' Set the right character spacing. '''

        if not 0 <= spacing <= 255:
            spacing = 0

        if spacing != self._char_spacing:
            self._char_spacing = spacing
            self._write_bytes(Command.ESC, 32, spacing)

    def set_left_margin(self, spacing=0):
        ''' Set the left margin. '''

        if not 0 <= spacing <= 47:
            spacing = 0

        if spacing != self._left_margin:
            self._left_margin = spacing
            self._write_bytes(Command.ESC, 66, spacing)

    def set_line_spacing(self, spacing=30):
        ''' Set line spacing. '''

        if not 0 <= spacing <= 255:
            spacing = 30

        if spacing != self._line_spacing:
            self._line_spacing = spacing
            self._write_bytes(Command.ESC, 51, spacing)

    def set_size(self, value='S'):
        ''' Set text size. '''

        value = value.upper()
        if value != self._size:
            self._size = value
            if value == 'L':    # Large: double width and height
                size, self._char_height, self.max_column = 0x11, 48, 16
            elif value == 'M':  # Medium: double height
                size, self._char_height, self.max_column = 0x01, 48, 32
            else:
                size, self._char_height, self.max_column = 0x00, 24, 32

            self._write_bytes(Command.GS, 33, size)
            self._prev_byte = '\n'

    def sleep(self, seconds=1):
        ''' Put the printer into a low-energy state. '''

        if not self._is_sleeping:
            self._is_sleeping = True
            if seconds > 0:
                sleep(seconds)

            self._write_bytes(Command.ESC, 56, seconds, seconds >> 8)

    def status(self):
        ''' Check the printer status. If RX pin is not connected, all values
            will be set to True.

            Return a dict:
                movement: False if the movement is not connected.
                   paper: False is no paper.
                    temp: False if the temperature exceeds 60°C.
                 voltage: False if the voltage is higher than 9.5V
        '''

        ret = { 'movement': True, 'paper': True,
                'temp': True, 'voltage': True }
        self._write_bytes(Command.ESC, 118, 0)
        sleep(0.05)
        if self.in_waiting:
            stat = ord(self.read(1))
            ret['movement'] = stat & 0b00000001 == 1
            ret['paper'] = stat & 0b00000100 == 0
            ret['voltage'] = stat & 0b00001000 == 0
            ret['temp'] = stat & 0b01000000 == 0
        return ret

    def strike(self, state=True):
        ''' Turn on/off double-strike mode. '''

        state = bool(state)
        if state is not self._strike:
            self._strike = state
            self._write_bytes(Command.ESC, 71, int(state))

    def test(self):
        ''' Print settings as test. '''

        self._write_bytes(Command.DC2, 84)
        self._timeout_set(self._dot_print_time * 24 * 26 +
                          self._dot_feed_time * (8 * 26 + 32))

    def underline(self, weight=1):
        ''' Turn underline mode on/off.
            0: turns off underline mode
            1: turns on underline mode (1 dot thick)
            2: turns on underline mode (2 dots thick)
        '''

        if not 0 <= weight <= 2:
            weight = 0

        if weight != self._underline:
            self._underline = weight
            self._write_bytes(Command.ESC, 45, weight)

    def upside_down(self, state=True):
        ''' Turns on/off upside-down printing mode. '''

        state = bool(state)
        if state is not self._upside_down:
            self._upside_down = state
            self._write_bytes(Command.ESC, 123, int(state))

    def wake(self):
        ''' Wake up the printer. '''

        if self._is_sleeping:
            self._is_sleeping = False
            self._timeout_set(0)
            self._write_bytes(255)
            sleep(0.05)    # Sleep 50ms as in documentation
            self.sleep(0)  # SLEEP OFF - IMPORTANT!

    # Private methods

    def _set_print_mode(self, mask):
        ''' Set the print mode. '''

        self._print_mode |= mask
        self._write_print_mode()
        self._char_height = 48 if self._print_mode & 16 else 24
        self.max_column = 16 if self._print_mode & 32 else 32

    def _timeout_set(self, delay):
        ''' Sets estimated completion time for a just-issued task. '''

        self._resume_time = time() + delay

    def _timeout_wait(self):
        ''' Waits (if necessary) for the prior task to complete. '''

        while (time() - self._resume_time) < 0:
            pass

    def _unset_print_mode(self, mask):
        ''' Unset the print mode.  '''

        self._print_mode &= ~mask
        self._write_print_mode()
        self._char_height = 48 if self._print_mode & 16 else 24
        self.max_column = 16 if self._print_mode & 32 else 32

    def _write_bytes(self, *args):
        ''' 'Raw' byte-writing. '''

        self._timeout_wait()
        self._timeout_set(len(args) * self._byte_time)
        for data in args:
            if isinstance(data, Command):
                data = data.value
            self.write(convert_encoding(data, is_raw=True))

    def _write_print_mode(self):
        ''' Write the print mode. '''

        self._write_bytes(Command.ESC, 33, self._print_mode)


def tests():
    ''' Tests. '''

    with ThermalPrinter() as printer:
        try:
            from PIL import Image
            printer.feed()
            printer.image(Image.open('gnu.png'))
            printer.feed()
        except ImportError:
            pass

        printer.set_barcode_height(80)
        printer.set_barcode_position(BarCodePosition.BELOW)
        printer.set_barcode_width(3)
        printer.barcode('012345678901', BarCode.EAN13)

        printer.bold()
        printer.println('Bold')
        printer.bold(False)

        printer.double_height()
        printer.println('Double height')
        printer.double_height(False)

        printer.double_width()
        printer.println('Double width')
        printer.double_width(False)

        printer.inverse()
        printer.println('Inverse')
        printer.inverse(False)

        printer.rotate()
        printer.println('Rotate 90°')
        printer.rotate(False)

        printer.strike()
        printer.println('Strike')
        printer.strike(False)

        printer.underline()
        printer.println('Underline')
        printer.underline(False)

        printer.upside_down()
        printer.println('Upside down')
        printer.upside_down(False)

        printer.underline(2)
        printer.println('{0:{1}>{2}}'.format(' ', ' ', printer.max_column))
        printer.underline(0)

        printer.println('A boolean centered:')
        printer.justify('C')
        printer.println(True)

        printer.justify('L')
        printer.println('An integer on the right:')
        printer.justify('R')
        printer.println(42)

        printer.feed()
        printer.justify('C')
        printer.println("Voilà !")
        printer.feed(3)

        return 0

    return 1


if __name__ == '__main__':
    exit(tests())

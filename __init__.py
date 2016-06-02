#!/usr/bin/env python
# coding: utf-8
''' Python module to manage the DP-EH600 thermal printer.

    This module is maintained by Mickaël Schoentgen <mickael@jmsinfo.co>.
    Based on the work of Phil Burgess and Fried/Ladyada (Adafruit).

    Python 3+ only.
    Dependencies:
        pyserial

    usermod -G dialout -a $USER

    You can always get the latest version of this module at:
        https://github.com/BoboTiG/thermalprinter
    If that URL should fail, try contacting the author.
'''

from atexit import register
from configparser import SafeConfigParser
from enum import Enum
from time import sleep

from serial import Serial

__all__ = ['BarCode', 'BarCodePosition', 'CharSet', 'Chinese', 'Command',
           'CodePage', 'ThermalPrinter', 'ThermalPrinterError']


__version__ = '0.0.2'
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

    # pylint: disable=invalid-name

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


class Chinese(Enum):
    ''' Chinese formats. '''

    GBK = 0
    UTF_8 = 1
    BIG5 = 3


class CodePage(Enum):
    ''' Character Code Tables.
        (code, description)
    '''

    CP437 = (0, 'the United States of America, European standard')
    CP932 = (1, 'Katakana')
    CP850 = (2, 'Multi language')
    CP860 = (3, 'Portuguese')
    CP863 = (4, 'Canada, French')
    CP865 = (5, 'Western Europe')
    CYRILLIC = (6, 'The Slavic language')
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

    # pylint: disable=invalid-name

    DC2 = 18
    ESC = 27
    FS = 28
    GS = 29


class ThermalPrinter(Serial):
    ''' I talk to printers. Easy! '''

    # pylint: disable=too-many-ancestors
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-public-methods
    # pylint: disable=too-many-locals

    max_column = 32
    fo_stats = None

    def __init__(self, port='/dev/ttyAMA0', baudrate=19200):
        ''' Print init. '''

        register(self._on_exit)
        self._baudrate = baudrate
        self._byte_time = 11.0 / float(self._baudrate)
        self._dot_feed_time = 0.0025
        self._dot_print_time = 0.033

        self._lines = 0
        self._feeds = 0

        self._barcode_height = 0
        self._barcode_left_margin = 0
        self._barcode_position = None
        self._barcode_width = 0
        self._bold = None
        self._charset = None
        self._char_spacing = 0
        self._char_height = 24
        self._chinese = None
        self._chinese_format = None
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
        self._prev_byte = ''
        self._print_mode = 0
        self._rotate = None
        self._size = ''
        self._strike = None
        self._underline = -1
        self._upside_down = None

        super().__init__(port=port, baudrate=self._baudrate)
        sleep(0.5)  # Important

        # Printer settings
        self._write_bytes(Command.ESC, 55,
                          3,    # The most heated point (0..255, default: 9)
                          80,   # Heat time (0..255, default: 80)
                          12)   # Heat time interval (0..255, default: 2)

        self.set_defaults()

    def __enter__(self):
        ''' `with ThermalPrinter() as printer:` '''

        return self

    def _on_exit(self):
        ''' To be sure we keep stats and cleanup. '''

        self._update_stats()
        self.close()

    def barcode(self, data, bc_type):
        ''' Bar code printing. '''

        # pylint: disable=bad-builtin

        def _range1(min_=48, max_=57):
            return [n for n in range(min_, max_ + 1)]

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
            raise ThermalPrinterError('Valid bar codes are: {}.'.format(err))

        code, (min_, max_), range_type = bc_type.value
        data_len = len(data)
        range_ = ranges_[range_type]()

        if not min_ <= data_len <= max_:
            err = '[{}] Should be {} <= len(data) <= {} (current: {}).'.format(
                bc_type.name, min_, max_, data_len)
            raise ThermalPrinterError(err)
        elif bc_type is BarCode.ITF and data_len % 2 != 0:
            raise ThermalPrinterError('[BarCode.ITF] len(data) must be even.')

        if not all(ord(char) in range_ for char in data):
            if range_type != 3:
                valid = map(chr, range_)
            else:
                valid = map(hex, range_)
            err = '[{}] Valid characters: {}.'.format(
                bc_type.name, ', '.join(valid))
            raise ThermalPrinterError(err)

        self._write_bytes(Command.GS, 107, code, data_len)
        for char in list(data):
            char = bytes([ord(char)])
            self.write(char)
        sleep(
            (self._barcode_height + self._line_spacing) * self._dot_print_time)
        self._prev_byte = '\n'
        self._lines += int(self._barcode_height / self._line_spacing) + 1

    def barcode_height(self, val=80):
        ''' Set bar code height. '''

        if not 1 <= val <= 255:
            val = 80

        if val != self._barcode_height:
            self._barcode_height = val
            self._write_bytes(Command.GS, 104, val)

    def barcode_left_margin(self, val=0):
        ''' Set the bar code printed on the left spacing. '''

        if not 0 <= val <= 255:
            val = 0

        if val != self._barcode_left_margin:
            self._barcode_left_margin = val
            self._write_bytes(Command.GS, 120, val)

    def barcode_position(self, bc_pos=BarCodePosition.HIDDEN):
        ''' Set bar code position. '''

        if not isinstance(bc_pos, BarCodePosition):
            err = ', '.join([pos.name for pos in BarCodePosition])
            raise ThermalPrinterError('Valid positions are: {}.'.format(err))

        if bc_pos is not self._barcode_position:
            self._barcode_position = bc_pos
            self._write_bytes(Command.GS, 72, bc_pos.value)

    def barcode_width(self, width=2):
        ''' Set bar code width. '''

        if not 2 <= width <= 6:
            width = 2

        if width != self._barcode_width:
            self._barcode_width = width
            self._write_bytes(Command.GS, 119, width)

    def bold(self, state=True):
        ''' Turn emphasized mode on/off. '''

        state = bool(state)
        if state is not self._bold:
            self._bold = state
            self._write_bytes(Command.ESC, 69, int(state))

    def charset(self, charset=None):
        ''' Select an internal character set. '''

        if not charset:
            charset = CharSet.USA
        elif not isinstance(charset, CharSet):
            err = 'Valid charsets are: {}.'.format(
                ', '.join([cset.name for cset in CharSet]))
            raise ThermalPrinterError(err)

        if charset is not self._charset:
            self._charset = charset
            self._write_bytes(Command.ESC, 82, charset.value)

    def char_spacing(self, spacing=0):
        ''' Set the right character spacing. '''

        if not 0 <= spacing <= 255:
            spacing = 0

        if spacing != self._char_spacing:
            self._char_spacing = spacing
            self._write_bytes(Command.ESC, 32, spacing)

    def chinese(self, state=True):
        ''' Select/cancel Chinese mode. '''

        state = bool(state)
        if state is not self._chinese:
            self._chinese = state
            self._write_bytes(Command.FS, 38 if state else 46)

    def chinese_format(self, fmt=None):
        ''' Selection of the Chinese format. '''

        if not fmt:
            fmt = Chinese.UTF_8
        elif not isinstance(fmt, Chinese):
            err = ', '.join([cfmt.name for cfmt in Chinese])
            raise ThermalPrinterError(
                'Valid Chinese formats are: {}.'.format(err))

        if fmt is not self._chinese_format:
            self._chinese_format = fmt
            self._write_bytes(Command.ESC, 57, fmt.value)

    def codepage(self, codepage=None):
        ''' Select character code table. '''

        if not codepage:
            codepage = CodePage.CP437
        elif not isinstance(codepage, CodePage):
            codes = ''
            last = list(CodePage)[-1]
            for cpage in CodePage:
                sep = '.' if cpage is last else ', '
                _, name = cpage.value
                if name:
                    codes += '{} ({}){}'.format(cpage.name, name, sep)
                else:
                    codes += '{}{}'.format(cpage.name, sep)
            raise ThermalPrinterError('Valid codepages are: {}'.format(codes))

        if codepage is not self._codepage:
            self._codepage = codepage
            value, _ = codepage.value
            self._write_bytes(Command.ESC, 116, value)
            sleep(0.05)

    def double_height(self, state=True):
        ''' Set double height mode. '''

        state = bool(state)
        if state is not self._double_height:
            self._double_height = state
            if state:
                self._set_print_mode(16)
            else:
                self._unset_print_mode(16)

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
        sleep(number * self._dot_feed_time * self._char_height)
        self._prev_byte = '\n'
        self._column = 0
        self._feeds += number

    def flush(self, clear=False):
        ''' Remove the print data in buffer.
            Caution: the receive buffer will not be cleared.
                     Set clear to True if needed.
        '''

        self._write_bytes(Command.ESC, 64)
        self.reset_output_buffer()
        sleep(0.05)
        if clear:
            self.reset_input_buffer()

    def image(self, image):
        ''' Print Image. Requires Python Imaging Library. This is
            specific to the Python port and not present in the Arduino
            library. Image will be cropped to 384 pixels width if
            necessary, and converted to 1-bit w/diffusion dithering.
            For any other behavior (scale, B&W threshold, etc.), use
            the Imaging Library to perform such operations before
            passing the result to this function.

            Max width: 384px.
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
        for row_start in range(0, height, 255):
            chunk_height = min(height - row_start, 255)
            self._write_bytes(Command.DC2, 42, chunk_height,
                              row_bytes_clipped)
            for _ in range(chunk_height):
                for _ in range(row_bytes_clipped):
                    self.write(bytes([bitmap[idx]]))
                    idx += 1
                sleep(row_bytes_clipped * self._byte_time)
                idx += row_bytes - row_bytes_clipped

        self._lines += int(height / self._line_spacing) + 1
        self._prev_byte = '\n'

    def inverse(self, state=True):
        ''' Turn white/black reverse printing mode. '''

        state = bool(state)
        if state is not self._inverse:
            self._inverse = state
            self._write_bytes(Command.GS, 66, int(state))

    def justify(self, value='L'):
        ''' Set text justification. '''

        if not value:
            value = 'L'
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

    def left_margin(self, spacing=0):
        ''' Set the left margin. '''

        if not 0 <= spacing <= 47:
            spacing = 0

        if spacing != self._left_margin:
            self._left_margin = spacing
            self._write_bytes(Command.ESC, 66, spacing)

    def line_spacing(self, spacing=30):
        ''' Set line spacing. '''

        if not 0 <= spacing <= 255:
            spacing = 30

        if spacing != self._line_spacing:
            self._line_spacing = spacing
            self._write_bytes(Command.ESC, 51, spacing)

    def print_char(self, char='', number=1, codepage=None):
        ''' Print one character one or several times in a given code page. '''

        if not codepage and not self._codepage:
            raise ThermalPrinterError('Code page needed.')

        # Save the current code page
        current = self._codepage
        if current is not codepage:
            self.codepage(codepage)

        for _ in range(number):
            self.write(char)

        sleep(number * self._dot_feed_time * self._char_height)

        # restore the original code page
        if current is not codepage:
            self.codepage(current)

    def println(self, line, line_feed=True, **kwargs):
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

        # Apply style
        for style, value in kwargs.items():
            if hasattr(self, style):
                getattr(self, style)(value)

        if line:
            if isinstance(line, (bool, int)):
                line = str(line)
            self.write(self._conv(line))
            if line_feed:
                self.write(b'\n')
            self._lines += 1
            sleep(2 * self._dot_feed_time * self._char_height)

        # Restore default style
        for style, value in kwargs.items():
            if hasattr(self, style):
                getattr(self, style)(False)

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

    def rotate(self, state=True):
        ''' Turn on/off clockwise rotation of 90°. '''

        state = bool(state)
        if state is not self._rotate:
            self._rotate = state
            self._write_bytes(Command.ESC, 86, int(state))

    def set_defaults(self):
        ''' Reset formatting parameters. '''

        self.online()
        self.bold(False)
        self.charset(CharSet.USA)
        self.char_spacing()
        self.codepage(CodePage.CP437)
        self.double_height(False)
        self.inverse(False)
        self.justify()
        self.left_margin()
        self.line_spacing()
        self.rotate(False)
        self.size()
        self.strike(False)
        self.underline(0)
        self.upside_down(False)

    def size(self, value='S'):
        ''' Set text size. '''

        if not value:
            value = 'S'
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

        ret = {'movement': True, 'paper': True,
               'temp': True, 'voltage': True}
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
        sleep(self._dot_print_time * 24 * 26 +
              self._dot_feed_time * (8 * 26 + 32))

    def underline(self, weight=1):
        ''' Turn underline mode on/off.
            0: turns off underline mode
            1: turns on underline mode (1 dot thick)
            2: turns on underline mode (2 dots thick)
        '''

        if 0 <= weight <= 2:
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
            self._write_bytes(255)
            sleep(0.05)    # Sleep 50ms as in documentation
            self.sleep(0)  # SLEEP OFF - IMPORTANT!

    # Private methods

    def _conv(self, data):
        ''' Convert data before sending to the printer. '''

        ret = []
        for char in list(data):
            int_ = ord(char)
            if int_ > 256:
                int_ = ord(chr(int_).encode(self._codepage.name,
                                            errors='replace'))
            ret.append(int_)
        return bytearray(ret)

    def _set_print_mode(self, mask):
        ''' Set the print mode. '''

        self._print_mode |= mask
        self._write_print_mode()
        self._char_height = 48 if self._print_mode & 16 else 24
        self.max_column = 16 if self._print_mode & 32 else 32

    def _update_stats(self):
        ''' Statistics update. '''

        if not self.fo_stats or (self._feeds + self._lines) == 0:
            return

        ini = SafeConfigParser()
        ini.read(self.fo_stats)
        self._lines += ini.getint('stats', 'printed_lines')
        self._feeds += ini.getint('stats', 'line_feeds')
        ini.set('stats', 'printed_lines', str(self._lines))
        ini.set('stats', 'line_feeds', str(self._feeds))
        ini.write(open(self.fo_stats, 'w'))
        self._lines = 0
        self._feeds = 0

    def _unset_print_mode(self, mask):
        ''' Unset the print mode.  '''

        self._print_mode &= ~mask
        self._write_print_mode()
        self._char_height = 48 if self._print_mode & 16 else 24
        self.max_column = 16 if self._print_mode & 32 else 32

    def _write_bytes(self, *args):
        ''' 'Raw' byte-writing. '''

        sleep(len(args) * self._byte_time)
        for data in args:
            if isinstance(data, Command):
                data = data.value
            self.write(bytes([data]))

    def _write_print_mode(self):
        ''' Write the print mode. '''

        self._write_bytes(Command.ESC, 33, self._print_mode)


class ThermalPrinterError(Exception):
    ''' Error. Error. ERRor!/*Er..:._ '''


def test_char(char):
    ''' Test one charactere with all possible code page. '''

    with ThermalPrinter() as printer:
        for codepage in list(CodePage):
            printer.println('{}: {}'.format(codepage.name, char),
                            codepage=codepage)

        return 0

    return 1


def tests():
    ''' Tests. '''

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
        printer.println('现代汉语通用字表', chinese=True,
                        chinese_format=Chinese.BIG5)
        printer.println('Double height', double_height=True)
        printer.println('Double width', double_width=True)
        printer.println('Inverse', inverse=True)
        printer.println('Rotate 90°', rotate=True,
                        codepage=CodePage.ISO_8859_1)
        printer.println('Strike', strike=True)
        printer.println('Underline', underline=1)
        printer.println('Upside down', upside_down=True)

        printer.println('Voilà !', justify='C', strike=True,
                        underline=2)

        printer.feed(2)
        return 0

    return 1


if __name__ == '__main__':
    exit(tests())

#!/usr/bin/env python3
# coding: utf-8
''' This is part of the Python's module to manage the DP-EH600 thermal printer.
    Source: https://github.com/BoboTiG/thermalprinter
'''

from atexit import register
from time import sleep

from serial import Serial

from .constants import BarCode, BarCodePosition, CharSet, Chinese, Command, \
    CodePage
from .exceptions import ThermalPrinterConstantError, ThermalPrinterValueError


class ThermalPrinter(Serial):
    ''' I talk to printers. Easy! '''

    # pylint: disable=too-many-ancestors
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-public-methods
    # pylint: disable=too-many-locals

    lines = 0
    feeds = 0
    max_column = 32

    def __init__(self, port='/dev/ttyAMA0', baudrate=19200, **kwargs):
        ''' Print init. '''

        try:
            heat_time = int(kwargs['heat_time'])
        except (KeyError, ValueError):
            heat_time = 80
        if not 0 <= heat_time <= 255:
            raise ThermalPrinterValueError(
                'heat_time should be between 0 and 255 (default: 80).')

        try:
            heat_interval = int(kwargs['heat_interval'])
        except (KeyError, ValueError):
            heat_interval = 12
        if not 0 <= heat_interval <= 255:
            raise ThermalPrinterValueError(
                'heat_interval should be between 0 and 255 (default: 12).')

        try:
            heated_point = int(kwargs['heated_point'])
        except (KeyError, ValueError):
            heated_point = 3
        if not 0 <= heated_point <= 255:
            raise ThermalPrinterValueError(
                'heated_point should be between 0 and 255 (default: 3).')

        # Init the serial
        super().__init__(port=port, baudrate=self._baudrate)
        sleep(0.5)  # Important
        register(self._on_exit)

        # Printer settings
        self._write_bytes(
            Command.ESC, 55, heated_point, heat_time, heat_interval)

        self._baudrate = baudrate
        self._byte_time = 11.0 / float(self._baudrate)
        self._dot_feed_time = 0.0025
        self._dot_print_time = 0.033

        # Default values
        self._barcode_height = 80
        self._barcode_left_margin = 0
        self._barcode_position = BarCodePosition.HIDDEN
        self._barcode_width = 0
        self._bold = False
        self._charset = CharSet.USA
        self._char_spacing = 0
        self._char_height = 24
        self._chinese = False
        self._chinese_format = Chinese.UTF_8
        self._codepage = CodePage.CP437
        self._column = 0
        self._double_height = False
        self._double_width = False
        self._inverse = False
        self._is_online = True
        self._is_sleeping = False
        self._justify = 'L'
        self._left_margin = 0
        self._line_spacing = 30
        self._prev_byte = ''
        self._print_mode = 0
        self._rotate = False
        self._size = 'S'
        self._strike = False
        self._underline = 0
        self._upside_down = False

        # Factory settings
        self.reset()

    def __enter__(self):
        ''' `with ThermalPrinter() as printer:` '''

        return self

    def _on_exit(self):
        ''' To be sure we keep stats and cleanup. '''

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
            raise ThermalPrinterConstantError('Valid bar codes are: ' + err)

        code, (min_, max_), range_type = bc_type.value
        data_len = len(data)
        range_ = ranges_[range_type]()

        if not min_ <= data_len <= max_:
            err = '[{}] Should be {} <= len(data) <= {} (current: {}).'.format(
                bc_type.name, min_, max_, data_len)
            raise ThermalPrinterValueError(err)
        elif bc_type is BarCode.ITF and data_len % 2 != 0:
            raise ThermalPrinterValueError(
                '[BarCode.ITF] len(data) must be even.')

        if not all(ord(char) in range_ for char in data):
            if range_type != 3:
                valid = map(chr, range_)
            else:
                valid = map(hex, range_)
            err = '[{}] Valid characters: {}.'.format(
                bc_type.name, ', '.join(valid))
            raise ThermalPrinterValueError(err)

        self._write_bytes(Command.GS, 107, code, data_len)
        for char in list(data):
            char = bytes([ord(char)])
            self.write(char)
        sleep(
            (self._barcode_height + self._line_spacing) * self._dot_print_time)
        self._prev_byte = '\n'
        self.lines += int(self._barcode_height / self._line_spacing) + 1

    def barcode_height(self, height=80):
        ''' Set bar code height. '''

        if not 1 <= height <= 255:
            raise ThermalPrinterValueError(
                'height should be between 1 and 255 (default: 80).')

        if height != self._barcode_height:
            self._barcode_height = height
            self._write_bytes(Command.GS, 104, height)

    def barcode_left_margin(self, margin=0):
        ''' Set the bar code printed on the left spacing. '''

        if not 0 <= margin <= 255:
            raise ThermalPrinterValueError(
                'margin should be between 0 and 255 (default: 0).')

        if margin != self._barcode_left_margin:
            self._barcode_left_margin = margin
            self._write_bytes(Command.GS, 120, margin)

    def barcode_position(self, position=BarCodePosition.HIDDEN):
        ''' Set bar code position. '''

        if not isinstance(position, BarCodePosition):
            err = ', '.join([pos.name for pos in BarCodePosition])
            raise ThermalPrinterConstantError(
                'Valid positions are: {}.'.format(err))

        if position is not self._barcode_position:
            self._barcode_position = position
            self._write_bytes(Command.GS, 72, position.value)

    def barcode_width(self, width=2):
        ''' Set bar code width. '''

        if not 2 <= width <= 6:
            raise ThermalPrinterValueError(
                'width should be between 2 and 6 (default: 2).')

        if width != self._barcode_width:
            self._barcode_width = width
            self._write_bytes(Command.GS, 119, width)

    def bold(self, state=False):
        ''' Turn emphasized mode on/off. '''

        state = bool(state)
        if state is not self._bold:
            self._bold = state
            self._write_bytes(Command.ESC, 69, int(state))

    def charset(self, charset=CharSet.USA):
        ''' Select an internal character set. '''

        if not isinstance(charset, CharSet):
            err = 'Valid charsets are: {}.'.format(
                ', '.join([cset.name for cset in CharSet]))
            raise ThermalPrinterConstantError(err)

        if charset is not self._charset:
            self._charset = charset
            self._write_bytes(Command.ESC, 82, charset.value)

    def char_spacing(self, spacing=0):
        ''' Set the right character spacing. '''

        if not 0 <= spacing <= 255:
            raise ThermalPrinterValueError(
                'spacing should be between 0 and 255 (default: 0).')

        if spacing != self._char_spacing:
            self._char_spacing = spacing
            self._write_bytes(Command.ESC, 32, spacing)

    def chinese(self, state=False):
        ''' Select/cancel Chinese mode. '''

        state = bool(state)
        if state is not self._chinese:
            self._chinese = state
            self._write_bytes(Command.FS, 38 if state else 46)

    def chinese_format(self, fmt=Chinese.UTF_8):
        ''' Selection of the Chinese format. '''

        if not isinstance(fmt, Chinese):
            err = ', '.join([cfmt.name for cfmt in Chinese])
            raise ThermalPrinterConstantError(
                'Valid Chinese formats are: {}.'.format(err))

        if fmt is not self._chinese_format:
            self._chinese_format = fmt
            self._write_bytes(Command.ESC, 57, fmt.value)

    def codepage(self, codepage=CodePage.CP437):
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
            raise ThermalPrinterConstantError(
                'Valid codepages are: {}'.format(codes))

        if codepage is not self._codepage:
            self._codepage = codepage
            value, _ = codepage.value
            self._write_bytes(Command.ESC, 116, value)
            sleep(0.05)

    def double_height(self, state=False):
        ''' Set double height mode. '''

        state = bool(state)
        if state is not self._double_height:
            self._double_height = state
            if state:
                self._set_print_mode(16)
            else:
                self._unset_print_mode(16)

    def double_width(self, state=False):
        ''' Select double width mode. '''

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
            raise ThermalPrinterValueError(
                'number should be between 0 and 255 (default: 1).')

        self._write_bytes(Command.ESC, 100, number)
        sleep(number * self._dot_feed_time * self._char_height)
        self._prev_byte = '\n'
        self._column = 0
        self.feeds += number

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
        ''' Print Image. Requires Python Imaging Library.
            Image will be cropped to 384 pixels width if
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

        self.lines += int(height / self._line_spacing) + 1
        self._prev_byte = '\n'

    def inverse(self, state=False):
        ''' Turn white/black reverse printing mode. '''

        state = bool(state)
        if state is not self._inverse:
            self._inverse = state
            self._write_bytes(Command.GS, 66, int(state))

    def justify(self, value='L'):
        ''' Set text justification. '''

        value = value.upper()
        if value not in 'LCR':
            err = 'value should be one of L (left, default), C (center)'
            err += '  or R (right).'
            raise ThermalPrinterValueError(err)

        if value != self._justify:
            self._justify = value
            if value == 'C':
                pos = 1
            elif value == 'R':
                pos = 2
            else:
                pos = 0
            self._write_bytes(Command.ESC, 97, pos)

    def left_margin(self, margin=0):
        ''' Set the left margin. '''

        if not 0 <= margin <= 47:
            raise ThermalPrinterValueError(
                'margin should be between 0 and 47 (default: 0).')

        if margin != self._left_margin:
            self._left_margin = margin
            self._write_bytes(Command.ESC, 66, margin)

    def line_spacing(self, spacing=30):
        ''' Set line spacing. '''

        if not 0 <= spacing <= 255:
            raise ThermalPrinterValueError(
                'spacing should be between 0 and 255 (default: 30).')

        if spacing != self._line_spacing:
            self._line_spacing = spacing
            self._write_bytes(Command.ESC, 51, spacing)

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

    def out(self, line, line_feed=True, **kwargs):
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
            try:
                getattr(self, style)(value)
            except TypeError:
                pass

        if line:
            if isinstance(line, (bool, int)):
                line = str(line)
            self.write(self._conv(line))
            if line_feed:
                self.write(b'\n')
                self.lines += 1

                # Sizes M and L are double height
                if self._size != 'S':
                    self.lines += 1

            sleep(2 * self._dot_feed_time * self._char_height)

        # Restore default style
        for style, value in kwargs.items():
            try:
                getattr(self, style)()
            except TypeError:
                pass

    def print_char(self, char='', number=1, codepage=None):
        ''' Print one character one or several times in a given code page. '''

        if not codepage and not self._codepage:
            raise ThermalPrinterConstantError('Code page needed.')

        # Save the current code page
        current = self._codepage
        if current is not codepage:
            self.codepage(codepage)

        for _ in range(number):
            self.write(char)

        sleep(number * self._dot_feed_time * self._char_height)

        # Restore the original code page
        if current is not codepage:
            self.codepage(current)

    def rotate(self, state=False):
        ''' Turn on/off clockwise rotation of 90°. '''

        state = bool(state)
        if state is not self._rotate:
            self._rotate = state
            self._write_bytes(Command.ESC, 86, int(state))

    def size(self, value='S'):
        ''' Set text size. '''

        value = value.upper()
        if value not in 'SML':
            err = 'value should be one of S (small, default), M (medium)'
            err += '  or L (large).'
            raise ThermalPrinterValueError(err)

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

        if not self._is_sleeping and seconds > 0:
            self._is_sleeping = True
            sleep(seconds)
            self._write_bytes(Command.ESC, 56, seconds, seconds >> 8)

    def status(self):
        ''' Check the printer status. If RX pin is not connected, all values
            will be set to True.

            Return a dict:
                movement: False if the movement is not connected
                   paper: False is no paper
                    temp: False if the temperature exceeds 60°C
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

    def strike(self, state=False):
        ''' Turn on/off double-strike mode. '''

        state = bool(state)
        if state is not self._strike:
            self._strike = state
            self._write_bytes(Command.ESC, 71, int(state))

    def reset(self):
        ''' Reset the printer to factory defaults. '''

        self._write_bytes(Command.ESC, 64)

    def test(self):
        ''' Print settings as test. '''

        self._write_bytes(Command.DC2, 84)
        sleep(self._dot_print_time * 24 * 26 +
              self._dot_feed_time * (8 * 26 + 32))

    def underline(self, weight=0):
        ''' Turn underline mode on/off.
            0: turns off underline mode
            1: turns on underline mode (1 dot thick)
            2: turns on underline mode (2 dots thick)
        '''

        if not 0 <= weight <= 2:
            raise ThermalPrinterValueError(
                'weight should be between 0 and 2 (default: 0).')

        if weight != self._underline:
            self._underline = weight
            self._write_bytes(Command.ESC, 45, weight)

    def upside_down(self, state=False):
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

        encoding = 'utf-8' if self._chinese else self._codepage.name
        return bytes(data, encoding, errors='replace')

    def _set_print_mode(self, mask):
        ''' Set the print mode. '''

        self._print_mode |= mask
        self._write_print_mode()
        self._char_height = 48 if self._print_mode & 16 else 24
        self.max_column = 16 if self._print_mode & 32 else 32

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

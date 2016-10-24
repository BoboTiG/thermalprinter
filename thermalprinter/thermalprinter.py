#!/usr/bin/env python3
# coding: utf-8
''' This is part of the Python's module to manage the DP-EH600 thermal printer.
    Source: https://github.com/BoboTiG/thermalprinter
'''

from atexit import register
from time import sleep

from serial import Serial

from .constants import BarCodePosition, CharSet, Chinese, Command, CodePage, \
    CodePageConverted
from .exceptions import ThermalPrinterAttributeError, ThermalPrinterValueError
from .validate import validate_barcode, validate_barcode_position, \
    validate_charset, validate_chinese_format, validate_codepage


class ThermalPrinter(Serial):
    ''' I talk to printers. Easy! '''

    # pylint: disable=too-many-ancestors
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-public-methods
    # pylint: disable=too-many-locals
    # pylint: disable=attribute-defined-outside-init

    # Counters
    __lines = 0
    __feeds = 0

    def __init__(self, port='/dev/ttyAMA0', baudrate=19200, **kwargs):
        ''' Print init. '''

        try:
            self.heat_time = int(kwargs['heat_time'])
        except KeyError:
            self.heat_time = 80
        if not 0 <= self.heat_time <= 255:
            raise ThermalPrinterValueError(
                'heat_time should be between 0 and 255 (default: 80).')

        try:
            self.heat_interval = int(kwargs['heat_interval'])
        except KeyError:
            self.heat_interval = 12
        if not 0 <= self.heat_interval <= 255:
            raise ThermalPrinterValueError(
                'heat_interval should be between 0 and 255 (default: 12).')

        try:
            self.most_heated_point = int(kwargs['most_heated_point'])
        except KeyError:
            self.most_heated_point = 3
        if not 0 <= self.most_heated_point <= 255:
            raise ThermalPrinterValueError(
                'most_heated_point should be between 0 and 255 (default: 3).')

        # Few important values
        self._baudrate = baudrate
        self._byte_time = 11.0 / float(self._baudrate)
        self._dot_feed_time = 0.0025
        self._dot_print_time = 0.033

        # Init the serial
        super().__init__(port=port, baudrate=self._baudrate)
        sleep(0.5)  # Important
        register(self._on_exit)

        # Printer settings
        self.send_command(Command.ESC, 55, self.most_heated_point,
                          self.heat_time, self.heat_interval)

        # Factory settings
        self.reset()

    def __enter__(self):
        ''' `with ThermalPrinter() as printer:` '''

        return self

    def _on_exit(self):
        ''' To be sure we keep stats and cleanup. '''

        self.close()

    def __repr__(self):
        ''' String representation of the current printer settings
            and its state.

            To know the serial state:
            >>> printer = ThermalPrinter()
            >>> super(type(printer), printer).__repr__()
        '''

        return '{name}<id=0x{id:x}, heat_interval={p.heat_interval}, ' \
            'most_heated_point={p.most_heated_point}, ' \
            'heat_time={p.heat_time}, is_online={p.is_online}, ' \
            'is_sleeping={p.is_sleeping}, max_column={p.max_column!r}>(' \
            'barcode_height={p._barcode_height!r}, ' \
            'barcode_left_margin={p._barcode_left_margin!r}, ' \
            'barcode_position={p._barcode_position!r}, ' \
            'barcode_width={p._barcode_width!r}, ' \
            'bold={p._bold}, ' \
            'charset={p._charset!r}, ' \
            'char_spacing={p._char_spacing!r}, ' \
            'char_height={p._char_height!r}, ' \
            'chinese={p._chinese}, ' \
            'chinese_format={p._chinese_format!r}, ' \
            'codepage={p._codepage!r}, ' \
            'double_height={p._double_height!r}, ' \
            'double_width={p._double_width!r}, ' \
            'inverse={p._inverse}, ' \
            'justify={p._justify!r}, ' \
            'left_margin={p._left_margin!r}, ' \
            'line_spacing={p._line_spacing!r}, ' \
            'rotate={p._rotate}, ' \
            'size={p._size!r}, ' \
            'strike={p._strike}, ' \
            'underline={p._underline!r}, ' \
            'upside_down={p._upside_down}' \
            ')'.format(name=self.__class__.__name__, id=id(self), p=self)

    # Protect some attributes to being modified outside this class.

    @property
    def is_online(self):
        ''' The printer is online. '''
        return self.__is_online

    @is_online.setter
    def is_online(self, _):  # pylint: disable=no-self-use
        ''' Read-only attribute. '''
        raise ThermalPrinterAttributeError('Read-only attribute.')

    @property
    def is_sleeping(self):
        ''' The printer is sleeping. '''
        return self.__is_sleeping

    @is_sleeping.setter
    def is_sleeping(self, _):  # pylint: disable=no-self-use
        ''' Read-only attribute. '''
        raise ThermalPrinterAttributeError('Read-only attribute.')

    @property
    def lines(self):
        ''' Number of printed lines since the start of the script. '''
        return self.__lines

    @lines.setter
    def lines(self, _):  # pylint: disable=no-self-use
        ''' Read-only attribute. '''
        raise ThermalPrinterAttributeError('Read-only attribute.')

    @property
    def feeds(self):
        ''' Number of printed line feeds since the start of the script. '''
        return self.__feeds

    @feeds.setter
    def feeds(self, _):  # pylint: disable=no-self-use
        ''' Read-only attribute. '''
        raise ThermalPrinterAttributeError('Read-only attribute.')

    @property
    def max_column(self):
        ''' Number of printable characters on one line. '''
        return self.__max_column

    @max_column.setter
    def max_column(self, _):  # pylint: disable=no-self-use
        ''' Read-only attribute. '''
        raise ThermalPrinterAttributeError('Read-only attribute.')

    # Module's methods

    def out(self, data, line_feed=True, **kwargs):
        ''' Send one line to the printer.

            You can pass formatting instructions directly via arguments:
            >>> out(data, justify='C', inverse=True)

            This will prevent you to do:
            >>> justify('C')
            >>> inverse(True)
            >>> out(data)
            >>> inverse(False)
            >>> justify('L')
        '''

        if data is None:
            return

        # Apply style
        for style, value in kwargs.items():
            try:
                getattr(self, style)(value)
            except TypeError:
                pass

        self.write(self.to_bytes(data))
        if line_feed:
            self.write(b'\n')
            self.__lines += 1

            # Sizes M and L are double height
            if self._size != 'S':
                self.__lines += 1

        sleep(2 * self._dot_feed_time * self._char_height)

        # Restore default style
        for style, value in kwargs.items():
            try:
                getattr(self, style)()
            except TypeError:
                pass

    def send_command(self, *args):
        ''' 'Raw' byte-writing. '''

        for data in args:
            if isinstance(data, Command):
                data = data.value
            self.write(bytes([data]))
        sleep(len(args) * self._byte_time)

    def to_bytes(self, data):
        ''' Convert data before sending to the printer. '''

        if isinstance(data, (bool, int, float, complex)):
            data = str(data)
        elif isinstance(data, bytes):
            return data
        elif isinstance(data, bytearray):
            return bytes(data)
        elif isinstance(data, memoryview):
            return data.tobytes()

        encoding = 'utf-8' if self._chinese else self._codepage.name
        try:
            return bytes(data, encoding, errors='replace')
        except LookupError:
            # Fall back to the most appropriate code page
            # >>> ls(CodePageConverted)
            encoding = CodePageConverted[self._codepage.name].value
            return bytes(data, encoding, errors='replace')

    # Printer's methods

    def barcode(self, data, barcode_type):
        ''' Bar code printing. '''

        validate_barcode(data, barcode_type)
        code = barcode_type.value[0]
        self.send_command(Command.GS, 107, code, len(data))
        # TODO: use out() ?
        for char in list(data):
            char = bytes([ord(char)])
            self.write(char)
        sleep(
            (self._barcode_height + self._line_spacing) * self._dot_print_time)
        self.__lines += int(self._barcode_height / self._line_spacing) + 1

    def barcode_height(self, height=162):
        ''' Set bar code height. '''

        if not isinstance(height, int) or not 1 <= height <= 255:
            raise ThermalPrinterValueError(
                'height should be between 1 and 255 (default: 162).')

        if height != self._barcode_height:
            self._barcode_height = height
            self.send_command(Command.GS, 104, height)

    def barcode_left_margin(self, margin=0):
        ''' Set the left margin of the bar code. '''

        if not isinstance(margin, int) or not 0 <= margin <= 255:
            raise ThermalPrinterValueError(
                'margin should be between 0 and 255 (default: 0).')

        if margin != self._barcode_left_margin:
            self._barcode_left_margin = margin
            self.send_command(Command.GS, 120, margin)

    def barcode_position(self, position=BarCodePosition.HIDDEN):
        ''' Set the bar code position. '''

        validate_barcode_position(position)
        if position is not self._barcode_position:
            self._barcode_position = position
            self.send_command(Command.GS, 72, position.value)

    def barcode_width(self, width=3):
        ''' Set the bar code width. '''

        if not isinstance(width, int) or not 2 <= width <= 6:
            raise ThermalPrinterValueError(
                'width should be between 2 and 6 (default: 3).')

        if width != self._barcode_width:
            self._barcode_width = width
            self.send_command(Command.GS, 119, width)

    def bold(self, state=False):
        ''' Turn emphasized mode on/off. '''

        state = bool(state)
        if state is not self._bold:
            self._bold = state
            self.send_command(Command.ESC, 69, int(state))

    def charset(self, charset=CharSet.USA):
        ''' Select an internal character set. '''

        validate_charset(charset)
        if charset is not self._charset:
            self._charset = charset
            self.send_command(Command.ESC, 82, charset.value)

    def char_spacing(self, spacing=0):
        ''' Set the right character spacing. '''

        if not isinstance(spacing, int) or not 0 <= spacing <= 255:
            raise ThermalPrinterValueError(
                'spacing should be between 0 and 255 (default: 0).')

        if spacing != self._char_spacing:
            self._char_spacing = spacing
            self.send_command(Command.ESC, 32, spacing)

    def chinese(self, state=False):
        ''' Select/cancel Chinese mode. '''

        state = bool(state)
        if state is not self._chinese:
            self._chinese = state
            self.send_command(Command.FS, 38 if state else 46)

    def chinese_format(self, fmt=Chinese.GBK):
        ''' Selection of the Chinese format. '''

        validate_chinese_format(fmt)
        if fmt is not self._chinese_format:
            self._chinese_format = fmt
            self.send_command(Command.ESC, 57, fmt.value)

    def codepage(self, codepage=CodePage.CP437):
        ''' Select character code table. '''

        validate_codepage(codepage)
        if not self._chinese and codepage is not self._codepage:
            self._codepage = codepage
            value, _ = codepage.value
            self.send_command(Command.ESC, 116, value)
            sleep(0.05)

    def double_height(self, state=False):
        ''' Set double height mode. '''

        state = bool(state)
        if state is not self._double_height:
            self._double_height = state
            self._char_height = 48 if state else 24
            self.send_command(Command.ESC, 33, 16 if state else 0)

    def double_width(self, state=False):
        ''' Select double width mode. '''

        state = bool(state)
        if state is not self._double_width:
            self._double_width = state
            self.__max_column = 16 if state else 32
            self.send_command(Command.ESC, 14 if state else 20, 1)

    def feed(self, number=1):
        ''' Feeds by the specified number of lines. '''

        if not isinstance(number, int) or not 0 <= number <= 255:
            raise ThermalPrinterValueError(
                'number should be between 0 and 255 (default: 1).')

        self.send_command(Command.ESC, 100, number)
        sleep(number * self._dot_feed_time * self._char_height)
        self.__feeds += number

    def flush(self, clear=False):
        ''' Remove the print data in buffer.
            Caution: the receive buffer will not be cleared.
                     Set clear to True if needed.
        '''

        self.send_command(Command.ESC, 64)
        self.reset_output_buffer()
        sleep(0.05)
        if clear:
            self.reset_input_buffer()

    def image(self, image):
        ''' Print Image. Requires Python Imaging Library (pillow).
            Image will be cropped to 384 pixels width if
            necessary, and converted to 1-bit w/diffusion dithering.
            For any other behavior (scale, B&W threshold, etc.), use
            the Imaging Library to perform such operations before
            passing the result to this function.

            Max width: 384px.

            >>> from PIL import Image
            >>> printer.image(Image.open('picture.png'))
        '''

        # Checks if an object is an image object. See `isImageType()` from
        # https://github.com/python-pillow/Pillow/blob/master/PIL/Image.py
        if not hasattr(image, 'im'):
            raise ThermalPrinterValueError('image should be a PIL Image.')

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
            self.send_command(Command.DC2, 42, chunk_height,
                              row_bytes_clipped)
            for _ in range(chunk_height):
                for _ in range(row_bytes_clipped):
                    self.write(bytes([bitmap[idx]]))
                    idx += 1
                sleep(row_bytes_clipped * self._byte_time)
                idx += row_bytes - row_bytes_clipped

        self.__lines += int(height / self._line_spacing) + 1

    def inverse(self, state=False):
        ''' Turn white/black reverse printing mode. '''

        state = bool(state)
        if state is not self._inverse:
            self._inverse = state
            self.send_command(Command.GS, 66, int(state))

    def justify(self, value='L'):
        ''' Set text justification. '''

        if not isinstance(value, str) or value not in 'LCR':
            err = 'value should be one of L (left, default), C (center)'
            err += '  or R (right).'
            raise ThermalPrinterValueError(err)

        value = value.upper()
        if value != self._justify:
            self._justify = value
            if value == 'C':
                pos = 1
            elif value == 'R':
                pos = 2
            else:
                pos = 0
            self.send_command(Command.ESC, 97, pos)

    def left_margin(self, margin=0):
        ''' Set the left margin. '''

        if not isinstance(margin, int) or not 0 <= margin <= 47:
            raise ThermalPrinterValueError(
                'margin should be between 0 and 47 (default: 0).')

        if margin != self._left_margin:
            self._left_margin = margin
            self.send_command(Command.ESC, 66, margin)

    def line_spacing(self, spacing=30):
        ''' Set line spacing. '''

        if not isinstance(spacing, int) or not 0 <= spacing <= 255:
            raise ThermalPrinterValueError(
                'spacing should be between 0 and 255 (default: 30).')

        if spacing != self._line_spacing:
            self._line_spacing = spacing
            self.send_command(Command.ESC, 51, spacing)

    def offline(self):
        ''' Take the printer offline. Print commands sent after this
            will be ignored until 'online' is called.
        '''

        if self.is_online:
            self.__is_online = False
            self.send_command(Command.ESC, 61, 0)

    def online(self):
        ''' Take the printer online.
            Subsequent print commands will be obeyed.
        '''

        if not self.is_online:
            self.__is_online = True
            self.send_command(Command.ESC, 61, 1)

    def reset(self):
        ''' Reset the printer to factory defaults. '''

        self.send_command(Command.ESC, 64)

        # Default values
        self.__max_column = 32
        self.__is_online = True
        self.__is_sleeping = False

        self._barcode_height = 162
        self._barcode_left_margin = 0
        self._barcode_position = BarCodePosition.HIDDEN
        self._barcode_width = 3
        self._bold = False
        self._charset = CharSet.USA
        self._char_spacing = 0
        self._char_height = 24
        self._chinese = False
        self._chinese_format = Chinese.GBK
        self._codepage = CodePage.CP437
        self._double_height = False
        self._double_width = False
        self._inverse = False
        self._justify = 'L'
        self._left_margin = 0
        self._line_spacing = 30
        self._rotate = False
        self._size = 'S'
        self._strike = False
        self._underline = 0
        self._upside_down = False

    def rotate(self, state=False):
        ''' Turn on/off clockwise rotation of 90°. '''

        state = bool(state)
        if state is not self._rotate:
            self._rotate = state
            self.send_command(Command.ESC, 86, int(state))

    def size(self, value='S'):
        ''' Set text size. '''

        if not isinstance(value, str) or value not in 'SML':
            err = 'value should be one of S (small, default), M (medium)'
            err += '  or L (large).'
            raise ThermalPrinterValueError(err)

        value = value.upper()
        if value != self._size:
            self._size = value
            if value == 'L':    # Large: double width and height
                size, self._char_height, self.__max_column = 0x11, 48, 16
            elif value == 'M':  # Medium: double height
                size, self._char_height, self.__max_column = 0x01, 48, 32
            else:
                size, self._char_height, self.__max_column = 0x00, 24, 32

            self.send_command(Command.GS, 33, size)

    def sleep(self, seconds=1):
        ''' Put the printer into a low-energy state. '''

        if self.is_sleeping:
            return

        if not isinstance(seconds, int) or seconds < 0:
            raise ThermalPrinterValueError(
                'seconds should be null or positive (default: 0).')

        if seconds:
            self.__is_sleeping = True
        self.send_command(Command.ESC, 56, seconds, seconds >> 8)

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
        self.send_command(Command.ESC, 118, 0)
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
            self.send_command(Command.ESC, 71, int(state))

    def test(self):
        ''' Print the test page (contains printer's settings). '''

        self.send_command(Command.DC2, 84)
        sleep(self._dot_print_time * 24 * 26 +
              self._dot_feed_time * (8 * 26 + 32))

    def underline(self, weight=0):
        ''' Turn underline mode on/off.
            0: turns off underline mode
            1: turns on underline mode (1 dot thick)
            2: turns on underline mode (2 dots thick)
        '''

        if not isinstance(weight, int) or not 0 <= weight <= 2:
            raise ThermalPrinterValueError(
                'weight should be between 0 and 2 (default: 0).')

        if weight != self._underline:
            self._underline = weight
            self.send_command(Command.ESC, 45, weight)

    def upside_down(self, state=False):
        ''' Turns on/off upside-down printing mode. '''

        state = bool(state)
        if state is not self._upside_down:
            self._upside_down = state
            self.send_command(Command.ESC, 123, int(state))

    def wake(self):
        ''' Wake up the printer. '''

        if self.is_sleeping:
            self.__is_sleeping = False
            self.send_command(255)
            sleep(0.05)    # Sleep 50ms as in documentation
            self.sleep(0)  # SLEEP OFF - IMPORTANT!

"""This is part of the Python's module to manage the DP-EH600 thermal printer.
Source: https://github.com/BoboTiG/thermalprinter.
"""

from __future__ import annotations

import contextlib
from atexit import register
from time import sleep
from typing import Any

from serial import Serial

from thermalprinter.constants import (
    BarCode,
    BarCodePosition,
    CharSet,
    Chinese,
    CodePage,
    CodePageConverted,
    Command,
)
from thermalprinter.exceptions import ThermalPrinterCommunicationError, ThermalPrinterValueError
from thermalprinter.validate import (
    validate_barcode,
    validate_barcode_position,
    validate_charset,
    validate_chinese_format,
    validate_codepage,
)


class ThermalPrinter(Serial):
    r""":param str port: Serial port to use, known as the device name.
    :param int baudrate: Baud rate such as 9600, or 115200 etc.
    :param float command_timeout: Command timeout, in seconds.
    :param dict \\*\\*kwargs: Additionnal optional arguments:

        - ``heat_time`` (int): printer heat time (default: ``80``);
        - ``heat_interval`` (int): printer heat time interval (default: ``12``);
        - ``most_heated_point`` (int): for the printer, the most heated point (default: ``3``).

    :exception ThermalPrinterValueError: On incorrect argument's type or value.

    .. versionchanged:: 0.3.0
        Added ``command_timeout`` keyword-argument.
    """

    # Counters
    __lines: int = 0
    __feeds: int = 0

    # Default values
    __max_column = 32
    __is_online = True
    __is_sleeping = False
    _barcode_height = 162
    _barcode_left_margin = 0
    _barcode_position = BarCodePosition.HIDDEN
    _barcode_width = 3
    _bold = False
    _charset = CharSet.USA
    _char_spacing = 0
    _char_height = 24
    _chinese = False
    _chinese_format = Chinese.GBK
    _codepage = CodePage.CP437
    _double_height = False
    _double_width = False
    _inverse = False
    _justify = "L"
    _left_margin = 0
    _line_spacing = 30
    _rotate = False
    _size = "S"
    _strike = False
    _underline = 0
    _upside_down = False

    def __init__(
        self,
        port: str = "/dev/ttyAMA0",
        baudrate: int = 19200,
        command_timeout: float = 0.05,
        **kwargs: Any,
    ) -> None:
        # Few important values
        self._baudrate = baudrate
        self._byte_time = 11.0 / float(self._baudrate)
        self._dot_feed_time = 0.0025
        self._dot_print_time = 0.033
        self._command_timeout = command_timeout
        self.heat_time = int(kwargs.get("heat_time", 80))
        self.heat_interval = int(kwargs.get("heat_interval", 12))
        self.most_heated_point = int(kwargs.get("most_heated_point", 3))

        # Init the serial
        super().__init__(port=port, baudrate=self._baudrate)
        sleep(0.5)  # Important
        register(self._on_exit)

        # Several checks
        if not 0 <= self.heat_time <= 255:
            msg = "heat_time should be between 0 and 255 (default: 80)."
            raise ThermalPrinterValueError(msg)
        if not 0 <= self.heat_interval <= 255:
            msg = "heat_interval should be between 0 and 255 (default: 12)."
            raise ThermalPrinterValueError(msg)
        if not 0 <= self.most_heated_point <= 255:
            msg = "most_heated_point should be between 0 and 255 (default: 3)."
            raise ThermalPrinterValueError(msg)

        # Printer settings
        self.send_command(Command.ESC, 55, self.most_heated_point, self.heat_time, self.heat_interval)

        # Factory settings
        self.reset()

    def __enter__(self) -> ThermalPrinter:  # noqa: PYI034
        """`with ThermalPrinter() as printer:`."""
        return self

    def _on_exit(self) -> None:
        """To be sure we keep stats and cleanup."""
        self.close()

    def __repr__(self) -> str:
        """Representation of the current printer settings and its state.

        To know the serial state:

        >>> printer = ThermalPrinter()
        >>> repr(super(type(printer), printer))
        """
        settings = (
            f"heat_interval={self.heat_interval}",
            f"heat_time={self.heat_time}",
            f"most_heated_point={self.most_heated_point}",
        )
        states = []

        for var in vars(self):
            if not var.startswith("_"):
                continue

            try:
                attr = getattr(self, var[1:])
            except AttributeError:
                continue
            else:
                if not callable(attr):
                    continue
                states.append(f"{var[1:]}={getattr(self, var)}")

        return (
            f"{type(self).__name__}"
            f"<id=0x{id(self):x}, {', '.join(sorted(settings))}>"
            f"({', '.join(sorted(states))})"
        )

    # Protect some attributes to being modified outside this class.

    @property
    def is_online(self) -> bool:
        """The printer online status."""
        return self.__is_online

    @property
    def is_sleeping(self) -> bool:
        """The printer sleep status."""
        return self.__is_sleeping

    @property
    def lines(self) -> int:
        """Number of printed lines since the start of the script."""
        return self.__lines

    @property
    def feeds(self) -> int:
        """Number of printed line feeds since the start of the script."""
        return self.__feeds

    @property
    def max_column(self) -> int:
        """Number of printable characters on one line."""
        return self.__max_column

    # Module's methods

    def out(self, data: Any, line_feed: bool = True, **kwargs: Any) -> None:
        """Send one line to the printer.

        :param mixed data: the data to print.
        :param bool line_feed: send a line break after the printed data.
        :param dict kwargs: additional styles to apply.

        You can pass formatting instructions directly via arguments:

        >>> printer.out(data, justify="C", inverse=True)

        This is a quicker way to do:

        >>> printer.justify("C")
        >>> printer.inverse(True)
        >>> printer.out(data)
        >>> printer.inverse(False)
        >>> printer.justify("L")
        """
        if data is None:
            return

        # Apply style
        for style, value in kwargs.items():
            with contextlib.suppress(TypeError):
                getattr(self, style)(value)
        self.write(self.to_bytes(data))
        if line_feed:
            self.write(b"\n")
            self.__lines += 1

            # Sizes M and L are double height
            if self._size != "S":
                self.__lines += 1

        sleep(2 * self._dot_feed_time * self._char_height)

        # Restore default style
        for style in kwargs:
            with contextlib.suppress(TypeError):
                getattr(self, style)()

    def send_command(self, command: Command, *data: int) -> None:
        """Raw byte-writing.

        :param command: command for the printer.
        :param data: command arguments.
        """
        # The command
        if command is not Command.NONE:
            self.write(bytes([command.value]))

        # Its data
        for arg in data:
            self.write(bytes([arg]))
        sleep((1 + len(data)) * self._byte_time)

    def to_bytes(self, data: Any) -> bytes:
        """Convert data before sending to the printer.

        :param mixed data: any type of data to print.
        :return bytes: the converted data in bytes
        """
        if isinstance(data, (bool, int, float, complex)):
            data = str(data)
        elif isinstance(data, bytes):
            return data
        elif isinstance(data, bytearray):
            return bytes(data)
        elif isinstance(data, memoryview):
            return data.tobytes()

        encoding = "utf-8" if self._chinese else self._codepage.name
        try:
            return bytes(data, encoding, errors="replace")
        except LookupError:
            # Fall back to the most appropriate code page
            # >>> ls(CodePageConverted)
            encoding = CodePageConverted[self._codepage.name].value
            return bytes(data, encoding, errors="replace")

    # Printer's methods

    def barcode(self, data: str, barcode_type: BarCode) -> None:
        """Bar code printing. All checks are done to ensure the data validity.

        :param str data: data to print.
        :param BarCode barecode_type: bar code type to use.
        :exception ThermalPrinterValueError: On incorrect ``data``'s type or value.
        :exception ThermalPrinterConstantError: On bad ``barecode_type``'s type.
        """
        validate_barcode(data, barcode_type)
        code = barcode_type.value[0]
        self.send_command(Command.GS, 107, code, len(data))
        # Idea to test: use self.out()
        for char in data:
            self.write(bytes([ord(char)]))
        sleep((self._barcode_height + self._line_spacing) * self._dot_print_time)
        self.__lines += int(self._barcode_height / self._line_spacing) + 1

    def barcode_height(self, height: int = 162) -> None:
        """Set bar code height.

        :param int height: bar code height (min=1, max=255).
        :exception ThermalPrinterValueError: On incorrect ``height``'s type or value.
        """
        if not isinstance(height, int) or not 1 <= height <= 255:
            msg = "height should be between 1 and 255 (default: 162)."
            raise ThermalPrinterValueError(msg)

        if height != self._barcode_height:
            self._barcode_height = height
            self.send_command(Command.GS, 104, height)

    def barcode_left_margin(self, margin: int = 0) -> None:
        """Set the left margin of the bar code.

        :param int margin: left margin (min=0, max=255).
        :exception ThermalPrinterValueError: On incorrect ``margin``'s type or value.
        """
        if not isinstance(margin, int) or not 0 <= margin <= 255:
            msg = "margin should be between 0 and 255 (default: 0)."
            raise ThermalPrinterValueError(msg)

        if margin != self._barcode_left_margin:
            self._barcode_left_margin = margin
            self.send_command(Command.GS, 120, margin)

    def barcode_position(self, position: BarCodePosition = BarCodePosition.HIDDEN) -> None:
        """Set the position of the text relative to the bar code.

        :param BarCodePosition position: the position to use.
        :exception ThermalPrinterConstantError: On bad ``position``'s type.
        """
        validate_barcode_position(position)
        if position is not self._barcode_position:
            self._barcode_position = position
            self.send_command(Command.GS, 72, position.value)

    def barcode_width(self, width: int = 3) -> None:
        """Set the bar code width.

        :param int width: bar code with (min=2, max=6).
        :exception ThermalPrinterValueError: On incorrect ``width``'s type or value.
        """
        if not isinstance(width, int) or not 2 <= width <= 6:
            msg = "width should be between 2 and 6 (default: 3)."
            raise ThermalPrinterValueError(msg)

        if width != self._barcode_width:
            self._barcode_width = width
            self.send_command(Command.GS, 119, width)

    def bold(self, state: bool = False) -> None:
        """Turn emphasized mode on/off.

        :param bool state: new state.
        """
        if state is not self._bold:
            self._bold = state
            self.send_command(Command.ESC, 69, int(state))

    def charset(self, charset: CharSet = CharSet.USA) -> None:
        """Select an internal character set.

        :param CharSet charset: new charset to use.
        :exception ThermalPrinterConstantError: On bad ``charset``'s type.
        """
        validate_charset(charset)
        if charset is not self._charset:
            self._charset = charset
            self.send_command(Command.ESC, 82, charset.value)

    def char_spacing(self, spacing: int = 0) -> None:
        """Set the right character spacing.

        :param int spacing: spacing to use (min=0, max=255).
        :exception ThermalPrinterValueError: On incorrect ``spacing``'s type or value.
        """
        if not isinstance(spacing, int) or not 0 <= spacing <= 255:
            msg = "spacing should be between 0 and 255 (default: 0)."
            raise ThermalPrinterValueError(msg)

        if spacing != self._char_spacing:
            self._char_spacing = spacing
            self.send_command(Command.ESC, 32, spacing)

    def chinese(self, state: bool = False) -> None:
        """Select/cancel Chinese mode.

        :param bool state: new state.
        """
        if state is not self._chinese:
            self._chinese = state
            self.send_command(Command.FS, 38 if state else 46)

    def chinese_format(self, fmt: Chinese = Chinese.GBK) -> None:
        """Selection of the Chinese format.

        :param Chinese fmt: new format to use.
        :exception ThermalPrinterConstantError: On bad ``fmt``'s type.
        """
        validate_chinese_format(fmt)
        if fmt is not self._chinese_format:
            self._chinese_format = fmt
            self.send_command(Command.ESC, 57, fmt.value)

    def codepage(self, codepage: CodePage = CodePage.CP437) -> None:
        """Select character code table.

        :param CodePage codepage: new code page to use.
        :exception ThermalPrinterConstantError: On bad ``codepage``'s type.
        """
        validate_codepage(codepage)
        if not self._chinese and codepage is not self._codepage:
            self._codepage = codepage
            value, _ = codepage.value
            self.send_command(Command.ESC, 116, value)
            sleep(self._command_timeout)

    def double_height(self, state: bool = False) -> None:
        """Set double height mode.

        :param bool state: new state.
        """
        if state is not self._double_height:
            self._double_height = state
            self._char_height = 48 if state else 24
            self.send_command(Command.ESC, 33, 16 if state else 0)

    def double_width(self, state: bool = False) -> None:
        """Select double width mode.

        :param bool state: new state.
        """
        if state is not self._double_width:
            self._double_width = state
            self.__max_column = 16 if state else 32
            self.send_command(Command.ESC, 14 if state else 20, 1)

    def feed(self, number: int = 1) -> None:
        """Feeds by the specified number of lines.

        :param int number: number of lines (min=0, max=255).
        :exception ThermalPrinterValueError: On incorrect ``number``'s type or value.
        """
        if not isinstance(number, int) or not 0 <= number <= 255:
            msg = "number should be between 0 and 255 (default: 1)."
            raise ThermalPrinterValueError(msg)

        self.send_command(Command.ESC, 100, number)
        sleep(number * self._dot_feed_time * self._char_height)
        self.__feeds += number

    def flush(self, clear: bool = False) -> None:
        """Remove the print data in buffer.

        :param bool clear: set to ``True`` to also clear the receive buffer.
        """
        self.send_command(Command.ESC, 64)
        self.reset_output_buffer()
        sleep(self._command_timeout)
        if clear:
            self.reset_input_buffer()

    def image(self, image: Any) -> None:
        """Print Image. Requires Python Imaging Library (Pillow).
        Image will be cropped to 384 pixels width if
        necessary, and converted to 1-bit w/diffusion dithering.
        For any other behavior (scale, B&W threshold, etc.), use
        the Imaging Library to perform such operations before
        passing the result to this function.

        Max width: 384px.

        :param PIL.Image image: the PIL Image to use.

        Example:

            >>> from PIL import Image
            >>> printer.image(Image.open("picture.png"))
        """
        if image.mode != "1":
            image = image.convert("1")

        width = min(image.size[0], 384)
        height = image.size[1]
        row_bytes = int((width + 7) / 8)
        row_bytes_clipped = min(row_bytes, 48)
        bitmap = bytearray(row_bytes * height)
        pixels = image.load()

        for col in range(height):
            offset = col * row_bytes
            row = 0
            for pad in range(row_bytes):
                sum_ = 0
                bit = 128
                while bit > 0 and row < width:
                    if pixels[row, col] == 0:
                        sum_ |= bit
                    row += 1
                    bit >>= 1
                bitmap[offset + pad] = sum_

        idx = 0
        for row_start in range(0, height, 255):
            chunk_height = min(height - row_start, 255)
            self.send_command(Command.DC2, 42, chunk_height, row_bytes_clipped)
            for _ in range(chunk_height):
                for _ in range(row_bytes_clipped):
                    self.write(bytes([bitmap[idx]]))
                    idx += 1
                sleep(row_bytes_clipped * self._byte_time)
                idx += row_bytes - row_bytes_clipped

        self.__lines += height // self._line_spacing + 1

    def inverse(self, state: bool = False) -> None:
        """Turn white/black reverse printing mode.

        :param bool state: new state.
        """
        if state is not self._inverse:
            self._inverse = state
            self.send_command(Command.GS, 66, int(state))

    def justify(self, value: str = "L") -> None:
        """Set text justification.

        :param str value: the new justification.
            ``L`` to align left.
            ``C`` to align center.
            ``R`` to align right.
        :exception ThermalPrinterValueError: On incorrect ``value``'s type or value.
        """
        if not isinstance(value, str) or value not in "LCRlcr" or len(value) != 1:
            err = "value should be one of L (left, default), C (center)  or R (right)."
            raise ThermalPrinterValueError(err)

        value = value.upper()
        if value != self._justify:
            self._justify = value
            if value == "C":
                pos = 1
            elif value == "R":
                pos = 2
            else:
                pos = 0
            self.send_command(Command.ESC, 97, pos)

    def left_margin(self, margin: int = 0) -> None:
        """Set the left margin.

        :param int margin: the new margin (min=0, max=47).
        :exception ThermalPrinterValueError: On incorrect ``margin``'s type or value.
        """
        if not isinstance(margin, int) or not 0 <= margin <= 47:
            msg = "margin should be between 0 and 47 (default: 0)."
            raise ThermalPrinterValueError(msg)

        if margin != self._left_margin:
            self._left_margin = margin
            self.send_command(Command.ESC, 66, margin)

    def line_spacing(self, spacing: int = 30) -> None:
        """Set line spacing.

        :param int spacing: the new spacing (min=0, max=255).
        :exception ThermalPrinterValueError: On incorrect ``spacing``'s type or value.
        """
        if not isinstance(spacing, int) or not 0 <= spacing <= 255:
            msg = "spacing should be between 0 and 255 (default: 30)."
            raise ThermalPrinterValueError(msg)

        if spacing != self._line_spacing:
            self._line_spacing = spacing
            self.send_command(Command.ESC, 51, spacing)

    def offline(self) -> None:
        """Take the printer offline.
        Print commands sent after this will be ignored until :attr:`online()` is called.
        """
        if self.is_online:
            self.__is_online = False
            self.send_command(Command.ESC, 61, 0)

    def online(self) -> None:
        """Take the printer online.
        Subsequent print commands will be obeyed.
        """
        if not self.is_online:
            self.__is_online = True
            self.send_command(Command.ESC, 61, 1)

    def reset(self) -> None:
        """Reset the printer to factory defaults."""
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
        self._justify = "L"
        self._left_margin = 0
        self._line_spacing = 30
        self._rotate = False
        self._size = "S"
        self._strike = False
        self._underline = 0
        self._upside_down = False

    def rotate(self, state: bool = False) -> None:
        """Turn on/off clockwise rotation of 90°.

        :param bool state: new state.
        """
        if state is not self._rotate:
            self._rotate = state
            self.send_command(Command.ESC, 86, int(state))

    def size(self, value: str = "S") -> None:
        """Set text size.

        :param str value: the new text size.
            ``S`` for small.
            ``M`` for medium (double height).
            ``L`` for large (double width and height).
        :exception ThermalPrinterValueError: On incorrect ``value``'s type or value.

        :Note: This method affects :attr:`max_column`.
        """
        if not isinstance(value, str) or value not in "SMLsml" or len(value) != 1:
            err = "value should be one of S (small, default), M (medium)  or L (large)."
            raise ThermalPrinterValueError(err)

        value = value.upper()
        if value != self._size:
            self._size = value
            if value == "L":  # Large: double width and height
                size, self._char_height, self.__max_column = 0x11, 48, 16
            elif value == "M":  # Medium: double height
                size, self._char_height, self.__max_column = 0x01, 48, 32
            else:
                size, self._char_height, self.__max_column = 0x00, 24, 32

            self.send_command(Command.GS, 33, size)

    def sleep(self, seconds: int = 1) -> None:
        """Put the printer into a low-energy state.

        :param int seconds: value to pass to the printer (min=0).
        :exception ThermalPrinterValueError: On incorrect ``seconds``'s type or value.
        """
        if self.is_sleeping:
            return

        if not isinstance(seconds, int) or seconds < 0:
            msg = "seconds should be null or positive (default: 0)."
            raise ThermalPrinterValueError(msg)

        if seconds:
            self.__is_sleeping = True
        self.send_command(Command.ESC, 56, seconds, seconds >> 8)

    def status(self, raise_on_error: bool = True) -> dict[str, bool]:
        """Check the printer status.

        :param bool raise_on_error: raise on error.
        :exception ThermalPrinterCommunicationError:
            If RX pin is not connected and if ``raise_on_error`` is ``True``.
        :rtype: dict[str, bool]
        :return: A dict containing:

            - ``movement``: ``False`` if the movement is not connected
            - ``paper``: ``False`` if no paper
            - ``temp``: ``False`` if the temperature exceeds 60°C
            - ``voltage``: ``False`` if the voltage is higher than 9.5V

        .. versionchanged:: 0.2.0
           Added ``raise_on_error`` keyword argument.
        """
        ret = {"movement": True, "paper": True, "temp": True, "voltage": True}
        self.send_command(Command.ESC, 118, 0)
        sleep(self._command_timeout)
        if self.in_waiting:
            stat = ord(self.read(1))
            ret["movement"] = stat & 0b00000001 == 1
            ret["paper"] = stat & 0b00000100 == 0
            ret["voltage"] = stat & 0b00001000 == 0
            ret["temp"] = stat & 0b01000000 == 0
        elif raise_on_error:
            raise ThermalPrinterCommunicationError

        return ret

    def strike(self, state: bool = False) -> None:
        """Turn on/off double-strike mode.

        :param bool state: new state.
        """
        if state is not self._strike:
            self._strike = state
            self.send_command(Command.ESC, 71, int(state))

    def test(self) -> None:
        """Print the test page (contains printer's settings)."""
        self.send_command(Command.DC2, 84)
        sleep(self._dot_print_time * 24 * 26 + self._dot_feed_time * (8 * 26 + 32))

    def underline(self, weight: int = 0) -> None:
        """Turn underline mode on/off.

        :param int weight: the underline's weight.
            ``0`` will turn off underline mode.
            ``1`` will turn on underline mode (1 dot thick).
            ``2`` will turns on underline mode (2 dots thick).
        :exception ThermalPrinterValueError: On incorrect ``weight``'s type or value.
        """
        if not isinstance(weight, int) or not 0 <= weight <= 2:
            msg = "weight should be between 0 and 2 (default: 0)."
            raise ThermalPrinterValueError(msg)

        if weight != self._underline:
            self._underline = weight
            self.send_command(Command.ESC, 45, weight)

    def upside_down(self, state: bool = False) -> None:
        """Turns on/off upside-down printing mode.

        :param bool state: new state.
        """
        if state is not self._upside_down:
            self._upside_down = state
            self.send_command(Command.ESC, 123, int(state))

    def wake(self) -> None:
        """Wake up the printer."""
        if self.is_sleeping:
            self.__is_sleeping = False
            self.send_command(Command.NONE, 255)
            sleep(self._command_timeout)  # Sleep 50ms as in documentation
            self.sleep(0)  # SLEEP OFF - IMPORTANT!

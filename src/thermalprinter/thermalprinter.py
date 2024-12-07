"""This is part of the Python's module to manage the DP-EH600 thermal printer.
Source: https://github.com/BoboTiG/thermalprinter.
"""

from __future__ import annotations

from atexit import register
from time import sleep
from typing import TYPE_CHECKING

from serial import Serial

from thermalprinter.constants import (
    DEFAULT_BAUDRATE,
    DEFAULT_HEAT_INTERVAL,
    DEFAULT_HEAT_TIME,
    DEFAULT_MOST_HEATED_POINT,
    DEFAULT_PORT,
    BarCodePosition,
    CharSet,
    Chinese,
    CodePage,
    CodePageConverted,
    Command,
    Justify,
    Size,
    Underline,
)
from thermalprinter.exceptions import ThermalPrinterCommunicationError, ThermalPrinterValueError
from thermalprinter.validate import (
    validate_barcode,
    validate_barcode_position,
    validate_charset,
    validate_chinese_format,
    validate_codepage,
)

if TYPE_CHECKING:
    from types import TracebackType
    from typing import Any

    from thermalprinter.constants import BarCode


class ThermalPrinter(Serial):
    """
    The class managing the thermal printer.

    :param str port: Serial port to use, known as the device name.
    :param int baudrate: Baud rate.
    :param float command_timeout: Command timeout, in seconds.
    :param int heat_time: Printer heat time.
    :param int heat_interval: Printer heat time interval.
    :param int most_heated_point: Printer most heated point.
    :param bool run_setup_cmd: Set to ``False`` to disable the automatic one-shot run of the printer settings command (that ay be problematic on some devices).
    :param flat sleep_sec_after_init: Initial *mandatory* time-to-wait right after the serial initialisation.

    :exception ThermalPrinterValueError: On incorrect argument's type, or value.

    .. versionadded:: 0.3.0
        The ``command_timeout`` keyword-argument.

    .. versionadded:: 0.4.0
        ``run_setup_cmd``, and ``sleep_sec_after_init``, keyword-arguments.
    """  # noqa: E501

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
    _justify = Justify.LEFT
    _left_margin = 0
    _line_spacing = 30
    _rotate = False
    _size = Size.SMALL
    _strike = False
    _underline = Underline.OFF
    _upside_down = False

    def __init__(  # noqa: PLR0913
        self,
        port: str = DEFAULT_PORT,
        *,
        baudrate: int = DEFAULT_BAUDRATE,
        command_timeout: float = 0.05,
        heat_interval: int = DEFAULT_HEAT_INTERVAL,
        heat_time: int = DEFAULT_HEAT_TIME,
        most_heated_point: int = DEFAULT_MOST_HEATED_POINT,
        run_setup_cmd: bool = True,
        sleep_sec_after_init: float = 0.5,
    ) -> None:
        # Few important values
        self.is_open = False
        self._baudrate = baudrate
        self._byte_time = 11.0 / float(self._baudrate)
        self._dot_feed_time = 0.0021
        self._dot_print_time = 0.03
        self._command_timeout = command_timeout
        self._heat_time = heat_time
        self._heat_interval = heat_interval
        self._most_heated_point = most_heated_point

        # Several checks
        error = ""
        if not 0 <= heat_time <= 255:
            error = f"heat_time should be between 0 and 255 (default: {DEFAULT_HEAT_TIME})."
        elif not 0 <= heat_interval <= 255:
            error = f"heat_interval should be between 0 and 255 (default: {DEFAULT_HEAT_INTERVAL})."
        elif not 0 <= most_heated_point <= 255:
            error = f"most_heated_point should be between 0 and 255 (default: {DEFAULT_MOST_HEATED_POINT})."
        if error:
            raise ThermalPrinterValueError(error)

        # Init the serial
        super().__init__(port=port, baudrate=self._baudrate)
        sleep(sleep_sec_after_init)  # Important
        register(self._on_exit)

        # Printer settings
        if run_setup_cmd:
            self.init(self._heat_time)

        # Factory settings
        self.reset()

    def __enter__(self) -> ThermalPrinter:  # noqa: PYI034
        """`with ThermalPrinter() as printer:`."""
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self._on_exit()

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
            f"baudrate={self.baudrate}",
            f"is_open={self.is_open}",
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
    def has_paper(self) -> bool:
        """Return ``True`` if there is paper."""
        return self.status(raise_on_error=False)["paper"]

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
        """Number of printed lines."""
        return self.__lines

    @property
    def feeds(self) -> int:
        """Number of printed line feeds."""
        return self.__feeds

    @property
    def max_column(self) -> int:
        """Number of printable characters on one line."""
        return self.__max_column

    # Module's methods

    def out(self, data: Any, *, line_feed: bool = True, **kwargs: Any) -> None:
        """Send one line to the printer.

        :param mixed data: The data to print.
        :param bool line_feed: Send a line break after the printed data.
        :param dict kwargs: Additional styles to apply.

        You can pass formatting instructions directly via arguments:

        >>> printer.out(data, justify=Justify.CENTER, inverse=True)

        This is a quicker way to do:

        >>> printer.justify(Justify.CENTER)
        >>> printer.inverse(True)
        >>> printer.out(data)
        >>> printer.inverse(False)
        >>> printer.justify(Justify.LEFT)
        """
        # Apply styles
        for style, value in kwargs.items():
            getattr(self, style)(value)

        self.write(self.to_bytes(data))

        if line_feed:
            self.write(b"\n")
            self.__lines += 1

            # Sizes M and L are double height
            if self._size != Size.SMALL:
                self.__lines += 1

        sleep(2 * self._dot_feed_time * self._char_height)

        # Restore default styles
        for style in kwargs:
            getattr(self, style)()

    def send_command(self, command: Command, *args: int) -> None:
        """Send a command to the printer.

        :param Command command: The command to send to the printer.
        :param list[int] args: Eventual command arguments.
        """
        if command is not Command.NONE:
            self.write(bytes([command.value]))

        for arg in args:
            self.write(bytes([arg]))

        sleep((1 + len(args)) * self._byte_time)

    def to_bytes(self, data: Any) -> bytes:
        """Convert data before sending to the printer.

        :param mixed data: Any type of data to print.
        :return bytes: The converted data in bytes
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
        """Barcode printing. All checks are done to ensure the data validity.

        :param str data: The data to print.
        :param BarCode barecode_type: The barcode type to use.
        :exception ThermalPrinterValueError: On incorrect ``data``'s type, or value.
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
        """Set the barcode height.

        :param int height: The barcode height (min=1, max=255).
        :exception ThermalPrinterValueError: On incorrect ``height``'s type, or value.
        """
        if not isinstance(height, int) or not 1 <= height <= 255:
            msg = "height should be between 1 and 255 (default: 162)."
            raise ThermalPrinterValueError(msg)

        if height != self._barcode_height:
            self._barcode_height = height
            self.send_command(Command.GS, 104, height)

    def barcode_left_margin(self, margin: int = 0) -> None:
        """Set the left margin of the barcode.

        :param int margin: The barcode left margin (min=0, max=255).
        :exception ThermalPrinterValueError: On incorrect ``margin``'s type, or value.
        """
        if not isinstance(margin, int) or not 0 <= margin <= 255:
            msg = "margin should be between 0 and 255 (default: 0)."
            raise ThermalPrinterValueError(msg)

        if margin != self._barcode_left_margin:
            self._barcode_left_margin = margin
            self.send_command(Command.GS, 120, margin)

    def barcode_position(self, position: BarCodePosition = BarCodePosition.HIDDEN) -> None:
        """Set the position of the text relative to the barcode.

        :param BarCodePosition position: The barcode position to use.
        :exception ThermalPrinterConstantError: On bad ``position``'s type.
        """
        validate_barcode_position(position)
        if position is not self._barcode_position:
            self._barcode_position = position
            self.send_command(Command.GS, 72, position.value)

    def barcode_width(self, width: int = 3) -> None:
        """Set the barcode width.

        :param int width: The barcode with (min=2, max=6).
        :exception ThermalPrinterValueError: On incorrect ``width``'s type, or value.
        """
        if not isinstance(width, int) or not 2 <= width <= 6:
            msg = "width should be between 2 and 6 (default: 3)."
            raise ThermalPrinterValueError(msg)

        if width != self._barcode_width:
            self._barcode_width = width
            self.send_command(Command.GS, 119, width)

    def bold(self, state: bool = False) -> None:
        """Turn on/off the emphasized mode.

        :param bool state: Enabled if ``state`` is ``True``, else disabled.
        """
        if state is not self._bold:
            self._bold = state
            self.send_command(Command.ESC, 69, int(state))

    def charset(self, charset: CharSet = CharSet.USA) -> None:
        """Set the character set.

        :param CharSet charset: The new charset to use.
        :exception ThermalPrinterConstantError: On bad ``charset``'s type.
        """
        validate_charset(charset)
        if charset is not self._charset:
            self._charset = charset
            self.send_command(Command.ESC, 82, charset.value)

    def char_spacing(self, spacing: int = 0) -> None:
        """Set the character spacing.

        :param int spacing: The spacing to use (min=0, max=255).
        :exception ThermalPrinterValueError: On incorrect ``spacing``'s type, or value.
        """
        if not isinstance(spacing, int) or not 0 <= spacing <= 255:
            msg = "spacing should be between 0 and 255 (default: 0)."
            raise ThermalPrinterValueError(msg)

        if spacing != self._char_spacing:
            self._char_spacing = spacing
            self.send_command(Command.ESC, 32, spacing)

    def chinese(self, state: bool = False) -> None:
        """Turn on/off Chinese mode.

        :param bool state: Enabled if ``state`` is ``True``, else disabled.
        """
        if state is not self._chinese:
            self._chinese = state
            self.send_command(Command.FS, 38 if state else 46)

    def chinese_format(self, fmt: Chinese = Chinese.GBK) -> None:
        """Set the Chinese format.

        :param Chinese fmt: The new Chinese format to use.
        :exception ThermalPrinterConstantError: On bad ``fmt``'s type.
        """
        validate_chinese_format(fmt)
        if fmt is not self._chinese_format:
            self._chinese_format = fmt
            self.send_command(Command.ESC, 57, fmt.value)

    def codepage(self, codepage: CodePage = CodePage.CP437) -> None:
        """Set the character code table.

        :param CodePage codepage: The new code page to use.
        :exception ThermalPrinterConstantError: On bad ``codepage``'s type.
        """
        validate_codepage(codepage)
        if not self._chinese and codepage is not self._codepage:
            self._codepage = codepage
            value, _ = codepage.value
            self.send_command(Command.ESC, 116, value)
            sleep(self._command_timeout)

    def double_height(self, state: bool = False) -> None:
        """Turn on/off the double height mode.

        :param bool state: Enabled if ``state`` is ``True``, else disabled.
        """
        if state is not self._double_height:
            self._double_height = state
            self._char_height = 48 if state else 24
            self.send_command(Command.ESC, 33, 16 if state else 0)

    def double_width(self, state: bool = False) -> None:
        """Turn on/off the double width mode.

        :param bool state: Enabled if ``state`` is ``True``, else disabled.
        """
        if state is not self._double_width:
            self._double_width = state
            self.__max_column = 16 if state else 32
            self.send_command(Command.ESC, 14 if state else 20, 1)

    def feed(self, number: int = 1) -> None:
        """Feed by the specified number of lines.

        :param int number: The number of lines (min=0, max=255).
        :exception ThermalPrinterValueError: On incorrect ``number``'s type, or value.
        """
        if not isinstance(number, int) or not 0 <= number <= 255:
            msg = "number should be between 0 and 255 (default: 1)."
            raise ThermalPrinterValueError(msg)

        self.send_command(Command.ESC, 100, number)
        sleep(number * self._dot_feed_time * self._char_height)
        self.__feeds += number

    def flush(self, clear: bool = False) -> None:
        """Remove the print data from the output buffer.

        :param bool clear: Set to ``True`` to also clear the input buffer.
        """
        self.send_command(Command.ESC, 64)
        self.reset_output_buffer()
        sleep(self._command_timeout)
        if clear:
            self.reset_input_buffer()

    def image(self, image: Any) -> None:
        """Picture printing. Requires the Python Imaging Library (Pillow).
        The image will be cropped to 384 pixels width if
        necessary, and converted to 1-bit w/diffusion dithering.
        For any other behavior (scale, B&W threshold, etc.), use
        the Imaging Library to perform such operations before
        passing the result to this function.

        Max width: 384px.

        :param PIL.Image image: The PIL Image object to use.

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

    def init(self, heat_time: int) -> None:
        """Set printer heat properties.

        :param int heat_time: Printer heat time.
        """
        self.send_command(Command.ESC, 55, self._most_heated_point, heat_time, self._heat_interval)

    def inverse(self, state: bool = False) -> None:
        """Turn on/off the white/black reverse printing mode.

        :param bool state: Enabled if ``state`` is ``True``, else disabled.
        """
        if state is not self._inverse:
            self._inverse = state
            self.send_command(Command.GS, 66, int(state))

    def justify(self, value: Justify = Justify.LEFT) -> None:
        """Set the text justification.

        .. versionchanged:: 0.4.0
            The ``value`` keyword-argument was converted from a :obj:`str` to :const:`constants.Justify`.
        """
        if value != self._justify:
            self._justify = value
            self.send_command(Command.ESC, 97, value.value)

    def left_margin(self, margin: int = 0) -> None:
        """Set the left margin.

        :param int margin: The new margin (min=0, max=47).
        :exception ThermalPrinterValueError: On incorrect ``margin``'s type, or value.
        """
        if not isinstance(margin, int) or not 0 <= margin <= 47:
            msg = "margin should be between 0 and 47 (default: 0)."
            raise ThermalPrinterValueError(msg)

        if margin != self._left_margin:
            self._left_margin = margin
            self.send_command(Command.ESC, 66, margin)

    def line_spacing(self, spacing: int = 30) -> None:
        """Set the line spacing.

        :param int spacing: The new spacing (min=0, max=255).
        :exception ThermalPrinterValueError: On incorrect ``spacing``'s type, or value.
        """
        if not isinstance(spacing, int) or not 0 <= spacing <= 255:
            msg = "spacing should be between 0 and 255 (default: 30)."
            raise ThermalPrinterValueError(msg)

        if spacing != self._line_spacing:
            self._line_spacing = spacing
            self.send_command(Command.ESC, 51, spacing)

    def offline(self) -> None:
        """Take the printer offline.
        Upcoming print commands issued will be ignored until :attr:`online()` is called.
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
        self._justify = Justify.LEFT
        self._left_margin = 0
        self._line_spacing = 30
        self._rotate = False
        self._size = Size.SMALL
        self._strike = False
        self._underline = Underline.OFF
        self._upside_down = False

    def rotate(self, state: bool = False) -> None:
        """Turn on/off 90° clockwise rotation.

        :param bool state: Enabled if ``state`` is ``True``, else disabled.
        """
        if state is not self._rotate:
            self._rotate = state
            self.send_command(Command.ESC, 86, int(state))

    def size(self, value: Size = Size.SMALL) -> None:
        """Set the text size.

        .. versionchanged:: 0.4.0
            The ``value`` keyword-argument was converted from a :obj:`str` to :const:`constants.Size`.

        .. note::
            This method affects :attr:`max_column`.
        """
        if value != self._size:
            self._size = value
            size, self._char_height, self.__max_column = value.value
            self.send_command(Command.GS, 33, size)

    def sleep(self, seconds: int = 1) -> None:
        """Put the printer into a low-energy state.

        :param int seconds: Value to pass to the printer (min=0).
        :exception ThermalPrinterValueError: On incorrect ``seconds``'s type, or value.
        """
        if self.is_sleeping:
            return

        if not isinstance(seconds, int) or seconds < 0:
            msg = "seconds should be null or positive (default: 0)."
            raise ThermalPrinterValueError(msg)

        if seconds:
            self.__is_sleeping = True
        self.send_command(Command.ESC, 56, seconds, seconds >> 8)

    def status(self, *, raise_on_error: bool = True) -> dict[str, bool]:
        """Return the printer status.

        :param bool raise_on_error: Raise on error.
        :exception ThermalPrinterCommunicationError:
            If the RX pin is not connected, and if ``raise_on_error`` is ``True``.
        :rtype: dict[str, bool]
        :return: A dict containing:

            - ``movement``: ``False`` if the movement is not connected
            - ``paper``: ``False`` if no paper
            - ``temp``: ``False`` if the temperature exceeds 60°C
            - ``voltage``: ``False`` if the voltage is higher than 9.5V

        .. versionadded:: 0.2.0
           The ``raise_on_error`` keyword-argument.
        """
        ret = {"movement": False, "paper": False, "temp": False, "voltage": False}
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
        """Turn on/off the double-strike mode.

        :param bool state: Enabled if ``state`` is ``True``, else disabled.
        """
        if state is not self._strike:
            self._strike = state
            self.send_command(Command.ESC, 71, int(state))

    def test(self) -> None:
        """Print the test page (including printer's settings)."""
        self.send_command(Command.DC2, 84)
        sleep(self._dot_print_time * 24 * 26 + self._dot_feed_time * (8 * 26 + 32))

    def underline(self, weight: Underline = Underline.OFF) -> None:
        """Set the underline mode.

        .. versionchanged:: 0.4.0
            The ``weight`` keyword-argument was converted from an :obj:`int` to :const:`constants.Underline`.
        """
        if weight != self._underline:
            self._underline = weight
            self.send_command(Command.ESC, 45, weight.value)

    def upside_down(self, state: bool = False) -> None:
        """Turns on/off the upside-down printing mode.

        :param bool state: Enabled if ``state`` is ``True``, else disabled.
        """
        if state is not self._upside_down:
            self._upside_down = state
            self.send_command(Command.ESC, 123, int(state))

    def wake(self) -> None:
        """Wake up the printer."""
        if self.is_sleeping:
            self.__is_sleeping = False
            self.send_command(Command.NONE, 255)
            sleep(self._command_timeout)  # Sleep 50ms as in the documentation
            self.sleep(0)  # Sleep off - important!

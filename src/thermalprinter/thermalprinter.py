"""This is part of the Python's module to manage the DP-EH600 thermal printer.
Source: https://github.com/BoboTiG/thermalprinter.
"""

from __future__ import annotations

import math
from atexit import register
from logging import getLogger
from pathlib import Path
from time import sleep
from typing import TYPE_CHECKING

from serial import Serial

from thermalprinter.constants import *
from thermalprinter.exceptions import ThermalPrinterCommunicationError, ThermalPrinterValueError
from thermalprinter.tools import stats_save

if TYPE_CHECKING:
    from types import TracebackType
    from typing import Any

    from _typeshed import ReadableBuffer


log = getLogger(__name__)

GNU_FILE = Path(__file__).parent / "gnu.png"


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
    :param bool use_stats: Set to ``False`` to disable statistics persistence.

    :exception ThermalPrinterValueError: On incorrect argument's type, or value.

    .. versionadded:: 0.3.0
        The ``command_timeout`` keyword-argument.

    .. versionadded:: 1.0.0
        ``run_setup_cmd``, and ``sleep_sec_after_init``, ``use_stats``, keyword-arguments.
    """  # noqa: E501

    # Counters
    __lines: int = 0
    __feeds: int = 0

    # Default values
    __max_column = 32
    __is_online = True
    __is_sleeping = False
    _barcode_height = Defaults.BARCODE_HEIGHT.value
    _barcode_left_margin = 0
    _barcode_position = BarCodePosition.HIDDEN
    _barcode_width = Defaults.BARCODE_WIDTH.value
    _bold = False
    _charset = CharSet.USA
    _char_spacing = 0
    _char_height = 24
    _chinese = False
    _chinese_format = Chinese.GBK
    _codepage = CodePage.CP437
    _double_height = False
    _double_width = False
    _font_b = False
    _inverse = False
    _justify = Justify.LEFT
    _left_blank = 0
    _left_margin = 0
    _line_spacing = Defaults.LINE_SPACING.value
    _rotate = False
    _size = Size.SMALL
    _strike = False
    _underline = Underline.OFF
    _upside_down = False

    def __init__(  # noqa: PLR0913
        self,
        port: str = Defaults.PORT.value,
        *,
        baudrate: int = Defaults.BAUDRATE.value,
        byte_time: float = Defaults.BYTE_TIME.value,
        command_timeout: float = 0.05,
        dot_feed_time: float = Defaults.DOT_FEED_TIME.value,
        dot_print_time: float = Defaults.DOT_PRINT_TIME.value,
        heat_interval: int = Defaults.HEAT_INTERVAL.value,
        heat_time: int = Defaults.HEAT_TIME.value,
        most_heated_point: int = Defaults.MOST_HEATED_POINT.value,
        run_setup_cmd: bool = True,
        sleep_sec_after_init: float = 0.5,
        use_stats: bool = True,
    ) -> None:
        # Few important values
        self.is_open = False
        self._baudrate = baudrate
        self._byte_time = byte_time
        self._dot_feed_time = dot_feed_time
        self._dot_print_time = dot_print_time
        self._command_timeout = command_timeout
        self._heat_time = heat_time
        self._heat_interval = heat_interval
        self._most_heated_point = most_heated_point
        self._use_stats = use_stats

        # Several checks
        msg = ""
        if not 0 <= heat_time <= 255:
            msg = f"heat_time should be between 0 and 255 (default: {Defaults.HEAT_TIME.value})."
        elif not 0 <= heat_interval <= 255:
            msg = f"heat_interval should be between 0 and 255 (default: {Defaults.HEAT_INTERVAL.value})."
        elif not 0 <= most_heated_point <= 255:
            msg = f"most_heated_point should be between 0 and 255 (default: {Defaults.MOST_HEATED_POINT.value})."
        if msg:
            raise ThermalPrinterValueError(msg)

        # Init the serial
        super().__init__(port=port, baudrate=baudrate, timeout=0, write_timeout=0, dsrdtr=True)
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
        if self._use_stats and (self.lines or self.feeds):
            stats_save(self)
            self.__feeds = 0
            self.__lines = 0

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

        return f"{type(self).__name__}<{', '.join(sorted(settings))}>({', '.join(sorted(states))})"

    def read(self, size: int = 1) -> bytes:
        res = super().read(size=size)
        log.debug(" <<< READ %r", res)
        return res

    def write(self, b: ReadableBuffer, /) -> int | None:
        log.debug(" >>> WRITE %r", b)
        while self.out_waiting:
            pass
        return super().write(b)

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

    def out(self, data: Any, **kwargs: Any) -> None:
        """Send one line to the printer.

        :param mixed data: The data to print.
        :param dict kwargs: Additional styles to apply.

        You can pass formatting instructions directly via arguments:

        >>> self.out(data, justify=Justify.CENTER, inverse=True)

        This is a quicker way to do:

        >>> printer.justify(Justify.CENTER)
        >>> printer.inverse(True)
        >>> self.out(data)
        >>> printer.inverse(False)
        >>> printer.justify(Justify.LEFT)
        """
        log.debug("Line: %r (%s)", data, ", ".join(f"{k}={v}" for k, v in kwargs.items()))

        # Apply styles
        for style, value in kwargs.items():
            log.debug("Apply style: %s: %r", style, value)
            getattr(self, style)(value)

        self.write(self.to_bytes(data) + b"\n")
        self.__lines += 1

        # Sizes M, and L, are double height
        if self._size is not Size.SMALL:
            self.__lines += 1

        sleep(2 * self._dot_feed_time * self._char_height)

        # Restore default styles
        for style in kwargs:
            log.debug("Restore style: %s", style)
            getattr(self, style)()

    def send_command(self, command: Command, *args: int) -> None:
        """Send a command to the printer.

        :param Command command: The command to send to the printer.
        :param list[int] args: Eventual command arguments.
        """
        data = []
        if command is not Command.NONE:
            log.debug("Command: %s %s", command.name, ", ".join(str(arg) for arg in args))
            data.append(bytes([command.value]))
        else:
            log.debug("Command: %s", ", ".join(str(arg) for arg in args))

        data.extend(bytes([arg]) for arg in args)
        self.write(b"".join(data))

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

    @staticmethod
    def validate_barcode(data: str, barcode_type: BarCode) -> None:
        """Validate data against the barcode type.

        :param str data: The data to print.
        :param BarCode barecode_type: The barcode type to validate.
        :exception ThermalPrinterValueError: On incorrect ``data``'s type, or value.
        """

        def _range0(min_: int = 48, max_: int = 57) -> list[int]:
            return list(range(min_, max_ + 1))

        def _range1() -> list[int]:
            range_ = [32, 36, 37, 43]
            range_.extend(_range0(45, 57))
            range_.extend(_range0(65, 90))
            return range_

        def _range2() -> list[int]:
            range_ = [36, 43]
            range_.extend(_range0(45, 58))
            range_.extend(_range0(65, 68))
            return range_

        def _range3() -> list[int]:
            return _range0(0, 127)

        _, (min_, max_), range_type = barcode_type.value
        data_len = len(data)
        range_: list[int] = [_range0, _range1, _range2, _range3][range_type]()  # type: ignore[operator]

        if not min_ <= data_len <= max_:
            msg = f"[{barcode_type.name}] Should be {min_} <= len(data) <= {max_} (current: {data_len})."
            raise ThermalPrinterValueError(msg)

        if barcode_type is BarCode.ITF and data_len % 2 != 0:
            msg = "[BarCode.ITF] len(data) must be even."
            raise ThermalPrinterValueError(msg)

        if any(ord(char) not in range_ for char in data):
            valid = map(chr, range_) if range_type != 3 else map(hex, range_)
            err = f"[{barcode_type.name}] Valid characters: {', '.join(valid)}."
            raise ThermalPrinterValueError(err)

    # Printer's methods

    def barcode(self, data: str, barcode_type: BarCode, **kwargs: Any) -> None:
        """Barcode printing. All checks are done to ensure the data validity.

        :param str data: The data to print.
        :param BarCode barecode_type: The barcode type to use.
        :param dict kwargs: Additional barcode properties to apply.
        :exception ThermalPrinterValueError: On incorrect ``data``'s type, or value.

        You can set additional barcode properties via arguments:

        >>> self.barcode("012345678901", BarCode.EAN13, width=3, height=80, position=BarCodePosition.BELOW)

        This is a quicker way to do:

        >>> printer.barcode_width(3)
        >>> printer.barcode_height(80)
        >>> printer.barcode_position(BarCodePosition.BELOW)
        >>> printer.barcode("012345678901", BarCode.EAN13)
        """
        self.validate_barcode(data, barcode_type)

        # Set barcode properties, if any
        for prop, value in kwargs.items():
            log.debug("Apply barcode property: %s: %r", prop, value)
            getattr(self, f"barcode_{prop}")(value)

        self.send_command(Command.GS, 107, barcode_type.value[0], len(data))
        for char in data:
            self.write(bytes([ord(char)]))

        sleep((self._barcode_height + self._line_spacing) * self._dot_print_time)
        self.__lines += int(self._barcode_height / self._line_spacing) + 1

    def barcode_height(self, height: int = Defaults.BARCODE_HEIGHT.value) -> None:
        """Set the barcode height.

        :param int height: The barcode height (min=1, max=255).
        :exception ThermalPrinterValueError: On incorrect ``height``'s type, or value.
        """
        if not isinstance(height, int) or not 1 <= height <= 255:
            msg = f"height should be between 1 and 255 (default: {Defaults.BARCODE_HEIGHT.value})."
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
        """
        if position is not self._barcode_position:
            self._barcode_position = position
            self.send_command(Command.GS, 72, position.value)

    def barcode_width(self, width: int = Defaults.BARCODE_WIDTH.value) -> None:
        """Set the barcode width.

        :param int width: The barcode with (min=2, max=6).
        :exception ThermalPrinterValueError: On incorrect ``width``'s type, or value.
        """
        if not isinstance(width, int) or not 2 <= width <= 6:
            msg = f"width should be between 2 and 6 (default: {Defaults.BARCODE_WIDTH.value})."
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

    def calibrate(self, *, with_info: bool = True) -> None:
        """Thermal calibration.

        Run this method before using the printer for the first time, any
        time a different power supply is used, or when using paper from a
        different source.

        Prints a series of black bars with increasing "heat time" settings.
        Because printed sections have different "grip" characteristics than
        blank paper, as this progresses the paper will usually at some point
        jam -- either uniformly, making a short bar, or at one side or the
        other, making a wedge shape. In some cases, the Raspberry Pi may reset
        for lack of power.

        Whatever the outcome, take the last number printed **before** any
        distorted bar, and use that value as ``heat_time`` keyword-argument
        when instantiating the printer.

        :param ThermalPrinter printer: Optional printer to use.
        :param bool with_info: Set to ``False`` to skip displaying the information.

        .. note::
            Source: [adafruit/Python-Thermal-Printer](https://github.com/adafruit/Python-Thermal-Printer/blob/master/calibrate.py)
        """
        if with_info:
            print(str(self.calibrate.__doc__).split(":param", 1)[0])

        for heat_time in range(0, 256, 15):
            self.init(heat_time)
            self.out(heat_time)
            self.out(" " * self.max_column, inverse=True)
        self.feed(2)

    def charset(self, charset: CharSet = CharSet.USA) -> None:
        """Set the character set.

        :param CharSet charset: The new charset to use.
        """
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
        """
        if fmt is not self._chinese_format:
            self._chinese_format = fmt
            self.send_command(Command.ESC, 57, fmt.value)

    def codepage(self, codepage: CodePage = CodePage.CP437) -> None:
        """Set the character code table.

        :param CodePage codepage: The new code page to use.
        """
        if not self._chinese and codepage is not self._codepage:
            self._codepage = codepage
            value, _ = codepage.value
            self.send_command(Command.ESC, 116, value)
            sleep(self._command_timeout)

    def demo(self) -> None:
        """Show time!

        Demonstrate printer capabilities.
        """

        # Image
        try:
            from PIL import Image
        except ImportError:
            print("The PIL module is not installed, skipping the image demo.")
        else:
            self.feed()
            self.image(Image.open(GNU_FILE))
            self.feed()

        # Barcode
        self.barcode("012345678901", BarCode.EAN13, width=4, height=80, position=BarCodePosition.BELOW)

        # Style
        self.out("Bold", bold=True)
        self.out("Double height", double_height=True)
        self.out("Double width", double_width=True)
        self.out("Font B mode", font_b=True)
        self.out("Inverse", inverse=True)
        self.out("Rotate 90°", rotate=True, codepage=CodePage.ISO_8859_1)
        self.out("Size LARGE", size=Size.LARGE)
        self.out("Strike", strike=True)
        self.out("Underline", underline=Underline.THIN)
        self.out("Upside down", upside_down=True)
        self.out("Left margin", left_margin=5)
        self.out("Left blank", left_blank=10)

        # Chinese (almost all alphabets exist)
        self.out("现代汉语通用字表", chinese=True, chinese_format=Chinese.UTF_8)

        # Greek (excepted the ΐ character)
        self.out("Στην υγειά μας!", codepage=CodePage.CP737)

        # Other character
        self.out(b"Cards \xe8 \xe9 \xea \xeb", codepage=CodePage.CP932)

        # Accent
        self.out(
            "Voilà !",
            codepage=CodePage.ISO_8859_1,
            justify=Justify.CENTER,
            strike=True,
            underline=Underline.THICK,
        )

        self.feed(2)

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

    def font_b(self, state: bool = False) -> None:
        """Turn on/off the font B mode.

        :param bool state: Enabled if ``state`` is ``True``, else disabled.
        """
        if state is not self._font_b:
            self._font_b = state
            self.send_command(Command.ESC, 33, int(state))

    def image(self, image: Any) -> None:
        """Picture printing.

        Requires the Python Imaging Library (Pillow).
        The image will be resized to 384 pixels width (:const:`constants.MAX_IMAGE_WIDTH`)
        if necessary, and converted to 1-bit without diffusion dithering.

        :param PIL.Image image: The PIL Image object to print.

        Example:

        >>> from PIL import Image
        >>> printer.image(Image.open("picture.png"))

        .. tip::
            Since **v1.0** the image will be automatically resized when too wide.
        """
        image = self.image_convert(image)
        image = self.image_resize(image)
        bitmap = self.image_chunks(image)

        width, height = image.size
        row_bytes = int((width + 7) / 8)  # Round up to next byte boundary

        self.send_command(
            Command.GS,
            118,
            48,
            0,
            int(row_bytes % 256),
            int(row_bytes / 256),
            int(height % 256),
            int(height / 256),
        )

        i = 0
        for _ in range(height):
            for _ in range(row_bytes):
                self.write(bytes([bitmap[i]]))
                i += 1
        sleep(height * self._dot_print_time)

        self.__lines += height // self._line_spacing + 1

    def image_convert(self, image: Any) -> Any:
        """Convert a given ``image`` to 1-bit without diffusion dithering, *if necessary*.

        :param PIL.Image image: The PIL Image object to convert.
        :rtype: PIL.Image
        :return: The converted image object, if converted, else the original ``image``.

        .. hint::
            Usually you do not need to call this method manually. It is used automatically
            by the :func:`image()` method.
        """
        if image.mode == "1":
            return image

        from PIL.Image import Dither

        new_mode = "1"
        log.info("Image converted from %r to %r", image.mode, new_mode)
        return image.convert(new_mode, dither=Dither.NONE)

    def image_chunks(self, image: Any) -> bytearray:
        """Convert a given ``image`` to 1-bit without diffusion dithering, *if necessary*.

        :param PIL.Image image: The PIL Image object to convert.
        :rtype: PIL.Image
        :return: The converted image object, if converted, else the original ``image``.

        .. hint::
            Usually you do not need to call this method manually. It is used automatically
            by the :func:`image()` method.
        """
        width, height = image.size
        chunks = math.ceil(width / 8)
        bitmap = bytearray()

        for y in range(height):
            for chunk in range(chunks):
                start = chunk * 8
                byte = 0
                for shift, x in enumerate(range(start, start + 8)):
                    pixel = image.getpixel((x, y)) if x < image.width else 1
                    byte |= int(not pixel) << (7 - shift)
                bitmap.append(byte)

        return bitmap

    def image_resize(self, image: Any) -> Any:
        """Resize a given ``image`` to fit into the maximum width of 384 pixels (:const:`constants.MAX_IMAGE_WIDTH`),
        *if necessary*.
        The size proportion will be respected.

        :param PIL.Image image: The PIL Image object to resize.
        :rtype: PIL.Image
        :return: The resized image object, if resized, else the original ``image``.

        .. hint::
            Usually you do not need to call this method manually. It is used automatically
            by the :func:`image()` method.
        """
        current_width, current_height = image.size
        if current_width <= MAX_IMAGE_WIDTH:
            return image

        from PIL.Image import Resampling

        new_width = MAX_IMAGE_WIDTH
        new_height = int(new_width * current_height / current_width)
        image.thumbnail((new_width, new_height), Resampling.LANCZOS)
        log.info("Image resized from %dx%d to %dx%d", current_width, current_height, *image.size)
        return image

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

        .. versionchanged:: 1.0.0
            The ``value`` keyword-argument was converted from a :obj:`str` to :const:`constants.Justify`.
        """
        if value is not self._justify:
            self._justify = value
            self.send_command(Command.ESC, 97, value.value)

    def left_blank(self, value: int = 0) -> None:
        """Set the left margin, in points.

        :param int value: Value to pass to the printer (min=0, max=255).
        :exception ThermalPrinterValueError: On incorrect ``value``'s type, or value.
        """
        if value == self._left_blank:
            return

        if not isinstance(value, int) or not (0 <= value <= 255):
            msg = "value should be betwwen 0 and 255."
            raise ThermalPrinterValueError(msg)

        self.send_command(Command.GS, 76, value, 0)

    def left_margin(self, margin: int = 0) -> None:
        """Set the left margin, in 8-points.

        :param int margin: The new margin (min=0, max=47).
        :exception ThermalPrinterValueError: On incorrect ``margin``'s type, or value.
        """
        if not isinstance(margin, int) or not 0 <= margin <= 47:
            msg = "margin should be between 0 and 47 (default: 0)."
            raise ThermalPrinterValueError(msg)

        if margin != self._left_margin:
            self._left_margin = margin
            self.send_command(Command.ESC, 66, margin)

    def line_spacing(self, spacing: int = Defaults.LINE_SPACING.value) -> None:
        """Set the line spacing.

        :param int spacing: The new spacing (min=0, max=255).
        :exception ThermalPrinterValueError: On incorrect ``spacing``'s type, or value.
        """
        if not isinstance(spacing, int) or not 0 <= spacing <= 255:
            msg = f"spacing should be between 0 and 255 (default: {Defaults.LINE_SPACING.value})."
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

    def print_char(self, char: str) -> None:
        """Test one character with all supported code pages.

        :param str char: The character to print.

        Say you are looking for the good code page to print a sequence,
        you can print it using every code pages:

        >>> print_char("现")

        This function is equivalent to:

        >>> for codepage in list(CodePage):
        ...    self.out(f"{codepage.name}: 现")
        """
        for codepage in list(CodePage):
            self.out(f"{codepage.name}: {char}")

    def reset(self) -> None:
        """Reset the printer to factory defaults."""
        self.flush(clear=True)

        print_density = 10  # 100%
        print_break_time = 2  # 500 uS
        self.send_command(Command.DC2, 35, (print_break_time << 5) | print_density)

        # Default values
        self.__max_column = 32
        self.__is_online = True
        self.__is_sleeping = False

        self._barcode_height = Defaults.BARCODE_HEIGHT.value
        self._barcode_left_margin = 0
        self._barcode_position = BarCodePosition.HIDDEN
        self._barcode_width = Defaults.BARCODE_WIDTH.value
        self._bold = False
        self._charset = CharSet.USA
        self._char_spacing = 0
        self._char_height = 24
        self._chinese = False
        self._chinese_format = Chinese.GBK
        self._codepage = CodePage.CP437
        self._double_height = False
        self._double_width = False
        self._font_b = False
        self._inverse = False
        self._justify = Justify.LEFT
        self._left_blank = 0
        self._left_margin = 0
        self._line_spacing = Defaults.LINE_SPACING.value
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

        .. versionchanged:: 1.0.0
            The ``value`` keyword-argument was converted from a :obj:`str` to :const:`constants.Size`.

        .. note::
            This method affects :attr:`max_column`.
        """
        if value is not self._size:
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

    @staticmethod
    def status_to_dict(stat: int) -> dict[str, bool]:
        """Return the printer status as a ``dict``.

        :rtype: dict[str, bool]
        :return: Contains those keys:

            - ``paper``: ``False`` if no paper
            - ``temp``: ``False`` if the temperature exceeds 60°C
            - ``voltage``: ``False`` if the voltage is higher than 9.5V

        .. versionchanged:: 1.0.0
           Removed the ``movement`` key as it would be always ``False``.
        """
        return {
            "paper": stat & 0b00000100 == 0,
            "temp": stat & 0b01000000 == 0,
            "voltage": stat & 0b00001000 == 0,
        }

    def status(self, *, raise_on_error: bool = True) -> dict[str, bool]:
        """Return the printer status.

        :param bool raise_on_error: Raise on error.
        :exception ThermalPrinterCommunicationError:
            If the RX pin is not connected, and if ``raise_on_error`` is ``True``.
        :rtype: dict[str, bool]
        :return: See :func:`status_to_dict()`.

        .. versionadded:: 0.2.0
           The ``raise_on_error`` keyword-argument.
        """
        self.send_command(Command.ESC, 118, 0)
        sleep(self._command_timeout)

        if self.in_waiting:
            stat = ord(self.read(1))
        elif raise_on_error:
            raise ThermalPrinterCommunicationError
        else:
            stat = -1

        return self.status_to_dict(stat)

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

        lines = 26
        self.__lines += lines
        self.__feeds += 1

        sleep(self._dot_print_time * 24 * lines + self._dot_feed_time * (8 * lines + 32))

    def underline(self, weight: Underline = Underline.OFF) -> None:
        """Set the underline mode.

        .. versionchanged:: 1.0.0
            The ``weight`` keyword-argument was converted from an :obj:`int` to :const:`constants.Underline`.
        """
        if weight is not self._underline:
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

import pytest

from thermalprinter.constants import Defaults
from thermalprinter.thermalprinter import ThermalPrinter


def test_repr(printer: ThermalPrinter) -> None:
    assert repr(printer) == (
        "FakeThermalPrinter<baudrate=19200, is_open=True>("
        f"barcode_height={Defaults.BARCODE_HEIGHT.value},"
        " barcode_left_margin=0,"
        " barcode_position=BarCodePosition.HIDDEN,"
        f" barcode_width={Defaults.BARCODE_WIDTH.value},"
        " bold=False,"
        " char_spacing=0,"
        " charset=CharSet.USA,"
        " chinese=False,"
        " chinese_format=Chinese.GBK,"
        " codepage=CodePage.CP437,"
        " double_height=False,"
        " double_width=False,"
        " font_b=False,"
        " inverse=False,"
        " justify=Justify.LEFT,"
        " left_blank=0,"
        " left_margin=0,"
        f" line_spacing={Defaults.LINE_SPACING.value},"
        " rotate=False,"
        " size=Size.SMALL,"
        " strike=False,"
        " underline=Underline.OFF,"
        " upside_down=False"
        ")"
    )


def test_attribute_has_paper(printer: ThermalPrinter) -> None:
    assert not printer.has_paper


def test_attribute_get_is_online(printer: ThermalPrinter) -> None:
    assert printer.is_online


def test_attribute_get_is_sleeping(printer: ThermalPrinter) -> None:
    assert not printer.is_sleeping


def test_attribute_get_lines(printer: ThermalPrinter) -> None:
    assert printer.lines == 0


def test_attribute_get_feeds(printer: ThermalPrinter) -> None:
    assert printer.feeds == 0


def test_attribute_get_max_column(printer: ThermalPrinter) -> None:
    assert printer.max_column == 32


def test_attribute_set_is_online(printer: ThermalPrinter) -> None:
    with pytest.raises(AttributeError):
        printer.is_online = False  # type: ignore[misc]


def test_attribute_set_is_sleeping(printer: ThermalPrinter) -> None:
    with pytest.raises(AttributeError):
        printer.is_sleeping = True  # type: ignore[misc]


def test_attribute_set_lines(printer: ThermalPrinter) -> None:
    with pytest.raises(AttributeError):
        printer.lines = 42  # type: ignore[misc]


def test_attribute_set_feeds(printer: ThermalPrinter) -> None:
    with pytest.raises(AttributeError):
        printer.feeds = 42  # type: ignore[misc]


def test_attribute_set_max_column(printer: ThermalPrinter) -> None:
    with pytest.raises(AttributeError):
        printer.max_column = 42  # type: ignore[misc]

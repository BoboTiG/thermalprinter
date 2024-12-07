"""This is part of the Python's module to manage the DP-EH600 thermal printer.
Source: https://github.com/BoboTiG/thermalprinter.
"""

from __future__ import annotations

from enum import Enum


class BarCode(Enum):
    """Barcode types."""

    # Syntax: (code, (min len(text), max len(text)), allowed_chars)
    UPC_A = (65, (11, 12), 0)
    UPC_E = (66, (11, 12), 0)
    JAN13 = (67, (12, 13), 0)
    EAN13 = (67, (12, 13), 0)  # noqa: PIE796
    JAN8 = (68, (7, 8), 0)
    EAN8 = (68, (7, 8), 0)  # noqa: PIE796
    CODE39 = (69, (1, 255), 1)
    ITF = (70, (1, 255), 0)
    CODABAR = (71, (1, 255), 2)
    CODE93 = (72, (1, 255), 3)
    CODE128 = (73, (2, 255), 3)

    def __repr__(self) -> str:
        return (
            f"<{type(self).__name__}.{self.name}: {self.value[0]}"
            f", range: {self.value[1][0]} <= len(data) <= {self.value[1][1]}>"
        )


class BarCodePosition(Enum):
    """Barcode positions."""

    HIDDEN = 0
    ABOVE = 1
    BELOW = 2
    BOTH = 3


class CharSet(Enum):
    """Character sets."""

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
    """Chinese formats."""

    GBK = 0
    UTF_8 = 1
    BIG5 = 3


class CodePage(Enum):
    """Character code tables."""

    CP437 = (0, "the United States of America, European standard")
    CP932 = (1, "Katakana")
    CP850 = (2, "Multi language")
    CP860 = (3, "Portuguese")
    CP863 = (4, "Canada, French")
    CP865 = (5, "Western Europe")
    CYRILLIC = (6, "The Slavic language")
    CP866 = (7, "The Slavic 2")
    MIK = (8, "The Slavic / Bulgaria")
    CP755 = (9, "Eastern Europe, Latvia 2")
    IRAN = (10, "Iran, Persia")
    CP862 = (15, "Hebrew")
    CP1252 = (16, "Latin 1 [WCP1252]")
    CP1253 = (17, "Greece [WCP1253]")
    CP852 = (18, "Latina 2")
    CP858 = (19, "A variety of language Latin 1 + Europe")
    IRAN2 = (20, "Persian")
    LATVIA = (21, "")
    CP864 = (22, "Arabic")
    ISO_8859_1 = (23, "Western Europe")
    CP737 = (24, "Greece")
    CP1257 = (25, "The Baltic Sea")
    THAI = (26, "Thai Wen")
    CP720 = (27, "Arabic")
    CP855 = (28, "")
    CP857 = (29, "Turkish")
    CP1250 = (30, "Central Europe [WCP1250]")
    CP775 = (31, "")
    CP1254 = (32, "Turkish [WCP1254]")
    CP1255 = (33, "Hebrew [WCP1255]")
    CP1256 = (34, "Arabic [WCP1256]")
    CP1258 = (35, "Vietnamese [WCP1258]")
    ISO_8859_2 = (36, "Latin 2")
    ISO_8859_3 = (37, "Latin 3")
    ISO_8859_4 = (38, "Baltic languages")
    ISO_8859_5 = (39, "The Slavic language")
    ISO_8859_6 = (40, "Arabic")
    ISO_8859_7 = (41, "Greece")
    ISO_8859_8 = (42, "Hebrew")
    ISO_8859_9 = (43, "Turkish")
    ISO_8859_15 = (44, "Latin 9")
    THAI2 = (45, "Thai Wen 2")
    CP856 = (46, "")
    CP874 = (47, "")


class CodePageConverted(Enum):
    """Some code pages are not available on Python, so we use a little translation table."""

    # unsupported encoding -> best replacement
    MIK = "ISO-8859-5"
    CP755 = "UTF-8"
    IRAN = "CP1256"
    IRAN2 = "UTF-8"  # noqa: PIE796
    LATVIA = "ISO-8859-4"
    THAI = "ISO-8859-11"
    THAI2 = "UTF-8"  # noqa: PIE796


class Command(Enum):
    """Codes used to send commands."""

    NONE = 0
    DC2 = 18
    ESC = 27
    FS = 28
    GS = 29


class Justify(Enum):
    """Text justifications."""

    LEFT = 0
    CENTER = 1
    RIGHT = 2


class Size(Enum):
    """Text sizes.

    - ``MEDIUM`` will double the text height.
    - ``LARGE`` will both double the text height, and its width.
    """

    # Syntax: (code, char height, max column)
    SMALL = (0x00, 24, 32)
    MEDIUM = (0x01, 48, 32)
    LARGE = (0x11, 48, 16)


class Underline(Enum):
    """Text underline weights."""

    OFF = 0
    THIN = 1
    THICK = 2


CONSTANTS = [BarCode, BarCodePosition, CharSet, Chinese, CodePage, CodePageConverted, Underline]

DEFAULT_BAUDRATE = 19200
DEFAULT_PORT = "/dev/ttyAMA0"
DEFAULT_HEAT_INTERVAL = 40
DEFAULT_HEAT_TIME = 80
DEFAULT_MOST_HEATED_POINT = 11

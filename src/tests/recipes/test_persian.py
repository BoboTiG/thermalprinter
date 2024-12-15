from __future__ import annotations

from typing import TYPE_CHECKING
from unittest.mock import patch

if TYPE_CHECKING:
    from thermalprinter import ThermalPrinter


def test_persian(printer: ThermalPrinter) -> None:
    result: list[bytes] = []

    def write(data: bytes) -> int | None:
        result.append(data)
        return len(data)

    with patch.object(printer, "write", write):
        printer.out("سلام. این یک جمله فارسی است\nگل پژمرده خار آید", persian=True)

    assert result == [
        # Set the codepage to CodePage.IRAN
        b"\x1bt\n",
        # Set the text justification to Justify.RIGHT
        b"\x1ba\x02",
        # The Persian text
        b"\x96\xa8\x90 \xfc\xa8\xa4\x91\xea \xf9\xf3\xf5\x9b \xed\xfe \xf6\xfe\x90 .\xf4\xf2\xa8\n\xa2\xfe\x8d \xa4\x91\xa1 \xf9\xa2\xa4\xf5\xa6\x95 \xf1\xf0\n",
        # Restore the default codepage
        b"\x1bt\x00",
        # Restore the default text justification
        b"\x1ba\x00",
    ]

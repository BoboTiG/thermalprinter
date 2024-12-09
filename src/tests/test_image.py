import logging
from pathlib import Path

import pytest

from thermalprinter.thermalprinter import ThermalPrinter

Image = pytest.importorskip("PIL.Image")

GNU = Path(__file__).parent.parent / "thermalprinter" / "gnu.png"
BIG = Path(__file__).parent / "ordered-hlines.png"


def test_no_resizing(printer: ThermalPrinter) -> None:
    printer.image(Image.open(GNU))


def test_resized(printer: ThermalPrinter, caplog: pytest.CaptureFixture) -> None:
    printer.image(Image.open(BIG))
    logs = [record.getMessage() for record in caplog.records if record.levelno == logging.INFO]
    assert logs == ["Resized the image from 512x512 to 384x384"]

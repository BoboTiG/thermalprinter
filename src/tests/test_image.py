import logging
from pathlib import Path

import pytest

from thermalprinter.thermalprinter import ThermalPrinter

Image = pytest.importorskip("PIL.Image")

SMALL = Path(__file__).parent / "glider.png"
BIG = Path(__file__).parent / "glider-big.png"


def test_convert(printer: ThermalPrinter, caplog: pytest.CaptureFixture) -> None:
    image = Image.open(SMALL)
    try:
        assert image.mode == "RGB"
        new_image = printer.image_convert(image)
    finally:
        image.close()

    assert new_image.mode == "1"

    logs = [record.getMessage() for record in caplog.records if record.levelno == logging.INFO]
    assert logs == ["Image converted from RGB to 1"]

    # Second conversion, it should be a no-op
    caplog.clear()
    assert printer.image_convert(new_image).mode == "1"
    logs = [record.getMessage() for record in caplog.records if record.levelno == logging.INFO]
    assert not logs

    assert list(new_image.getdata()) == [255, 0, 255, 255, 255, 255, 0, 0, 0]


def test_to_grayscale(printer: ThermalPrinter) -> None:
    image = Image.open(SMALL)
    try:
        image = printer.image_convert(image)
        bitmap = printer.image_to_grayscale(image)
    finally:
        image.close()

    assert bitmap == bytearray(b"@\x00\xe0")


def test_resize_not_necessary(printer: ThermalPrinter, caplog: pytest.CaptureFixture) -> None:
    image = Image.open(SMALL)
    try:
        assert image.size == (3, 3)
        assert printer.image_resize(image).size == image.size
    finally:
        image.close()

    logs = [record.getMessage() for record in caplog.records if record.levelno == logging.INFO]
    assert not logs


def test_resize_is_necessary(printer: ThermalPrinter, caplog: pytest.CaptureFixture) -> None:
    image = Image.open(BIG)
    try:
        assert image.size == (900, 900)
        assert printer.image_resize(image).size == (384, 384)
    finally:
        image.close()

    logs = [record.getMessage() for record in caplog.records if record.levelno == logging.INFO]
    assert logs == ["Image resized from 900x900 to 384x384"]

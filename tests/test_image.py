from os.path import abspath, dirname, realpath
from pathlib import Path

import pytest
from PIL import Image

from thermalprinter.exceptions import ThermalPrinterValueError


def test_empty_values(printer):
    with pytest.raises(TypeError):
        printer.image()


def test_bad_type_str(printer):
    with pytest.raises(ThermalPrinterValueError):
        printer.image("I am not an image ^^")


def test_bad_type_object(printer):
    with pytest.raises(ThermalPrinterValueError):
        printer.image(object)


def test_good(printer):
    cwd = dirname(realpath(abspath(__file__)))
    printer.image(Image.open("{}/../gnu.png".format(cwd)))


def test_pathlib_path(printer):
    image = Path(__file__).parent.parent / "gnu.png"
    printer.image(Image.open(image))

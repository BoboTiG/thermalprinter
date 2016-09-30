#!/usr/bin/env python3
# coding: utf-8

from os.path import abspath, dirname, realpath

import pytest
from PIL import Image
from thermalprinter.exceptions import ThermalPrinterValueError


def test_empty_values(printer):
    with pytest.raises(TypeError):
        printer.image()


def test_bad_type_str(printer):
    with pytest.raises(ThermalPrinterValueError):
        printer.image('I am not an image ^^')


def test_bad_type_object(printer):
    with pytest.raises(ThermalPrinterValueError):
        printer.image(object)


def test_good(printer):
    cwd = dirname(realpath(abspath(__file__)))
    printer.image(Image.open('{}/../gnu.png'.format(cwd)))

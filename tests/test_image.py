#!/usr/bin/env python3
# coding: utf-8

from os.path import abspath, dirname, realpath

import pytest
from PIL import Image


def test_empty_values(printer):
    with pytest.raises(TypeError):
        printer.image()


def test_good(printer):
    cwd = dirname(realpath(abspath(__file__)))
    printer.image(Image.open('{}/../gnu.png'.format(cwd)))

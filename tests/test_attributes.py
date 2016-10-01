#!/usr/bin/env python3
# coding: utf-8

import pytest

from thermalprinter.exceptions import ThermalPrinterAttributeError


def test_attribute_get_is_online(printer):
    assert printer.is_online is True


def test_attribute_get_is_sleeping(printer):
    assert printer.is_sleeping is False


def test_attribute_get_lines(printer):
    assert printer.lines == 0


def test_attribute_get_feeds(printer):
    assert printer.feeds == 0


def test_attribute_get_max_column(printer):
    assert printer.max_column == 32


def test_attribute_set_is_online(printer):
    with pytest.raises(ThermalPrinterAttributeError):
        printer.is_online = False


def test_attribute_set_is_sleeping(printer):
    with pytest.raises(ThermalPrinterAttributeError):
        printer.is_sleeping = True


def test_attribute_set_lines(printer):
    with pytest.raises(ThermalPrinterAttributeError):
        printer.lines = 42


def test_attribute_set_feeds(printer):
    with pytest.raises(ThermalPrinterAttributeError):
        printer.feeds = 42


def test_attribute_set_max_column(printer):
    with pytest.raises(ThermalPrinterAttributeError):
        printer.max_column = 42

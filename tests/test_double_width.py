#!/usr/bin/env python3
# coding: utf-8


def test_default_value(printer):
    assert printer._double_width is False
    assert printer.max_column == 32


def test_changing_no_value(printer):
    printer.double_width()
    assert printer._double_width is False
    assert printer.max_column == 32


def test_changing_state_on(printer):
    printer.double_width(True)
    assert printer._double_width is True
    assert printer.max_column == 16


def test_changing_state_off(printer):
    printer.double_width(False)
    assert printer._double_width is False
    assert printer.max_column == 32


def test_reset_value(printer):
    printer.reset()
    assert printer._double_width is False
    assert printer.max_column == 32

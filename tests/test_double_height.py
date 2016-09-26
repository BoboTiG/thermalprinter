#!/usr/bin/env python3
# coding: utf-8


def test_default_value(printer):
    assert printer._double_height is False


def test_changing_no_value(printer):
    printer.double_height()
    assert printer._double_height is False


def test_changing_state_on(printer):
    printer.double_height(True)
    assert printer._double_height is True


def test_changing_state_off(printer):
    printer.double_height(False)
    assert printer._double_height is False


def test_reset_value(printer):
    printer.reset()
    assert printer._double_height is False

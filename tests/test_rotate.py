#!/usr/bin/env python3
# coding: utf-8


def test_default_value(printer):
    assert printer._rotate is False


def test_changing_no_value(printer):
    printer.rotate()
    assert printer._rotate is False


def test_changing_state_on(printer):
    printer.rotate(True)
    assert printer._rotate is True


def test_changing_state_off(printer):
    printer.rotate(False)
    assert printer._rotate is False


def test_reset_value(printer):
    printer.reset()
    assert printer._rotate is False

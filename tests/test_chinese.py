#!/usr/bin/env python3
# coding: utf-8


def test_default_value(printer):
    assert printer._chinese is False


def test_changing_no_value(printer):
    printer.chinese()
    assert printer._chinese is False


def test_changing_state_on(printer):
    printer.chinese(True)
    assert printer._chinese is True


def test_changing_state_off(printer):
    printer.chinese(False)
    assert printer._chinese is False


def test_reset_value(printer):
    printer.reset()
    assert printer._chinese is False

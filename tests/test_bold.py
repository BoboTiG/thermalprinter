#!/usr/bin/env python3
# coding: utf-8


def test_default_value(printer):
    assert printer._bold is False


def test_changing_no_value(printer):
    printer.bold()
    assert printer._bold is False


def test_changing_state_on(printer):
    printer.bold(True)
    assert printer._bold is True


def test_changing_state_off(printer):
    printer.bold(False)
    assert printer._bold is False


def test_reset_value(printer):
    printer.reset()
    assert printer._bold is False

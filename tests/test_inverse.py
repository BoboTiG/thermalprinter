#!/usr/bin/python3
# coding: utf-8


def test_default_value(printer):
        assert printer._inverse is False


def test_changing_no_value(printer):
        printer.inverse()
        assert printer._inverse is False


def test_changing_state_on(printer):
        printer.inverse(True)
        assert printer._inverse is True


def test_changing_state_off(printer):
        printer.inverse(False)
        assert printer._inverse is False

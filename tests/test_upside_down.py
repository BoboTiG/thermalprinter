#!/usr/bin/python3
# coding: utf-8


def test_default_value(printer):
        assert printer._upside_down is False


def test_changing_no_value(printer):
        printer.upside_down()
        assert printer._upside_down is False


def test_changing_state_on(printer):
        printer.upside_down(True)
        assert printer._upside_down is True


def test_changing_state_off(printer):
        printer.upside_down(False)
        assert printer._upside_down is False

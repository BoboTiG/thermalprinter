#!/usr/bin/env python3
# coding: utf-8

from inspect import getargspec, ArgSpec
from traceback import extract_stack

from thermalprinter.constants import BarCodePosition, CharSet, Chinese, \
    CodePage
from thermalprinter import ThermalPrinter


def test_signature___enter__(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    sig = ArgSpec(args=['self'], varargs=None, keywords=None, defaults=None)
    assert getargspec(ThermalPrinter.__enter__) == sig


def test_signature___init__(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    sig = ArgSpec(args=['self', 'port', 'baudrate'], varargs=None,
                  keywords='kwargs', defaults=('/dev/ttyAMA0', 19200))
    assert getargspec(ThermalPrinter.__init__) == sig


def test_signature___repr__(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    sig = ArgSpec(args=['self'], varargs=None, keywords=None, defaults=None)
    assert getargspec(ThermalPrinter.__repr__) == sig


def test_signature__on_exit(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    sig = ArgSpec(args=['self'], varargs=None, keywords=None, defaults=None)
    assert getargspec(ThermalPrinter._on_exit) == sig


def test_signature_barcode(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    sig = ArgSpec(args=['self', 'data', 'barcode_type'], varargs=None,
                  keywords=None, defaults=None)
    assert getargspec(ThermalPrinter.barcode) == sig


def test_signature_barcode_height(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    sig = ArgSpec(args=['self', 'height'], varargs=None, keywords=None,
                  defaults=(162,))
    assert getargspec(ThermalPrinter.barcode_height) == sig


def test_signature_barcode_left_margin(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    sig = ArgSpec(args=['self', 'margin'], varargs=None, keywords=None,
                  defaults=(0,))
    assert getargspec(ThermalPrinter.barcode_left_margin) == sig


def test_signature_barcode_position(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    sig = ArgSpec(args=['self', 'position'], varargs=None, keywords=None,
                  defaults=(BarCodePosition.HIDDEN,))
    assert getargspec(ThermalPrinter.barcode_position) == sig


def test_signature_barcode_width(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    sig = ArgSpec(args=['self', 'width'], varargs=None, keywords=None,
                  defaults=(3,))
    assert getargspec(ThermalPrinter.barcode_width) == sig


def test_signature_bold(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    sig = ArgSpec(args=['self', 'state'], varargs=None, keywords=None,
                  defaults=(False,))
    assert getargspec(ThermalPrinter.bold) == sig


def test_signature_charset(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    sig = ArgSpec(args=['self', 'charset'], varargs=None, keywords=None,
                  defaults=(CharSet.USA,))
    assert getargspec(ThermalPrinter.charset) == sig


def test_signature_char_spacing(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    sig = ArgSpec(args=['self', 'spacing'], varargs=None, keywords=None,
                  defaults=(0,))
    assert getargspec(ThermalPrinter.char_spacing) == sig


def test_signature_chinese(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    sig = ArgSpec(args=['self', 'state'], varargs=None, keywords=None,
                  defaults=(False,))
    assert getargspec(ThermalPrinter.chinese) == sig


def test_signature_chinese_format(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    sig = ArgSpec(args=['self', 'fmt'], varargs=None, keywords=None,
                  defaults=(Chinese.GBK,))
    assert getargspec(ThermalPrinter.chinese_format) == sig


def test_signature_codepage(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    sig = ArgSpec(args=['self', 'codepage'], varargs=None, keywords=None,
                  defaults=(CodePage.CP437,))
    assert getargspec(ThermalPrinter.codepage) == sig


def test_signature_double_height(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    sig = ArgSpec(args=['self', 'state'], varargs=None, keywords=None,
                  defaults=(False,))
    assert getargspec(ThermalPrinter.double_height) == sig


def test_signature_double_width(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    sig = ArgSpec(args=['self', 'state'], varargs=None, keywords=None,
                  defaults=(False,))
    assert getargspec(ThermalPrinter.double_width) == sig


def test_signature_feed(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    sig = ArgSpec(args=['self', 'number'], varargs=None, keywords=None,
                  defaults=(1,))
    assert getargspec(ThermalPrinter.feed) == sig


def test_signature_flush(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    sig = ArgSpec(args=['self', 'clear'], varargs=None, keywords=None,
                  defaults=(False,))
    assert getargspec(ThermalPrinter.flush) == sig


def test_signature_image(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    sig = ArgSpec(args=['self', 'image'], varargs=None, keywords=None,
                  defaults=None)
    assert getargspec(ThermalPrinter.image) == sig


def test_signature_inverse(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    sig = ArgSpec(args=['self', 'state'], varargs=None, keywords=None,
                  defaults=(False,))
    assert getargspec(ThermalPrinter.inverse) == sig


def test_signature_justify(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    sig = ArgSpec(args=['self', 'value'], varargs=None, keywords=None,
                  defaults=('L',))
    assert getargspec(ThermalPrinter.justify) == sig


def test_signature_left_margin(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    sig = ArgSpec(args=['self', 'margin'], varargs=None, keywords=None,
                  defaults=(0,))
    assert getargspec(ThermalPrinter.left_margin) == sig


def test_signature_line_spacing(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    sig = ArgSpec(args=['self', 'spacing'], varargs=None, keywords=None,
                  defaults=(30,))
    assert getargspec(ThermalPrinter.line_spacing) == sig


def test_signature_offline(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    sig = ArgSpec(args=['self'], varargs=None, keywords=None, defaults=None)
    assert getargspec(ThermalPrinter.offline) == sig


def test_signature_online(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    sig = ArgSpec(args=['self'], varargs=None, keywords=None, defaults=None)
    assert getargspec(ThermalPrinter.online) == sig


def test_signature_out(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    sig = ArgSpec(args=['self', 'line', 'line_feed'], varargs=None,
                  keywords='kwargs', defaults=(True,))
    assert getargspec(ThermalPrinter.out) == sig


def test_signature_rotate(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    sig = ArgSpec(args=['self', 'state'], varargs=None, keywords=None,
                  defaults=(False,))
    assert getargspec(ThermalPrinter.rotate) == sig


def test_signature_send_command(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    sig = ArgSpec(args=['self'], varargs='args', keywords=None, defaults=None)
    assert getargspec(ThermalPrinter.send_command) == sig


def test_signature_size(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    sig = ArgSpec(args=['self', 'value'], varargs=None, keywords=None,
                  defaults=('S',))
    assert getargspec(ThermalPrinter.size) == sig


def test_signature_sleep(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    sig = ArgSpec(args=['self', 'seconds'], varargs=None, keywords=None,
                  defaults=(1,))
    assert getargspec(ThermalPrinter.sleep) == sig


def test_signature_status(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    sig = ArgSpec(args=['self'], varargs=None, keywords=None, defaults=None)
    assert getargspec(ThermalPrinter.status) == sig


def test_signature_strike(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    sig = ArgSpec(args=['self', 'state'], varargs=None, keywords=None,
                  defaults=(False,))
    assert getargspec(ThermalPrinter.strike) == sig


def test_signature_reset(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    sig = ArgSpec(args=['self'], varargs=None, keywords=None, defaults=None)
    assert getargspec(ThermalPrinter.reset) == sig


def test_signature_test(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    sig = ArgSpec(args=['self'], varargs=None, keywords=None, defaults=None)
    assert getargspec(ThermalPrinter.test) == sig


def test_signature_to_bytes(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    sig = ArgSpec(args=['self', 'data'], varargs=None, keywords=None,
                  defaults=None)
    assert getargspec(ThermalPrinter.to_bytes) == sig


def test_signature_underline(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    sig = ArgSpec(args=['self', 'weight'], varargs=None, keywords=None,
                  defaults=(0,))
    assert getargspec(ThermalPrinter.underline) == sig


def test_signature_upside_down(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    sig = ArgSpec(args=['self', 'state'], varargs=None, keywords=None,
                  defaults=(False,))
    assert getargspec(ThermalPrinter.upside_down) == sig


def test_signature_wake(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    sig = ArgSpec(args=['self'], varargs=None, keywords=None, defaults=None)
    assert getargspec(ThermalPrinter.wake) == sig


def test__orphans(methods):
    assert not methods

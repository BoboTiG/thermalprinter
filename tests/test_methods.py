#!/usr/bin/env python3
# coding: utf-8

from inspect import getargspec, ArgSpec
from traceback import extract_stack

from thermalprinter.constants import BarCodePosition, CharSet, Chinese, \
    CodePage
from thermalprinter import ThermalPrinter


def test_signature___enter__(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    val = ArgSpec(args=['self'], varargs=None, keywords=None, defaults=None)
    assert getargspec(ThermalPrinter.__enter__) == val


def test_signature___init__(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    val = ArgSpec(args=['self', 'port', 'baudrate'], varargs=None,
                  keywords='kwargs', defaults=('/dev/ttyAMA0', 19200))
    assert getargspec(ThermalPrinter.__init__) == val


def test_signature___repr__(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    val = ArgSpec(args=['self'], varargs=None, keywords=None, defaults=None)
    assert getargspec(ThermalPrinter.__repr__) == val


def test_signature__conv(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    val = ArgSpec(args=['self', 'data'], varargs=None, keywords=None,
                  defaults=None)
    assert getargspec(ThermalPrinter._conv) == val


def test_signature__on_exit(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    val = ArgSpec(args=['self'], varargs=None, keywords=None, defaults=None)
    assert getargspec(ThermalPrinter._on_exit) == val


def test_signature__set_print_mode(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    val = ArgSpec(args=['self', 'mask'], varargs=None, keywords=None,
                  defaults=None)
    assert getargspec(ThermalPrinter._set_print_mode) == val


def test_signature__unset_print_mode(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    val = ArgSpec(args=['self', 'mask'], varargs=None, keywords=None,
                  defaults=None)
    assert getargspec(ThermalPrinter._unset_print_mode) == val


def test_signature__write_bytes(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    val = ArgSpec(args=['self'], varargs='args', keywords=None, defaults=None)
    assert getargspec(ThermalPrinter._write_bytes) == val


def test_signature__write_print_mode(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    val = ArgSpec(args=['self'], varargs=None, keywords=None, defaults=None)
    assert getargspec(ThermalPrinter._write_print_mode) == val


def test_signature_barcode(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    val = ArgSpec(args=['self', 'data', 'barcode_type'], varargs=None,
                  keywords=None, defaults=None)
    assert getargspec(ThermalPrinter.barcode) == val


def test_signature_barcode_height(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    val = ArgSpec(args=['self', 'height'], varargs=None, keywords=None,
                  defaults=(80,))
    assert getargspec(ThermalPrinter.barcode_height) == val


def test_signature_barcode_left_margin(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    val = ArgSpec(args=['self', 'margin'], varargs=None, keywords=None,
                  defaults=(0,))
    assert getargspec(ThermalPrinter.barcode_left_margin) == val


def test_signature_barcode_position(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    val = ArgSpec(args=['self', 'position'], varargs=None, keywords=None,
                  defaults=(BarCodePosition.HIDDEN,))
    assert getargspec(ThermalPrinter.barcode_position) == val


def test_signature_barcode_width(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    val = ArgSpec(args=['self', 'width'], varargs=None, keywords=None,
                  defaults=(2,))
    assert getargspec(ThermalPrinter.barcode_width) == val


def test_signature_bold(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    val = ArgSpec(args=['self', 'state'], varargs=None, keywords=None,
                  defaults=(False,))
    assert getargspec(ThermalPrinter.bold) == val


def test_signature_charset(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    val = ArgSpec(args=['self', 'charset'], varargs=None, keywords=None,
                  defaults=(CharSet.USA,))
    assert getargspec(ThermalPrinter.charset) == val


def test_signature_char_spacing(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    val = ArgSpec(args=['self', 'spacing'], varargs=None, keywords=None,
                  defaults=(0,))
    assert getargspec(ThermalPrinter.char_spacing) == val


def test_signature_chinese(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    val = ArgSpec(args=['self', 'state'], varargs=None, keywords=None,
                  defaults=(False,))
    assert getargspec(ThermalPrinter.chinese) == val


def test_signature_chinese_format(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    val = ArgSpec(args=['self', 'fmt'], varargs=None, keywords=None,
                  defaults=(Chinese.GBK,))
    assert getargspec(ThermalPrinter.chinese_format) == val


def test_signature_codepage(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    val = ArgSpec(args=['self', 'codepage'], varargs=None, keywords=None,
                  defaults=(CodePage.CP437,))
    assert getargspec(ThermalPrinter.codepage) == val


def test_signature_double_height(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    val = ArgSpec(args=['self', 'state'], varargs=None, keywords=None,
                  defaults=(False,))
    assert getargspec(ThermalPrinter.double_height) == val


def test_signature_double_width(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    val = ArgSpec(args=['self', 'state'], varargs=None, keywords=None,
                  defaults=(False,))
    assert getargspec(ThermalPrinter.double_width) == val


def test_signature_feed(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    val = ArgSpec(args=['self', 'number'], varargs=None, keywords=None,
                  defaults=(1,))
    assert getargspec(ThermalPrinter.feed) == val


def test_signature_flush(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    val = ArgSpec(args=['self', 'clear'], varargs=None, keywords=None,
                  defaults=(False,))
    assert getargspec(ThermalPrinter.flush) == val


def test_signature_image(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    val = ArgSpec(args=['self', 'image'], varargs=None, keywords=None,
                  defaults=None)
    assert getargspec(ThermalPrinter.image) == val


def test_signature_inverse(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    val = ArgSpec(args=['self', 'state'], varargs=None, keywords=None,
                  defaults=(False,))
    assert getargspec(ThermalPrinter.inverse) == val


def test_signature_justify(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    val = ArgSpec(args=['self', 'value'], varargs=None, keywords=None,
                  defaults=('L',))
    assert getargspec(ThermalPrinter.justify) == val


def test_signature_left_margin(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    val = ArgSpec(args=['self', 'margin'], varargs=None, keywords=None,
                  defaults=(0,))
    assert getargspec(ThermalPrinter.left_margin) == val


def test_signature_line_spacing(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    val = ArgSpec(args=['self', 'spacing'], varargs=None, keywords=None,
                  defaults=(30,))
    assert getargspec(ThermalPrinter.line_spacing) == val


def test_signature_offline(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    val = ArgSpec(args=['self'], varargs=None, keywords=None, defaults=None)
    assert getargspec(ThermalPrinter.offline) == val


def test_signature_online(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    val = ArgSpec(args=['self'], varargs=None, keywords=None, defaults=None)
    assert getargspec(ThermalPrinter.online) == val


def test_signature_out(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    val = ArgSpec(args=['self', 'line', 'line_feed'], varargs=None,
                  keywords='kwargs', defaults=(True,))
    assert getargspec(ThermalPrinter.out) == val


def test_signature_rotate(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    val = ArgSpec(args=['self', 'state'], varargs=None, keywords=None,
                  defaults=(False,))
    assert getargspec(ThermalPrinter.rotate) == val


def test_signature_size(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    val = ArgSpec(args=['self', 'value'], varargs=None, keywords=None,
                  defaults=('S',))
    assert getargspec(ThermalPrinter.size) == val


def test_signature_sleep(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    val = ArgSpec(args=['self', 'seconds'], varargs=None, keywords=None,
                  defaults=(1,))
    assert getargspec(ThermalPrinter.sleep) == val


def test_signature_status(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    val = ArgSpec(args=['self'], varargs=None, keywords=None, defaults=None)
    assert getargspec(ThermalPrinter.status) == val


def test_signature_strike(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    val = ArgSpec(args=['self', 'state'], varargs=None, keywords=None,
                  defaults=(False,))
    assert getargspec(ThermalPrinter.strike) == val


def test_signature_reset(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    val = ArgSpec(args=['self'], varargs=None, keywords=None, defaults=None)
    assert getargspec(ThermalPrinter.reset) == val


def test_signature_test(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    val = ArgSpec(args=['self'], varargs=None, keywords=None, defaults=None)
    assert getargspec(ThermalPrinter.test) == val


def test_signature_underline(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    val = ArgSpec(args=['self', 'weight'], varargs=None, keywords=None,
                  defaults=(0,))
    assert getargspec(ThermalPrinter.underline) == val


def test_signature_upside_down(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    val = ArgSpec(args=['self', 'state'], varargs=None, keywords=None,
                  defaults=(False,))
    assert getargspec(ThermalPrinter.upside_down) == val


def test_signature_wake(methods):
    methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))
    val = ArgSpec(args=['self'], varargs=None, keywords=None, defaults=None)
    assert getargspec(ThermalPrinter.wake) == val


def test__orphans(methods):
    assert not methods

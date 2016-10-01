#!/usr/bin/env python3
# coding: utf-8
''' This is part of the Python's module to manage the DP-EH600 thermal printer.
    Source: https://github.com/BoboTiG/thermalprinter
'''

from .constants import BarCode, BarCodePosition, CharSet, Chinese, CodePage
from .exceptions import ThermalPrinterConstantError, \
    ThermalPrinterValueError


def validate_barcode(data, barcode_type):
    ''' Validate data against the bar code type. '''

    # pylint: disable=bad-builtin

    def _range1(min_=48, max_=57):
        return set(range(min_, max_ + 1))

    def _range2():
        range_ = [32, 36, 37, 43]
        range_.extend(_range1(45, 57))
        range_.extend(_range1(65, 90))
        return range_

    def _range3():
        range_ = [36, 43]
        range_.extend(_range1(45, 58))
        range_.extend(_range1(65, 68))
        return range_

    def _range4():
        return _range1(0, 127)

    if not isinstance(barcode_type, BarCode):
        err = 'Valid bar codes are: ' + \
            ', '.join([barcode.name for barcode in BarCode])
        raise ThermalPrinterConstantError(err)

    _, (min_, max_), range_type = barcode_type.value
    data_len = len(data)
    range_ = [_range1, _range2, _range3, _range4][range_type]()

    if not min_ <= data_len <= max_:
        txt = '[{}] Should be {} <= len(data) <= {} (current: {}).'
        err = txt.format(barcode_type.name, min_, max_, data_len)
        raise ThermalPrinterValueError(err)
    elif barcode_type is BarCode.ITF and data_len % 2 != 0:
        raise ThermalPrinterValueError(
            '[BarCode.ITF] len(data) must be even.')

    if not all(ord(char) in range_ for char in data):
        if range_type != 3:
            valid = map(chr, range_)
        else:
            valid = map(hex, range_)
        err = '[{}] Valid characters: {}.'.format(
            barcode_type.name, ', '.join(valid))
        raise ThermalPrinterValueError(err)


def validate_barcode_position(position):
    ''' Validate a bar code position. '''

    if not isinstance(position, BarCodePosition):
        err = ', '.join([pos.name for pos in BarCodePosition])
        raise ThermalPrinterConstantError(
            'Valid positions are: {}.'.format(err))


def validate_charset(charset):
    ''' Validate a charset. '''

    if not isinstance(charset, CharSet):
        err = 'Valid charsets are: {}.'.format(
            ', '.join([cset.name for cset in CharSet]))
        raise ThermalPrinterConstantError(err)


def validate_chinese_format(fmt):
    ''' Validate a Chinese format. '''

    if not isinstance(fmt, Chinese):
        err = ', '.join([cfmt.name for cfmt in Chinese])
        raise ThermalPrinterConstantError(
            'Valid Chinese formats are: {}.'.format(err))


def validate_codepage(codepage):
    ''' Validate a code page. '''

    if not isinstance(codepage, CodePage):
        codes = ''
        last = list(CodePage)[-1]
        for cpage in CodePage:
            sep = '.' if cpage is last else ', '
            _, name = cpage.value
            if name:
                codes += '{} ({}){}'.format(cpage.name, name, sep)
            else:
                codes += '{}{}'.format(cpage.name, sep)
        raise ThermalPrinterConstantError(
            'Valid codepages are: {}'.format(codes))

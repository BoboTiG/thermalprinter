#!/usr/bin/env python3
# coding: utf-8
''' This is part of the Python's module to manage the DP-EH600 thermal printer.
    Source: https://github.com/BoboTiG/thermalprinter
'''


class ThermalPrinterError(Exception):
    ''' Error handling class. '''


class ThermalPrinterAttributeError(ThermalPrinterError):
    ''' Attribute error handling class. '''


class ThermalPrinterConstantError(ThermalPrinterError):
    ''' Constant error handling class. '''


class ThermalPrinterValueError(ThermalPrinterError):
    ''' Value error handling class. '''

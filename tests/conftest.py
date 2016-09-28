#!/usr/bin/env python3
# coding: utf-8

from types import FunctionType

import pytest

from thermalprinter import ThermalPrinter


class FakeThermalPrinter(ThermalPrinter):
    def __init__(self, port):
        super().__init__(port=port)

        # Disable timers
        self._byte_time = 0
        self._dot_feed_time = 0
        self._dot_print_time = 0


def pytest_addoption(parser):
    txt = 'Serial port to use (examples: /dev/ttyAMA0, /dev/ttyS0 [default])'
    parser.addoption('--port', action='store', default='/dev/ttyS0', help=txt)


@pytest.fixture(scope='session')
def port(request):
    return request.config.getoption('--port')


@pytest.fixture(scope='module')
def printer(port):
    return FakeThermalPrinter(port=port)


@pytest.fixture(scope='session')
def methods():
    return sorted([x for x, y in ThermalPrinter.__dict__.items()
                   if type(y) == FunctionType])

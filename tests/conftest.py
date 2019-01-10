# coding: utf-8
import os
import pty

import pytest

from thermalprinter import ThermalPrinter


class FakeThermalPrinter(ThermalPrinter):
    def __init__(self, port):
        super().__init__(port=port)

        # Disable timers
        self._byte_time = 0
        self._dot_feed_time = 0
        self._dot_print_time = 0

    def write(self, *args):
        pass


@pytest.fixture(scope='session')
def port(request):
    """ http://allican.be/blog/2017/01/15/python-dummy-serial-port.html """
    _, slave = pty.openpty()
    return os.ttyname(slave)


@pytest.fixture(scope='module')
def printer(port):
    return FakeThermalPrinter(port=port)

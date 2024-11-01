from __future__ import annotations

import os
import pty
from typing import TYPE_CHECKING, Generator

import pytest

from thermalprinter import ThermalPrinter

if TYPE_CHECKING:
    from _typeshed import ReadableBuffer


class FakeThermalPrinter(ThermalPrinter):
    def __init__(self, port: str) -> None:
        super().__init__(port=port)

        # Disable timers
        self._byte_time = 0
        self._dot_feed_time = 0
        self._dot_print_time = 0

    def write(self, b: ReadableBuffer) -> None:
        pass


@pytest.fixture(autouse=True)
def _no_warnings(recwarn: pytest.WarningsRecorder) -> Generator:
    """Fail on warning."""
    yield

    warnings = [f"{warning.filename}:{warning.lineno} {warning.message}" for warning in recwarn]
    for warning in warnings:
        print(warning)
    assert not warnings


@pytest.fixture(scope="session")
def port() -> str:
    """http://allican.be/blog/2017/01/15/python-dummy-serial-port.html."""
    _, slave = pty.openpty()
    return os.ttyname(slave)


@pytest.fixture(scope="module")
def printer(port: str) -> type[ThermalPrinter]:
    return FakeThermalPrinter(port=port)

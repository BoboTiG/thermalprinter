from __future__ import annotations

import os
import pty
from typing import TYPE_CHECKING, Generator

import pytest

from tests.faker import FakeThermalPrinter

if TYPE_CHECKING:
    from thermalprinter import ThermalPrinter


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

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from tests.faker import FakeThermalPrinter

if TYPE_CHECKING:
    from typing import Generator

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
    """A serial port for unit tests.

    Sources:
        - https://github.com/pyserial/pyserial/blob/v3.5/test/test.py
        - https://github.com/pyserial/pyserial/blob/v3.5/serial/urlhandler/protocol_loop.py
    """
    return "loop://"


@pytest.fixture
def printer(port: str) -> Generator[ThermalPrinter]:
    with FakeThermalPrinter(port) as device:
        yield device

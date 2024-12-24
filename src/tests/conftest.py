from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from tests.faker import FakeThermalPrinter

if TYPE_CHECKING:
    from collections.abc import Generator

    from thermalprinter import ThermalPrinter


@pytest.fixture(autouse=True)
def _no_warnings(recwarn: pytest.WarningsRecorder) -> Generator:
    """Fail on warning."""
    yield

    warnings = [f"{warning.filename}:{warning.lineno} {warning.message}" for warning in recwarn]
    for warning in warnings:  # pragma: nocover
        print(warning)
    assert not warnings


@pytest.fixture
def printer() -> Generator[ThermalPrinter]:
    with FakeThermalPrinter() as device:
        yield device

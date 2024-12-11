from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from thermalprinter.thermalprinter import ThermalPrinter


def test_flush(printer: ThermalPrinter) -> None:
    printer.flush(True)


def test_init(printer: ThermalPrinter) -> None:
    printer.init(42)


def test_print_char(printer: ThermalPrinter) -> None:
    printer.print_char("现")


def test_status(printer: ThermalPrinter) -> None:
    printer.write(b" ")
    assert printer.status() == printer.status_to_dict(ord(" "))


@pytest.mark.parametrize(
    ("stat", "expected"),
    [
        (-1, {"paper": False, "temp": False, "voltage": False}),
        (ord(b" "), {"paper": True, "temp": True, "voltage": True}),
    ],
)
def test_status_to_dict(stat: int, expected: dict[str, bool], printer: ThermalPrinter) -> None:
    assert printer.status_to_dict(stat) == expected


def test_test(printer: ThermalPrinter) -> None:
    printer.test()

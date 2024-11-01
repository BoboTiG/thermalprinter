from importlib.util import find_spec
from typing import Any

import pytest

from thermalprinter import constants as c
from thermalprinter.thermalprinter import ThermalPrinter
from thermalprinter.tools import ls, print_char, printer_tests


def test_print_char(printer: ThermalPrinter) -> None:
    print_char("现", printer=printer)


def check_lines(stdout: str, *constants: Any) -> None:
    output = [line for line in stdout.splitlines() if line not in {"", "---"}]
    assert len(output) == sum(len(list(constant)) for constant in constants)


def test_ls(capsys: pytest.CaptureFixture) -> None:
    ls()
    out = capsys.readouterr()[0]
    check_lines(out, *c.CONSTANTS)


def test_ls_2_constants(capsys: pytest.CaptureFixture) -> None:
    ls(c.BarCodePosition, c.Chinese)
    out = capsys.readouterr()[0]
    check_lines(out, c.BarCodePosition, c.Chinese)


@pytest.mark.parametrize(
    "constant",
    [
        c.BarCode,
        c.BarCodePosition,
        c.CharSet,
        c.Chinese,
        c.CodePage,
        c.CodePageConverted,
    ],
)
def test_ls_barcode(constant: Any, capsys: pytest.CaptureFixture) -> None:
    ls(constant)
    out = capsys.readouterr()[0]
    check_lines(out, constant)


def test_testing(printer: ThermalPrinter) -> None:
    raise_on_error = bool(find_spec("PIL"))
    printer_tests(printer=printer, raise_on_error=raise_on_error)

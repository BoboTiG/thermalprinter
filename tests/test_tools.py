import pytest

from thermalprinter import constants as c
from thermalprinter.tools import ls, print_char, printer_tests

def test_print_char(printer):
    print_char("现", printer=printer)


def check_lines(stdout, *constants):
    output = [l for l in stdout.splitlines() if l not in {"", "---"}]
    assert len(output) == sum(len(list(constant)) for constant in constants)

def test_ls(capsys):
    ls()
    out = capsys.readouterr()[0]
    check_lines(out, *c.CONSTANTS)


def test_ls_2_constants(capsys):
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
def test_ls_barcode(constant, capsys):
    ls(constant)
    out = capsys.readouterr()[0]
    check_lines(out, constant)


def test_testing(printer):
    printer_tests(printer=printer)

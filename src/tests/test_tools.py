from typing import Any

import pytest

from thermalprinter import constants
from thermalprinter.tools import ls


def check_lines(stdout: str, *constants: Any) -> None:
    output = [line for line in stdout.splitlines() if line not in {"", "---"}]
    assert len(output) == sum(len(list(constant)) for constant in constants)


def test_ls(capsys: pytest.CaptureFixture) -> None:
    ls()
    out = capsys.readouterr()[0]
    check_lines(out, *constants.CONSTANTS)


def test_ls_2_constants(capsys: pytest.CaptureFixture) -> None:
    ls(constants.BarCodePosition, constants.Chinese)
    out = capsys.readouterr()[0]
    check_lines(out, constants.BarCodePosition, constants.Chinese)


@pytest.mark.parametrize(
    "constant",
    [
        constants.BarCode,
        constants.BarCodePosition,
        constants.CharSet,
        constants.Chinese,
        constants.CodePage,
        constants.CodePageConverted,
    ],
)
def test_ls_barcode(constant: Any, capsys: pytest.CaptureFixture) -> None:
    ls(constant)
    out = capsys.readouterr()[0]
    check_lines(out, constant)

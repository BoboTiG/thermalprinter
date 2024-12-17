from pathlib import Path
from typing import Any
from unittest.mock import patch

import pytest

from thermalprinter import constants, tools
from thermalprinter.thermalprinter import ThermalPrinter


def check_lines(stdout: str, *constants: Any) -> None:
    output = [line for line in stdout.splitlines() if line not in {"", "---"}]
    assert len(output) == sum(len(list(constant)) for constant in constants)


def test_ls(capsys: pytest.CaptureFixture) -> None:
    tools.ls()
    out = capsys.readouterr()[0]
    check_lines(out, *constants.CONSTANTS)


def test_ls_2_constants(capsys: pytest.CaptureFixture) -> None:
    tools.ls(constants.BarCodePosition, constants.Chinese)
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
    tools.ls(constant)
    out = capsys.readouterr()[0]
    check_lines(out, constant)


def test_stats_load(tmp_path: Path) -> None:
    with patch("thermalprinter.constants.STATS_FILE", f"{tmp_path}/stats.json"):
        assert tools.stats_file() == tmp_path / "stats.json"
        assert tools.stats_load() == {"feeds": 0, "lines": 0}


def test_stats_save(printer: ThermalPrinter, tmp_path: Path) -> None:
    with patch("thermalprinter.constants.STATS_FILE", f"{tmp_path}/stats.json"):
        assert tools.stats_file() == tmp_path / "stats.json"
        assert tools.stats_load() == {"feeds": 0, "lines": 0}

        printer.out("one line")
        printer.feed(4)
        printer.test()
        printer.demo()

        tools.stats_save(printer)

        stats = tools.stats_load()
        assert stats["feeds"] == 9
        assert stats["lines"] in {54, 56}  # 56 when Persian dependencies are met

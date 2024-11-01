from pathlib import Path

import pytest

from thermalprinter.thermalprinter import ThermalPrinter

Image = pytest.importorskip("PIL.Image")
GNU = Path(__file__).parent / "gnu.png"


def test_empty_values(printer: ThermalPrinter) -> None:
    with pytest.raises(TypeError):
        printer.image()  # type: ignore[call-arg]


def test_path_str(printer: ThermalPrinter) -> None:
    printer.image(Image.open(str(GNU)))


def test_path_pathlib(printer: ThermalPrinter) -> None:
    printer.image(Image.open(GNU))

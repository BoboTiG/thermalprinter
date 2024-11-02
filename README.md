# DP-EH600 Thermal Printer

[![PyPI Version](https://img.shields.io/pypi/v/thermalprinter.svg)](https://pypi.python.org/pypi/thermalprinter)
[![PyPI Status](https://img.shields.io/pypi/status/thermalprinter.svg)](https://pypi.python.org/pypi/thermalprinter)
[![PyPI Python Versions](https://img.shields.io/pypi/pyversions/thermalprinter.svg)](https://pypi.python.org/pypi/thermalprinter)
[![Tests](https://github.com/BoboTiG/thermalprinter/actions/workflows/tests.yml/badge.svg?branch=master)](https://github.com/BoboTiG/thermalprinter/actions/workflows/tests.yml)
[![Github License](https://img.shields.io/github/license/BoboTiG/thermalprinter.svg)](https://github.com/BoboTiG/thermalprinter/blob/master/LICENSE)

Python module to manage DP-EH600 thermal printers (the one sold by AdaFruit).

- **Python 3.7+** and PEP8 compliant;
- this is a clean follow of the technical manual with few helpers;
- and there is a [complete, and beautiful, documentation](https://thermalprinter.readthedocs.io) 🙂
- also several useful [recipes](https://github.com/BoboTiG/thermalprinter-recipes);
- **contributors** are welcome, check the [developer guide](https://thermalprinter.readthedocs.io/en/latest/developers.html)!

## Printers

Supported printers:

- DP-EH600
- DP-EH400/1

## Installation

```bash
python -m pip install -U thermalprinter
```

## Usage

An example is better than a thousand words:

```python
from PIL import Image  # Optional, for printing images
from ThermalPrinter import *


with ThermalPrinter(port="/dev/ttyAMA0") as printer:
    # Picture
    printer.image(Image.open("src/tests/gnu.png"))

    # Bar codes
    printer.barcode_height(80)
    printer.barcode_position(BarCodePosition.BELOW)
    printer.barcode_width(3)
    printer.barcode("012345678901", BarCode.EAN13)

    # Styles
    printer.out("Bold", bold=True)
    printer.out("Double height", double_height=True)
    printer.out("Double width", double_width=True)
    printer.out("Inverse", inverse=True)
    printer.out("Rotate 90°", rotate=True, codepage=CodePage.ISO_8859_1)
    printer.out("Strike", strike=True)
    printer.out("Underline", underline=1)
    printer.out("Upside down", upside_down=True)

    # Chinese (almost all alphabets exist)
    printer.out("现代汉语通用字表", chinese=True, chinese_format=Chinese.UTF_8)
                
    # Greek (excepted the ΐ character)
    printer.out("Στην υγειά μας!", codepage=CodePage.CP737)

    # Other characters
    printer.out(b"Cards \xe8 \xe9 \xea \xeb", codepage=CodePage.CP932)

    # Accents
    printer.out("Voilà !", justify="C", strike=True, underline=2, codepage=CodePage.ISO_8859_1)

    # Line feeds
    printer.feed(2)
```

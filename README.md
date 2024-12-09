# DP-EH600 Thermal Printer

[![PyPI Version](https://img.shields.io/pypi/v/thermalprinter.svg)](https://pypi.python.org/pypi/thermalprinter)
[![PyPI Status](https://img.shields.io/pypi/status/thermalprinter.svg)](https://pypi.python.org/pypi/thermalprinter)
[![PyPI Python Versions](https://img.shields.io/pypi/pyversions/thermalprinter.svg)](https://pypi.python.org/pypi/thermalprinter)
[![Tests](https://github.com/BoboTiG/thermalprinter/actions/workflows/tests.yml/badge.svg?branch=master)](https://github.com/BoboTiG/thermalprinter/actions/workflows/tests.yml)
[![Github License](https://img.shields.io/github/license/BoboTiG/thermalprinter.svg)](https://github.com/BoboTiG/thermalprinter/blob/master/LICENSE)

Python module to manage DP-EH600 thermal printers (the one sold by AdaFruit).

- **Python 3.7** minimum;
- This is a clean follow of the technical manual with few helpers;
- And there is a [complete, and beautiful, documentation](https://thermalprinter.readthedocs.io) 🙂
- Also several useful [recipes](https://github.com/BoboTiG/thermalprinter-recipes);
- **Contributors** are welcome, check the [developer guide](https://thermalprinter.readthedocs.io/developers.html)!

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
from PIL import Image  # Optional, for images printing
from thermalprinter import *


with ThermalPrinter() as printer:
    # Picture
    printer.image(Image.open("src/tests/gnu.png"))

    # Barcode
    printer.barcode_height(80)
    printer.barcode_position(BarCodePosition.BELOW)
    printer.barcode_width(3)
    printer.barcode("012345678901", BarCode.EAN13)

    # Style
    printer.out("Bold", bold=True)
    printer.out("Double height", double_height=True)
    printer.out("Double width", double_width=True)
    printer.out("Font B mode", font_b=True)
    printer.out("Inverse", inverse=True)
    printer.out("Rotate 90°", rotate=True, codepage=CodePage.ISO_8859_1)
    printer.out("Size LARGE", size=Size.LARGE)
    printer.out("Strike", strike=True)
    printer.out("Underline", underline=Underline.THIN)
    printer.out("Upside down", upside_down=True)

    # Chinese (almost all alphabets exist)
    printer.out("现代汉语通用字表", chinese=True, chinese_format=Chinese.UTF_8)
                
    # Greek (excepted the ΐ character)
    printer.out("Στην υγειά μας!", codepage=CodePage.CP737)

    # Other characters
    printer.out(b"Cards \xe8 \xe9 \xea \xeb", codepage=CodePage.CP932)

    # Accent
    printer.out(
        "Voilà !",
        codepage=CodePage.ISO_8859_1,
        justify=Justify.CENTER,
        strike=True,
        underline=Underline.THICK,
    )

    # Line feeds
    printer.feed(2)
```

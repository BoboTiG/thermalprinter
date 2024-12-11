"""This is part of the Python's module to manage the DP-EH600 thermal printer.
Source: https://github.com/BoboTiG/thermalprinter.
"""

from __future__ import annotations

import json
from logging import getLogger
from pathlib import Path
from typing import TYPE_CHECKING

from thermalprinter import constants

if TYPE_CHECKING:
    from enum import Enum

    from thermalprinter import ThermalPrinter

log = getLogger(__name__)


def ls(*consts: type[Enum]) -> None:
    """Print constants values.

    :param list constants: Constant(s) to print.

    Print all constants:

    >>> ls()

    Print Chinese constant values:

    >>> ls(Chinese)

    Print Chinese, and CodePage, constant values:

    >>> ls(Chinese, CodePage)
    """
    for constant in consts or constants.CONSTANTS:
        print("---")
        for value in constant:
            print(value)
        print()


def stats_file() -> Path:
    """Return the full path to the statistics file."""
    return Path(constants.STATS_FILE).expanduser()


def stats_load() -> dict[str, int]:
    """Load statistics from the :const:`thermalprinter.constants.STATS_FILE` file.

    :rtype: dict[str, int]
    :return: Contains those keys:

        - ``feeds``: total count of printed feeds
        - ``lines``: total count of printed lines
    """
    try:
        return json.loads(stats_file().read_text())
    except FileNotFoundError:
        return {"feeds": 0, "lines": 0}


def stats_save(printer: ThermalPrinter) -> None:
    """Save printer statistics to the :const:`thermalprinter.constants.STATS_FILE` file.

    :param ThermalPrinter printer: The Printer.
    """
    stats = stats_load()
    stats["feeds"] += printer.feeds
    stats["lines"] += printer.lines

    file = stats_file()
    file.write_text(json.dumps(stats))
    log.debug("Saved statistics %r into %r.", stats, str(file))

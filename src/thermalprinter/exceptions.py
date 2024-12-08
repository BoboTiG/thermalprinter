"""This is part of the Python's module to manage the DP-EH600 thermal printer.
Source: https://github.com/BoboTiG/thermalprinter.
"""

from __future__ import annotations


class ThermalPrinterError(Exception):
    """Base class for thermal printer exceptions."""


class ThermalPrinterCommunicationError(ThermalPrinterError):
    """Raised on communication error with the printer."""


class ThermalPrinterValueError(ThermalPrinterError):
    """Raised on incorrect type, or value, passed to any method."""

"""This is part of the Python's module to manage the DP-EH600 thermal printer.
Source: https://github.com/BoboTiG/thermalprinter.
"""

from __future__ import annotations


class ThermalPrinterError(Exception):
    """Base class for thermal printer exceptions.."""


class ThermalPrinterCommunicationError(ThermalPrinterError):
    """Exception that is raised on communication error with the printer."""


class ThermalPrinterConstantError(ThermalPrinterError):
    """Exception that is raised on inexistant or out of range constant."""


class ThermalPrinterValueError(ThermalPrinterError):
    """Exception that is raised on incorrect type or value passed to any method."""

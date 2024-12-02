from __future__ import annotations

from typing import TYPE_CHECKING, Any

from thermalprinter import ThermalPrinter

if TYPE_CHECKING:
    from _typeshed import ReadableBuffer


class FakeThermalPrinter(ThermalPrinter):
    def __init__(self, port: str, **kwargs: Any) -> None:
        super().__init__(port=port, command_timeout=0.0, sleep_sec_after_init=0.0, **kwargs)

        # Disable timers
        self._byte_time = 0
        self._dot_feed_time = 0
        self._dot_print_time = 0

    def write(self, b: ReadableBuffer) -> None:
        pass

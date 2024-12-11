from __future__ import annotations

import queue
from typing import TYPE_CHECKING

from thermalprinter import ThermalPrinter

if TYPE_CHECKING:
    from typing import Any


class FakeThermalPrinter(ThermalPrinter):
    def __init__(self, port: str, **kwargs: Any) -> None:
        super().__init__(
            port=port,
            byte_time=0.0,
            command_timeout=0.0,
            dot_feed_time=0.0,
            dot_print_time=0.0,
            use_stats=False,
            **kwargs,
        )

        # Larger queue to handle all cases
        self._conn.queue = queue.Queue(4096 * 10)

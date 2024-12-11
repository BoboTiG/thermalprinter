from pathlib import Path
from unittest.mock import patch

from thermalprinter import tools
from thermalprinter.thermalprinter import ThermalPrinter


def test_stats_saved_on_exit(printer: ThermalPrinter, tmp_path: Path) -> None:
    with patch("thermalprinter.constants.STATS_FILE", f"{tmp_path}/stats.json"):
        assert tools.stats_file() == tmp_path / "stats.json"
        assert tools.stats_load() == {"feeds": 0, "lines": 0}

        with printer:
            printer.out("one line")
            printer.feed(4)
            printer.test()
            printer.demo()
            printer._use_stats = True

        assert tools.stats_load() == {"feeds": 9, "lines": 54}

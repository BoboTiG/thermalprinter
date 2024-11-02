# Changelog

## 0.3.0

Release date: `2024-11-02`

### Features

- Added support for Python 3.8, 3.9, 3.10, 3.11, 3.12, 3.13, and 3.14.
- Support for DP-EH400/1 printers is confirmed (#17).
- Added type annotations.
- New option to specify commands timeout via `ThermalPrinter(..., command_timeout=float)` (#17).
- Documentation is now generated from the source code to never miss signature changes.
- Moved the CI from Travis-CI to GitHub actions.
- Run ruff on the entire source code.
- Added more quality checks.

### Technical Changes

- Drop support for Python 3.5, and 3.6.
- Renamed `tools.test_char()` → `tools.print_char()`.
- Renamed `tools.testing()` → `tools.printer_tests()`.
- No longer checks that the provided `image` argument to `ThermalPrinter.image()` is a `PIL.Image` object.

### Contributors

Thanks to our beloved contributors: @uniphil, @d21d3q

## 0.2.0

Release date: `2019-01-10`

### Bug Fixes

- Fixed image printing in `tools.printer_tests()` when the module is installed. Will now raise an exception if `raise_on_error` argument is `True` (default).

### Features

- Add communication error in the `status()` (issue #3). Will now raise an exception if `raise_on_error` argument is `True` (default).
- Use `setup.cfg` instead of `setup.py`

### Technical Changes

- Removed `ThermalPrinterAttributeError` exception
- Attributes `is_online`, `is_sleeping`, `lines`, `feeds` and `max_column` now raise `AttributeError` when trying to set them (previously raising `ThermalPrinterAttributeError`)
- Changed signature of `tools.printer_tests(port='/dev/ttyAMA0', heat_time=80)` → `tools.printer_tests(printer=None, raise_on_error=True)`
- Changed signature of `tools.print_char(char)` → `tools.print_char(char, printer=None)`

### Contributors

Thanks to our beloved contributors: @d21d3q

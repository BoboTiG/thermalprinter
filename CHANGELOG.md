# 1.0.0

Release date: `2024-12-xx`

## Features

- New option to control printer settings at initialization: `ThermalPrinter(..., run_setup_cmd=bool)` (#15).
- New option to specify the *mandatory* sleep time, in seconds, right after the serial initialization: `ThermalPrinter(..., sleep_sec_after_init=float)`.
- Improved the documentation by fixing issues found with [Harper](https://github.com/elijah-potter/harper).
- 100% tests coverage!

## Technical Changes

- Added the `Justify` constant to use in the `ThermalPrinter.justify()` method (**breaking change**).
- Added the `Size` constant to use in the `ThermalPrinter.size()` method (**breaking change**).
- Added the `Underline` constant to use in the `ThermalPrinter.underline()` method (**breaking change**).
- Added the `Defaults` constant.
- Added the `ThermalPrinter.__exit__()` method to properly close the printer when leaving the context manager.
- Added the `ThermalPrinter.has_paper` property.
- Moved the `tools.printer_tests()` function to the `ThermalPrinter.demo()` method (**breaking change**).
- Moved the `tools.print_char()` function to the `ThermalPrinter.print_char()` method (**breaking change**).
- Moved the `validate.validate_barcode()` function to the `ThermalPrinter.validate_barcode()` method.
- Removed the `line_feed` keyword-argument from `ThermalPrinter.out()`.
- Removed the `validate.py` file, and most of `validate_*()` functions.
- Removed the `exceptions.ThermalPrinterConstantError` class.

# 0.3.0

Release date: `2024-11-02`

## Features

- Added support for Python 3.8, 3.9, 3.10, 3.11, 3.12, 3.13, and 3.14.
- Support for DP-EH400/1 printers is confirmed (#17).
- Added type annotations.
- New option to specify commands timeout via `ThermalPrinter(..., command_timeout=float)` (#17).
- Documentation is now generated from the source code to never miss signature changes.
- Moved the CI from Travis-CI to GitHub actions.
- Run ruff on the entire source code.
- Added more quality checks.

## Technical Changes

- Drop support for Python 3.5, and 3.6.
- Renamed `tools.test_char()` → `tools.print_char()`.
- Renamed `tools.testing()` → `tools.printer_tests()`.
- No longer checks that the provided `image` argument to `ThermalPrinter.image()` is a `PIL.Image` object.

## Contributors

Thanks to our beloved contributors: @uniphil, @d21d3q

# 0.2.0

Release date: `2019-01-10`

## Bug Fixes

- Fixed image printing in `tools.printer_tests()` when the module is installed. Will now raise an exception if `raise_on_error` argument is `True` (default).

## Features

- Add communication error in the `status()` (issue #3). Will now raise an exception if `raise_on_error` argument is `True` (default).
- Use `setup.cfg` instead of `setup.py`

## Technical Changes

- Removed `ThermalPrinterAttributeError` exception
- Attributes `is_online`, `is_sleeping`, `lines`, `feeds` and `max_column` now raise `AttributeError` when trying to set them (previously raising `ThermalPrinterAttributeError`)
- Changed signature of `tools.printer_tests(port='/dev/ttyAMA0', heat_time=80)` → `tools.printer_tests(printer=None, raise_on_error=True)`
- Changed signature of `tools.print_char(char)` → `tools.print_char(char, printer=None)`

## Contributors

Thanks to our beloved contributors: @d21d3q

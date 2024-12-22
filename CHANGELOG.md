# 1.0.1-dev

Release date: `202x-xx-xx`

## Bug Fixes

- Weather recipe: fixed special characters handling (#49).
- Weather recipe: added the missing `byteorder` (keyword-)argument to `int.from_bytes()` calls for Python 3.9, and 3.10.

## Features

- Weather recipe: now using a custom User-Agent HTTP header to fetch OpenWeatherMap data, added the `USER_AGENT` constant.

## Technical Changes

- Weather recipe: removed the useless `UNKNOWN` constant.

# 1.0.0

Release date: `2024-12-17`

## Bug Fixes

- Reworked images printing to, hopefully, fix all issues.
- Fixed printed lines counting in `ThermalPrinter.out()`.

## Features

- Support for QR701 printers is confirmed (#15).
- New extra: `calendar`, to print daily stuff from your calendar, and birthdays as a bonus! It provides the `print-calendar` executable.
- New extra: `persian`, to make your life easier when printing Persian text: `ThermalPrinter.out("...", persian=True")`.
- New extra: `weather`, to print the weather alongside with the saint of the day! It provides the `print-weather` executable.
- New text styles: `font_b`, and `left_blank`.
- New options to tweak printer behaviors: `byte_time`, `dot_feed_time`, `dot_print_time`, `read_timeout`, and `write_timeout`.
- New option to control printer settings at initialization: `ThermalPrinter(..., run_setup_cmd=bool)` (#15).
- It is now possible to pass barcode styling instructions in `ThermalPrinter.barcode(DATA, BARCODE_TYPE, **kwargs)`, in the same way it's done for `ThermalPrinter.out()`.
- Introduced statistics persisted at exit. This behavior can be disabled by passing `use_stats=False` to the class.
- Enhanced the demonstration code.
- Rewrote the entire documentation to cover all possible stuff, and it is way prettier now, (thanks to the awesome [Shibuya theme(https://shibuya.lepture.com)]).
- Improved the documentation by fixing issues found with [Harper](https://github.com/elijah-potter/harper).
- 100% tests coverage!
- Added lot of logs.

## Technical Changes

- Added the `Justify` constant to use in the `ThermalPrinter.justify()` method (**breaking change**).
- Added the `Size` constant to use in the `ThermalPrinter.size()` method (**breaking change**).
- Added the `Underline` constant to use in the `ThermalPrinter.underline()` method (**breaking change**).
- Added the `Defaults` constant. And they can be tweaked via `TP_*` environment variables.
- Added the `ThermalPrinter.__exit__()` method to properly close the printer when leaving the context manager.
- Added the `ThermalPrinter.has_paper` property.
- Added the `ThermalPrinter.close()` method.
- Added the `ThermalPrinter.demo()` method.
- Added the `ThermalPrinter.font_b()` method.
- Added the `ThermalPrinter.image_chunks()` method.
- Added the `ThermalPrinter.image_convert()` method.
- Added the `ThermalPrinter.image_resize()` method.
- Added the `ThermalPrinter.init()` method.
- Added the `ThermalPrinter.left_blank()` method.
- Added the `ThermalPrinter.status_to_dict()` method.
- Added the `tools.stats_file()` function.
- Added the `tools.stats_load()` function.
- Added the `tools.stats_save()` function.
- Moved the `tools.printer_tests()` function to the `ThermalPrinter.demo()` method (**breaking change**).
- Moved the `tools.print_char()` function to the `ThermalPrinter.print_char()` method (**breaking change**).
- Moved the `validate.validate_barcode()` function to the `ThermalPrinter.validate_barcode()` method.
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

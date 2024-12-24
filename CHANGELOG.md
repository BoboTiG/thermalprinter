# 2.0.0-dev

Release date: `202x-xx-xx`

## Bug Fixes

- Weather recipe: fixed special characters handling ({pull}`49`).
- Weather recipe: added the missing `byteorder` (keyword-)argument to `int.from_bytes()` calls for Python 3.9, and 3.10.

## Features

- Calendar recipe: improve multi-days event display ({issue}`43`).
- Calendar recipe: improve printing performances.
- Calendar recipe: feed before printing birthdays.
- Weather recipe: now using a custom User-Agent HTTP header to fetch OpenWeatherMap data, added the {const}`thermalprinter.recipes.weather.USER_AGENT` constant.

## Technical Changes

- Drop support for Python 3.7, and 3.8.
- Calendar recipe: added the {const}`thermalprinter.recipes.calendar.DAYS_NAMES` constant.
- Calendar recipe: added the {func}`thermalprinter.recipes.calendar.format_event_date()` function.
- Calendar recipe: moved the {meth}`thermalprinter.recipes.calendar.Calendar.forge_header_image()` method to its own {func}`thermalprinter.recipes.calendar.forge_header_image()` function.
- Weather recipe: removed the useless {const}`thermalprinter.recipes.weather.UNKNOWN` constant.

# 1.0.0

Release date: `2024-12-17`

## Bug Fixes

- Reworked images printing to, hopefully, fix all issues.
- Fixed printed lines counting in {meth}`thermalprinter.ThermalPrinter.out()`.

## Features

- Support for QR701 printers is confirmed ({issue}`15`).
- New extra: `calendar`, to print daily stuff from your calendar, and birthdays as a bonus! See {ref}`recipes <calendar>`.
- New extra: `persian`, to make your life easier when printing Persian text, see {ref}`recipes <persian-text>`.
- New extra: `weather`, to print the weather alongside with the saint of the day! See {ref}`recipes <weather>`.
- New text styles: {meth}`thermalprinter.ThermalPrinter.font_b()`, and {meth}`thermalprinter.ThermalPrinter.left_blank()`.
- New options to tweak printer behaviors: `byte_time`, `dot_feed_time`, `dot_print_time`, `read_timeout`, and `write_timeout`.
- New option to control printer settings at initialization to {class}`thermalprinter.ThermalPrinter`: `run_setup_cmd=bool` ({issue}`15`).
- It is now possible to pass barcode styling instructions in {meth}`thermalprinter.ThermalPrinter.barcode()`, in the same way it's done for {meth}`thermalprinter.ThermalPrinter.out()`.
- Introduced statistics persisted at exit. This behavior can be disabled by passing `use_stats=False` to {class}`thermalprinter.ThermalPrinter`.
- Enhanced the demonstration code.
- Rewrote the entire documentation to cover all possible stuff, and it is way prettier now, (thanks to the awesome [Shibuya theme](https://shibuya.lepture.com)).
- Improved the documentation by fixing issues found with [Harper](https://github.com/elijah-potter/harper).
- 100% tests coverage!
- Added lot of logs.

## Technical Changes

- Added the {const}`thermalprinter.constants.Justify` constant to use in the {meth}`thermalprinter.ThermalPrinter.justify()` method (**breaking change**).
- Added the {const}`thermalprinter.constants.Size` constant to use in the {meth}`thermalprinter.ThermalPrinter.size()` method (**breaking change**).
- Added the {const}`thermalprinter.constants.Underline` constant to use in the {meth}`thermalprinter.ThermalPrinter.underline()` method (**breaking change**).
- Added the {const}`thermalprinter.constants.Defaults` constant. And they can be tweaked via `TP_*` environment variables.
- Added the {meth}`thermalprinter.ThermalPrinter.__exit__()` method to properly close the printer when leaving the context manager.
- Added the {meth}`thermalprinter.ThermalPrinter.has_paper` property.
- Added the {meth}`thermalprinter.ThermalPrinter.close()` method.
- Added the {meth}`thermalprinter.ThermalPrinter.demo()` method.
- Added the {meth}`thermalprinter.ThermalPrinter.font_b()` method.
- Added the {meth}`thermalprinter.ThermalPrinter.image_chunks()` method.
- Added the {meth}`thermalprinter.ThermalPrinter.image_convert()` method.
- Added the {meth}`thermalprinter.ThermalPrinter.image_resize()` method.
- Added the {meth}`thermalprinter.ThermalPrinter.init()` method.
- Added the {meth}`thermalprinter.ThermalPrinter.left_blank()` method.
- Added the {meth}`thermalprinter.ThermalPrinter.status_to_dict()` method.
- Added the {func}`thermalprinter.tools.stats_file()` function.
- Added the {func}`thermalprinter.tools.stats_load()` function.
- Added the {func}`thermalprinter.tools.stats_save()` function.
- Moved the {func}`thermalprinter.tools.printer_tests()` function to the {meth}`thermalprinter.ThermalPrinter.demo()` method (**breaking change**).
- Moved the {func}`thermalprinter.tools.print_char()` function to the {meth}`thermalprinter.ThermalPrinter.print_char()` method (**breaking change**).
- Moved the {func}`thermalprinter.validate.validate_barcode()` function to the {meth}`thermalprinter.ThermalPrinter.validate_barcode()` method.
- Removed the {file}`validate.py` file, and most of `validate_*()` functions.
- Removed the {obj}`thermlaprinter.exceptions.ThermalPrinterConstantError` class.

# 0.3.0

Release date: `2024-11-02`

## Features

- Added support for Python 3.8, 3.9, 3.10, 3.11, 3.12, 3.13, and 3.14.
- Support for DP-EH400/1 printers is confirmed ({pull}`17`).
- Added type annotations.
- New option to specify commands timeout via `command_timeout=float)` in {class}`thermalprinter.ThermalPrinter` ({pull}`17`).
- Documentation is now generated from the source code to never miss signature changes.
- Moved the CI from Travis-CI to GitHub actions.
- Run ruff on the entire source code.
- Added more quality checks.

## Technical Changes

- Drop support for Python 3.5, and 3.6.
- Renamed {func}`thermalprinter.tools.test_char()` → {func}`thermalprinter.tools.print_char()`.
- Renamed {func}`thermalprinter.tools.testing()` → {func}`thermalprinter.tools.printer_tests()`.
- No longer checks that the provided `image` argument to {meth}`thermalprinter.ThermalPrinter.image()` is a {py:obj}`PIL.Image` object.

## Contributors

Thanks to our beloved contributors: {contributor}`uniphil`, {contributor}`d21d3q`

# 0.2.0

Release date: `2019-01-10`

## Bug Fixes

- Fixed image printing in {func}`thermalprinter.tools.printer_tests()` when the module is installed. Will now raise an exception if `raise_on_error` argument is `True` (default).

## Features

- Add communication error in the {meth}`thermalprinter.ThermalPrinter.status()` ({issue}`3`). Will now raise an exception if `raise_on_error` argument is `True` (default).
- Use {file}`setup.cfg` instead of {file}`setup.py`.

## Technical Changes

- Removed {obj}`thermalprinter.exceptions.ThermalPrinterAttributeError` exception.
- Attributes {attr}`thermalprinter.ThermalPrinter.is_online`, {attr}`thermalprinter.ThermalPrinter.is_sleeping`, {attr}`thermalprinter.ThermalPrinter.lines`, {attr}`thermalprinter.ThermalPrinter.feeds` and {attr}`thermalprinter.ThermalPrinter.max_column` now raise {py:obj}`AttributeError` when trying to set them (previously raising `ThermalPrinterAttributeError`).
- Changed the signature of {func}`thermalprinter.tools.printer_tests(port='/dev/ttyAMA0', heat_time=80)` → {func}`thermalprinter.tools.printer_tests(printer=None, raise_on_error=True)`.
- Changed the signature of {func}`thermalprinter.tools.print_char(char)` → {func}`thermalprinter.tools.print_char(char, printer=None)`.

## Contributors

Thanks to our beloved contributors: {contributor}`d21d3q`

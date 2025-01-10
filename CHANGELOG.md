# 2.0.1-dev

Release date: `2025-xx-xx`

## Bug Fixes

- Tests: missing code adaptation in `test_calendar.py::test_get_events_on_multi_days()`.

## Features

- 

## Technical Changes

- 

# 2.0.0

Release date: `2025-01-10`

## Bug Fixes

- Weather recipe: fixed special characters handling ({pull}`49`).
- Weather recipe: added the missing `byteorder` (keyword-)argument to `int.from_bytes()` calls for Python 3.9, and 3.10.

## Features

- Calendar recipe: improve multi-days event display ({issue}`43`).
- Calendar recipe: improve printing performances.
- Calendar recipe: feed before printing birthdays.
- Weather recipe: now using a custom User-Agent HTTP header to fetch OpenWeatherMap data.

## Technical Changes

- Drop support for Python 3.7, and 3.8.
- Calendar recipe: added the {func}`recipes.calendar.format_event_date()` function.
- Calendar recipe: moved the {meth}`recipes.calendar.Calendar.forge_header_image()` method to its own {func}`recipes.calendar.forge_header_image()` function.
- Weather recipe: added the {const}`recipes.weather.USER_AGENT` constant.
- Weather recipe: removed the {const}`recipes.weather.UNKNOWN` constant.

# 1.0.0

Release date: `2024-12-17`

## Bug Fixes

- Reworked images printing to, hopefully, fix all issues.
- Fixed printed lines counting in {meth}`ThermalPrinter.out()`.

## Features

- Support for QR701 printers is confirmed ({issue}`15`).
- New extra: `calendar`, to print daily stuff from your calendar, and birthdays as a bonus! See {ref}`recipes <calendar>`.
- New extra: `persian`, to make your life easier when printing Persian text, see {ref}`recipes <persian-text>`.
- New extra: `weather`, to print the weather alongside with the saint of the day! See {ref}`recipes <weather>`.
- New text styles: {meth}`ThermalPrinter.font_b()`, and {meth}`ThermalPrinter.left_blank()`.
- New options to tweak printer behaviors: `byte_time`, `dot_feed_time`, `dot_print_time`, `read_timeout`, and `write_timeout`. See {class}`ThermalPrinter`.
- New option to control printer settings at initialization to {class}`ThermalPrinter`: `run_setup_cmd=bool` ({issue}`15`).
- It is now possible to pass barcode styling instructions in {meth}`ThermalPrinter.barcode()`, in the same way it's done for {meth}`ThermalPrinter.out()`.
- Introduced statistics persisted at exit. This behavior can be disabled by passing `use_stats=False` to {class}`ThermalPrinter`.
- Enhanced the demonstration code.
- Rewrote the entire documentation to cover all possible stuff, and it is way prettier now, (thanks to the awesome [Shibuya theme](https://shibuya.lepture.com)).
- Improved the documentation by fixing issues found with [Harper](https://github.com/elijah-potter/harper).
- 100% tests coverage!
- Added lot of logs.

## Technical Changes

- Added the {const}`constants.Justify` constant to use in the {meth}`ThermalPrinter.justify()` method (**breaking change**).
- Added the {const}`constants.Size` constant to use in the {meth}`ThermalPrinter.size()` method (**breaking change**).
- Added the {const}`constants.Underline` constant to use in the {meth}`ThermalPrinter.underline()` method (**breaking change**).
- Added the {const}`constants.Defaults` constant. And they can be tweaked via `TP_*` environment variables.
- Added the {meth}`ThermalPrinter.__exit__()` method to properly close the printer when leaving the context manager.
- Added the {meth}`ThermalPrinter.has_paper` property.
- Added the {meth}`ThermalPrinter.close()` method.
- Added the {meth}`ThermalPrinter.demo()` method.
- Added the {meth}`ThermalPrinter.font_b()` method.
- Added the {meth}`ThermalPrinter.image_chunks()` method.
- Added the {meth}`ThermalPrinter.image_convert()` method.
- Added the {meth}`ThermalPrinter.image_resize()` method.
- Added the {meth}`ThermalPrinter.init()` method.
- Added the {meth}`ThermalPrinter.left_blank()` method.
- Added the {meth}`ThermalPrinter.status_to_dict()` method.
- Added the {func}`tools.stats_file()` function.
- Added the {func}`tools.stats_load()` function.
- Added the {func}`tools.stats_save()` function.
- Moved the {func}`tools.printer_tests()` function to the {meth}`ThermalPrinter.demo()` method (**breaking change**).
- Moved the {func}`tools.print_char()` function to the {meth}`ThermalPrinter.print_char()` method (**breaking change**).
- Moved the {func}`validate.validate_barcode()` function to the {meth}`ThermalPrinter.validate_barcode()` method.
- Removed the {file}`validate.py` file, and most `validate_*()` functions.
- Removed the {obj}`exceptions.ThermalPrinterConstantError` class.

# 0.3.0

Release date: `2024-11-02`

## Features

- Added support for Python 3.8, 3.9, 3.10, 3.11, 3.12, 3.13, and 3.14.
- Support for DP-EH400/1 printers is confirmed ({pull}`17`).
- Added type annotations.
- New option to specify commands timeout via `command_timeout=float)` in {class}`ThermalPrinter` ({pull}`17`).
- Documentation is now generated from the source code to never miss signature changes.
- Moved the CI from Travis-CI to GitHub actions.
- Run ruff on the entire source code.
- Added more quality checks.

## Technical Changes

- Drop support for Python 3.5, and 3.6.
- Renamed {func}`tools.test_char()` → {func}`tools.print_char()`.
- Renamed {func}`tools.testing()` → {func}`tools.printer_tests()`.
- No longer checks that the provided `image` argument to {meth}`ThermalPrinter.image()` is a {py:obj}`PIL.Image` object.

## Contributors

Thanks to our beloved contributors: {contributor}`uniphil`, {contributor}`d21d3q`

# 0.2.0

Release date: `2019-01-10`

## Bug Fixes

- Fixed image printing in {func}`tools.printer_tests()` when the module is installed. Will now raise an exception if `raise_on_error` argument is `True` (default).

## Features

- Add communication error in the {meth}`ThermalPrinter.status()` ({issue}`3`). Will now raise an exception if `raise_on_error` argument is `True` (default).
- Use {file}`setup.cfg` instead of {file}`setup.py`.

## Technical Changes

- Removed {obj}`exceptions.ThermalPrinterAttributeError` exception.
- Attributes {attr}`ThermalPrinter.is_online`, {attr}`ThermalPrinter.is_sleeping`, {attr}`ThermalPrinter.lines`, {attr}`ThermalPrinter.feeds` and {attr}`ThermalPrinter.max_column` now raise {py:obj}`AttributeError` when trying to set them (previously raising `ThermalPrinterAttributeError`).
- Changed the signature of {func}`tools.printer_tests(port='/dev/ttyAMA0', heat_time=80)` → {func}`tools.printer_tests(printer=None, raise_on_error=True)`.
- Changed the signature of {func}`tools.print_char(char)` → {func}`tools.print_char(char, printer=None)`.

## Contributors

Thanks to our beloved contributors: {contributor}`d21d3q`

# 0.1.0

Release date: `2016-05-24`

## Features

- First working version.

## Contributors

Thanks to our beloved contributors: {contributor}`phillipthelen`, and {contributor}`AKokkalas`

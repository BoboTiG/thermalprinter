# Changelog

## 0.3.0

### Features

- Add option to specify command timeout.
## 0.2.0

Release date: `2019-01-10`

### Bug Fixes

- Fixed image printing in `tools.testing()` when the module is installed. Will now raise an exception if `raise_on_error` argument is `True` (default).

### Features

- Add communication error in the `status()` (issue #3). Will now raise an exception if `raise_on_error` argument is `True` (default).
- Use `setup.cfg` instead of `setup.py`

### Technical Changes

- Removed `ThermalPrinterAttributeError` exception
- Attributes `is_online`, `is_sleeping`, `lines`, `feeds` and `max_column` now raise `AttributeError` when trying to set them (previously raising `ThermalPrinterAttributeError`)
- Changed signature of `tools.testing(port='/dev/ttyAMA0', heat_time=80)` -> `tools.testing(printer=None, raise_on_error=True)`
- Changed signature of `tools.test_char(char)` -> `tools.test_char(char, printer=None)`

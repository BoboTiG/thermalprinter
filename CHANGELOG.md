# Changelog

## 0.2.0

- Add communication error in the `status()` function (issue #3)
- Deleted ``ThermalPrinterAttributeError`` exception
  Attributes ``is_online``, ``is_sleeping``, ``lines``, ``feeds`` and ``max_column`` now raise ``AttributeError`` when trying to set them (previously raising ``ThermalPrinterAttributeError``)
- Use `setup.cfg` instead of `setup.py`

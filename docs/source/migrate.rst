============
🕊️ Migration
============

From v0.3 to v1.0
=================

.. currentmodule:: thermalprinter

- :func:`ThermalPrinter.justify()`:

  .. code-block:: diff

    + from thermalprinter import Justify

    - printer.justify("L")
    + printer.justify(Justify.LEFT)
    
    - printer.justify("C")
    + printer.justify(Justify.CENTER)

    - printer.justify("R")
    + printer.justify(Justify.RIGHT)

- :func:`ThermalPrinter.size()`:

  .. code-block:: diff

    + from thermalprinter import Size

    - printer.size("S")
    + printer.size(Size.SMALL)
    
    - printer.size("M")
    + printer.size(Size.MEDIUM)

    - printer.size("L")
    + printer.size(Size.LARGE)

- :func:`ThermalPrinter.underline()`:

  .. code-block:: diff

    + from thermalprinter import Underline

    - printer.underline(0)
    + printer.underline(Underline.OFF)
    
    - printer.underline(1)
    + printer.underline(Underline.THIN)

    - printer.underline(2)
    + printer.underline(Underline.THICK)

From v0.2 to v0.3
=================

.. currentmodule:: thermalprinter

- :func:`tools.test_char()` → :func:`tools.print_char()`:

  .. code-block:: diff

    - from thermalprinter.tools import test_char
    + from thermalprinter.tools import print_char

    - test_char("现")
    + print_char("现")

- :func:`tools.testing()` → :func:`tools.printer_tests()`:

  .. code-block:: diff

    - from thermalprinter.tools import testing
    + from thermalprinter.tools import printer_tests

    - testing()
    + printer_tests()

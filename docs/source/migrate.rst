=========
Migration
=========

From v0.3 to v0.4
=================

`justify()`
~~~~~~~~~~~

Code in v0.3:

.. code-block:: python

    printer.justify("L")
    printer.justify("C")
    printer.justify("R")

Code in v0.4:

.. code-block:: python

    from thermalprinter.constants import Justify

    printer.justify(Justify.LEFT)
    printer.justify(Justify.CENTER)
    printer.justify(Justify.RIGHT)

`size()`
~~~~~~~~

Code in v0.3:

.. code-block:: python

    printer.size("S")
    printer.size("M")
    printer.size("L")

Code in v0.4:

.. code-block:: python

    from thermalprinter.constants import Size

    printer.size(Size.SMALL)
    printer.size(Size.MEDIUM)
    printer.size(Size.LARGE)

`underline()`
~~~~~~~~~~~~~

Code in v0.3:

.. code-block:: python

    printer.underline(0)
    printer.underline(1)
    printer.underline(2)

Code in v0.4:

.. code-block:: python

    from thermalprinter.constants import Underline

    printer.underline(Underline.OFF)
    printer.underline(Underline.THIN)
    printer.underline(Underline.THICK)

From v0.2 to v0.3
=================

Tools
~~~~~

Code in v0.2:

.. code-block:: python

    tools.test_char("现")
    tools.testing()

Code in v0.3:

.. code-block:: python

    tools.print_char("现")
    tools.printer_tests()

========
🧾 Usage
========

.. currentmodule:: thermalprinter


Instantiate the Class
=====================

Import the module:

.. code-block:: python

    from thermalprinter import ThermalPrinter

So the module can be used as a context manager:

.. code-block:: python

    with ThermalPrinter() as printer:
        # ...

Or:

.. code-block:: python

    printer = ThermalPrinter()

Refer to the :func:`ThermalPrinter()` documentation for potential keyword-arguments.

A World of Infinite Possibilities
=================================

An example is better than a thousand words:

.. code-block:: python

    with ThermalPrinter() as printer:
        printer.out("Show time, here comes the demonstration!")
        printer.feed()
        printer.demo()

Where you can see the :func:`ThermalPrinter.demo()` source code right here:

.. literalinclude:: ../../src/thermalprinter/thermalprinter.py
    :pyobject: ThermalPrinter.demo
    :dedent:
    :language: python

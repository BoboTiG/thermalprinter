=====
Usage
=====

An example is better than a thousand words:

.. literalinclude:: ../../README.md
    :lines: 35-79
    :language: python

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

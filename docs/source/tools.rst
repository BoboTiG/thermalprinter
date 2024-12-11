========
🧰 Tools
========

.. module:: thermalprinter.tools

Constants
=========

.. autofunction:: ls

Statistics
==========

Simple printer statistics can be persisted into the :const:`thermalprinter.constants.STATS_FILE` file. They are enabled by default unless ``use_stats`` is set to ``False`` (see :func:`thermalprinter.ThermalPrinter()`).

.. autofunction:: stats_file
.. autofunction:: stats_load
.. autofunction:: stats_save

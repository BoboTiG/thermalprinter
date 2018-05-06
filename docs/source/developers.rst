.. highlight:: sh

==========
Developers
==========

Setup
=====

1. First, you need to fork the `GitHub repository <https://github.com/BoboTiG/thermalprinter>`_.

    **Note :** always work on a **specific branch** dedicated to your patch.

2. Then, you could need the :download:`Embedded printer DP-EH600 Technical Manual <../Embedded printer DP-EH600 Technical Manual.pdf>` and take a look at the `features advancement <https://github.com/BoboTiG/thermalprinter/issues/1>`_.
3. Finally, be sure to add/update tests and documentation within your patch.


Testing
=======

Dependency
----------

You will need `pytest <https://pypi.python.org/pypi/pytest>`_:

.. code-block:: bash

    python3 -m pip install --upgrade --user pytest


Adding/changing a method
------------------------

Before all, you will add a test file for the new method. Then, there is a test file called ``test_methods.py`` where all functions signatures are specified. Here is a little help to add a new one.

1. Say we want to find the signature of the ``size`` function:

.. code-block:: python

    >>> from thermalprinter import ThermalPrinter
    >>> from inspect import getargspec

    >>> getargspec(ThermalPrinter.size)
    ArgSpec(args=['self', 'value'], varargs=None, keywords=None, defaults=('S',))

2. Copy the all line ``ArgSpec(...)``.
3. Open the ``test_methods.py`` file and add a new test case, keep it sorted:

.. code-block:: python

    # Syntax of the function's name: test_signature_FUNCTION
    def test_signature_size(methods):
        methods.remove(extract_stack(None, 2)[1][2].replace('test_signature_', ''))

        # Here, you paste the ArgSpec(...) line
        sig = ArgSpec(args=['self', 'value'], varargs=None, keywords=None,
                      defaults=('S',))

        # And here you use the function's name too
        assert getargspec(ThermalPrinter.size) == sig

To summary, there are 3 modifications to apply, all functions in this file use the same syntax.


How to test?
------------

Enable the developer mode:

.. code-block:: bash

    python3 setup.py develop

Lauch the test suit:

.. code-block:: bash

    python3 -m pytest

And you can :doc:`test printing functions <tools>` (if you added a styling method, you can add it to this function).


Validating the code
===================

It is important to keep a clean base code. Use tools like `flake8 <https://pypi.python.org/pypi/flake8>`_ and `Pylint <https://pypi.python.org/pypi/pylint>`_.

Dependencies
------------

Install required packages:

.. code-block:: bash

    python3 -m pip install --upgrade --user flake8 pylint


How to validate?
----------------

.. code-block:: bash

    flake8
    pylint3 thermalprinter

If there is no output, you are good ;)


Documentation
=============

Dependencies
------------

You will need `Sphinx <http://sphinx-doc.org/>`_:

.. code-block:: bash

    python3 -m pip install --upgrade --user sphinx


How to build?
-------------

.. code-block:: bash

    cd docs
    make clean html

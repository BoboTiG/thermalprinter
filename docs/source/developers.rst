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

    sphinx-build --color -W -bhtml docs/source docs/output

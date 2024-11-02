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

Dependencies
------------

Install required packages:

.. code-block:: bash

    python -m pip install -e '.[tests]'


How to test?
------------

.. code-block:: bash

    python -m pytest

And you can :doc:`test printing functions <tools>` (if you added a styling method, you can add it to this function).


Validating the code
===================

It is important to keep a clean base code.

Dependencies
------------

Install required packages:

.. code-block:: bash

    python -m pip install -e '.[lint]'


How to validate?
----------------

.. code-block:: bash

    ./checks.sh


Documentation
=============

Dependencies
------------

Install required packages:

.. code-block:: bash

    python -m pip install -e '.[docs]'


How to build?
-------------

.. code-block:: bash

    sphinx-build --color -W -bhtml docs/source docs/output

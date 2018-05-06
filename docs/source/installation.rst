.. highlight:: sh

============
Installation
============

Dependencies
============

The only dependency is `pySerial <https://github.com/pyserial/pyserial>`_ (version 3.0+):

.. code-block:: bash

    python3 -m pip install --upgrade --user pyserial

For Python < 3.4, you will need to install *Enum* too:

.. code-block:: bash

    python3 -m pip install --upgrade --user enum34


Recommended way
===============

Quite simple:

.. code-block:: bash

    python3 -m pip install --upgrade --user thermalprinter


From sources
============

Alternatively, you can get a copy of the module from GitHub.

1. Clone the repository:

.. code-block:: bash

    git clone https://github.com/BoboTiG/thermalprinter.git
    cd thermalprinter

2. Install them module:

.. code-block:: bash

    python3 setup.py install --user

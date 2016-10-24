.. highlight:: sh

============
Installation
============

Dependencies
============

The only dependency is `pySerial <https://github.com/pyserial/pyserial>`_ (version 3.0+)::

    pip install pyserial

For Python < 3.4, you will need to install *Enum* too::

    pip install enum34


Recommended way
===============

Quite simple::

    pip install thermalprinter


From sources
============

Alternatively, you can get a copy of the module from GitHub.

1. Clone the repository::

    git clone https://github.com/BoboTiG/thermalprinter.git
    cd thermalprinter

2. Install them module::

    sudo python3 setup.py install

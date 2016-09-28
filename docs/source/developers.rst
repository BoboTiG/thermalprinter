==========
Developers
==========

First, you need to fork the `GitHub repos <https://github.com/BoboTiG/thermalprinter>`_.

**/!\\ Important:** always work on a specific branch dedicated to your patch.

Then, you could need the :download:`Embedded printer DP-EH600 Technical Manual <../Embedded printer DP-EH600 Technical Manual.pdf>` and take a look at the `features advancement <https://github.com/BoboTiG/thermalprinter/issues/1>`_.

Finally, be sure to add/update tests and documentation within your patch.

Dependencies
============

For the tests, you will need pytest::

    pip3 install pytest

To build the documentation, you will need Sphinx and the Read the Docs's theme::

    pip3 install sphinx sphinx_rtd_theme


Building
========

To build the documentation::

    cd docs
    make clean html


Testing
=======

Enable the developer mode::

    sudo python3 setup.py develop

Lauch the test suit::

    py.test-3

And you can :doc:`test printing functions <tools>`.

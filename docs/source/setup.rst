=====
Setup
=====

Raspberry Pi
============

*Note :* tested on Raspberry Pi 2 and 3.

1. Ensure that ``ttyAMA0`` is not used for serial console access. Edit the file ``/boot/cmdline.txt`` to remove all name-value pairs containing ``ttyAMA0``.
2. Add the user to the **dialout** group:

.. code-block:: bash

    sudo usermod -a -G dialout USER

3. Reboot.


Beagle Bone
===========

**Note :** documentation retrieved from `luopio/py-thermal-printer  <https://github.com/luopio/py-thermal-printer/blob/master/printer.py#L17>`_ and has not been tested.

.. code-block:: bash

    # Mux settings
    echo 1 > /sys/kernel/debug/omap_mux/spi0_sclk
    echo 1 > /sys/kernel/debug/omap_mux/spi0_d0


Other?
======

If you work with another hardware, please `tell us <https://github.com/BoboTiG/thermalprinter/issues>`_ :)

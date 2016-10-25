.. highlight:: shell

============
Installation
============

The embedded LCRS command line is available from within the built images that
are booted by clients booted from the LCRS PXE server or from ISO images.

You may invoke it as a classic python library, but it serves no purpose on a
regular system unless you want to wipe its hard drive.

To simulate usage, refer to the tests.

When installing within the embedded system, Buildroot is used. For installing it
within this environment, a script is called invoking normal python setup
procedure ``pip install -e .`` or ``python setup.py install``, however it's
also combined with installation of a relocatable virtualenv.

The concept is this::

    mkdir -p buildroot/linked_buildroot/output/target/usr/bin
    pip install . -t buildroot/linked_buildroot/output/target/usr/lib/python3.5/site-packages/ --install-option="--install-scripts=buildroot/linked_buildroot/output/target/usr/bin" --upgrade

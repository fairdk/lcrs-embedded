Developer guide
===============

For an overview, refer to the Makefile and various entrypoints. This section
contains guides to developing environments etc.

Contents:

.. toctree::
   :maxdepth: 2

   buildroot

Getting started
---------------

In order to build a bootable image with the LCRS CLI, you need to download
`Buildroot <https://buildroot.org>`__. You also need these dependencies::

    sudo apt-get install build-essential ncurses-base ncurses-bin libncurses5-dev dialog gcc-multilib g++ g++-multilib


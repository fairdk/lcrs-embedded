.. include:: ../README.rst

Getting started
---------------

In order to build a kernel, you need to download
`Buildroot <https://buildroot.org>`__. You also need these dependencies::

    sudo apt-get install build-essential ncurses-base ncurses-bin libncurses5-dev dialog gcc-multilib g++ g++-multilib

Make sure to have the
`Buildroot manual <https://buildroot.org/downloads/manual/manual.html#_getting_started>`__
at hand!

Copy the ``.config`` file from the Git repo into the location where you have
unpacked Buildroot, then run the ncurses configuration program::

    make nconfig



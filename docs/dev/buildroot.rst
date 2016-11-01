Buildroot configuration
=======================

In order to mess with the buildroot stuff and create new images containing the
LCRS CLI, you need some build root skills.

The main entry point is the Makefile which will run scripts that prompt you for
typical questions to get bootstrapped.

This is an documentation of the various choices made regarding the Buildroot
configuration.

Make sure to have the
`Buildroot manual <https://buildroot.org/downloads/manual/manual.html#_getting_started>`__
at hand!

Copying the ``.config-dist`` file should happen by running the Make target, if
you have a buildroot environment at hand, run this to see the configuration::

    make nconfig


Buildroot settings
------------------

- Root password: ``unset``, meaning there's no password for the root user.
- Default DHCP device: ``eth0``


Buildroot features
------------------

Before setting up the environment, consider that it takes quite a lot of storage
space (~6 GB), so you might wanna put it on a different drive.

Furthermore, after building, you cannot relocate. You would have to rebuild.
This is a well-known issue in Buildroot.

Toolchain:

Remember if you change the configuration of the toolchain, you need to rebuild
everything with ``make clean``.

 - Wchar
 - C++ support (because of smartmontools)

The following is compiled into the distributed Buildroot

System configuration:

 - /dev management with mdev
 - Network interface for DHCP: eth0 

Packages

 - bz2
 - dt
 - fio
 - ramspeed
 - stress

 - cpio
 - squashfs w/ gzip

 - Linux binary firmware for all Ethernet
 - dmidecode
 - fan-ctrl
 - hwdata
 - kdb (keyboard tables)
 - lm-sensors
 - memtester
 - pciutils (lspci)
 - sdparm
 - sg3utils w/ programs
 - smartmontools
 - sysstat
 - wipe
 - python3
    - All internal modules enabled
    - python-socketio

 Libraries
 Hardware handling
 - lbusb

 Networking
 - 

 Other
 - mcrypt

 Text and terminal handling
 - libiconv
 - ncurses w/ wide-char (utf-8 handling) + ncurses programs
 - newt

Network applications:

 - dhcpcd
 - dhcpdump
 - dropbear
 - ethtool
 - iputils
 - macchanger
 - netplug
 - ntp

Shell utilities:

 - None
 
System tools:

 - cpuload
 - htop
 - keyutils

Text editors:

 - nano

Maybe?
~~~~~~

 - ramspeed/smp
 - stress-ng
 
Filesystem images
~~~~~~~~~~~~~~~~~

 - ext2 root file system
 - initial RAM filesystem linked into linux kernel
 - iso image (isolinux)
 - squashfs root

Bootloaders
~~~~~~~~~~~

 - syslinux w/ isolinux + pxelinux


Test-driven development (TDD)
=============================

This program is written with
`TDD <https://en.wikipedia.org/wiki/Test-driven_development>`__ in mind.

The most sensitive parts of the suite of commands that are run are guided by a
philosophy that all functions should guarantee their intended outcomes, but
still have to rely on their respective system calls.

.. warning:: If something doesn't work, fail loudly. Throw exceptions, go mad.

Test philosophy
---------------

#. Define data structures, the main object to refer to is
:class:`lcrs_embedded.models.ScanResult`
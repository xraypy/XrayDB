Installation
=====================================

.. _xraydb.sqlite: https://github.com/xraypy/XrayDB/blob/master/xraydb.sqlite?raw=true
.. _xrayDB on github.com: https://github.com/xraypy/XrayDB/
.. _pytest: https://pytest.org/

The X-ray database is held in the SQLite3 file ``xraydb.sqlite``.  If you
are looking for direct use with SQLite, you can download this from here:
`xraydb.sqlite`_.


To install the XrayDB Python module (which includes the sqlite database), use::

   pip install xraydb

Depending on your system and Python installation, you may need
administrative privileges or to use `sudo` to install to a system-installed
Python environment.

.. Note:: The Python module supports Python 3.8 and above.


Development Version
~~~~~~~~~~~~~~~~~~~~~~~~

To work with the data sources or to add or modify data in the XrayDB, you
will want to clone or download the full source code kit
`xrayDB on github.com`_ which contains the current database, original
source data, python module, and files for generating the Periodic Table
posters. To get the latest development version,  use::

   git clone https://github.com/xraypy/XrayDB.git

Testing
~~~~~~~~~~

There are a set of tests scripts for the Python interface that can be run with
the `pytest`_ testing framework.  These are located in the ``python/tests``
folder. These tests are automatically run as part of the development process.
For any release or any master branch from the git repository, running
``pytest`` should run all of these tests to completion without errors or
failures.

Copyright, Licensing, and Re-distribution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../LICENSE
  :language: none

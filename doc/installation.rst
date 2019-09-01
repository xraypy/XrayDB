Installation
=====================================

.. _xraydb.sqlite: https://github.com/xraypy/XrayDB/blob/master/xraydb.sqlite?raw=true
.. _xrayDB on github.com: https://github.com/xraypy/XrayDB/

The X-ray database is held in the SQLite3 file ``xraydb.sqlite``.  If you
are looking for dirrect use with SQLite, you can download this from
`xraydb.sqlite`_.


If you want to use XrayDB from Python, install the XrayDB Python module
(which includes the sqlite database), with::

   pip install xraydb

If you are using Anaconda Python, you can also install with::

   conda install -c gsecars xraydb

Depending on your system and Python installation, you may need
administrative privileges to install any python library.  For many linux
and Mac OS X systems, you may need to use `sudo`.

.. Note:: The Python module supports Python 3.5 and above.


To work with the data sources or to add or modify data in the XrayDB, you
will want to clone or download the full source code kit
`xrayDB on github.com`_ which contains the current database, original
source data, python module, and files for generating the Periodic Table
posters.

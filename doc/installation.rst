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

.. Note:: The Python module supports Python 3.9 and above.


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


Acknowledgements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The project began with the data from the compilation of basic atomic
properties and X-ray absorption edge energies, emission energies, and
absorption cross sections from :cite:`Elam_Ravel_Sieber`, who
assembled data from a several sources. The original code to store this
with SQLite was written by Darren S. Dale (see
https://github.com/praxes/elam_physical_reference) from CHESS.  More
data has been added from other sources.  Energy widths of core holes
for excited electronic levels from :cite:`Keski_Krause` and
:cite:`Krause_Oliver`.  Elastic X-ray scattering data, :math:`f_0(q)`
is taken from :cite:`Waasmaier_Kirfel`.  Resonant scattering cross
sections :math:`f'(E)` and :math:`f''(E)` and absorption cross
sections from :cite:`Chantler` as from
https://www.nist.gov/pml/data/ffast/index.cfm, but on a finer energy
grid been provided directly by Christopher T. Chantler
:cite:`Chantler2016`.  Nathan Whittington from U Tennessee and Roman
Chernikov from BNL provided the code to calculate reflectivity of
multilayer and coated mirrors.  Code for better calculation of sample
thicknesses for XAFS transmission samples was provided by easyXAFS.
Most of the remaining code was written and is maintained by Matt
Newville, though with contributions from many others.


Citing this work
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To cite this work, please use  https://zenodo.org/badge/latestdoi/205441660


Copyright, Licensing, and Re-distribution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The original sources of the data included here are mostly based on published
works with the clear intent of providing data to the general public.  Some of
the datasets here do not have clear statements of copyright or license, but
have been freely available for many years. The work here is a compilation and
reformatting of those datasets.

To the extent possible, and unless otherwise stated, the database files, data
sources, and documentation files here are placed in the public domain, using
the Creative Commons 1.0 Universal (CC0 1.0) Public Domain Dedication below.

As an important note, the Python code in the `xraydb` package is
copyrighted and available under the terms of the MIT License.


.. literalinclude:: ../LICENSE
  :language: none

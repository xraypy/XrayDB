.. xraydb documentation master file

X-ray DB: X-ray Reference Data in SQLite
========================================

.. _XrayDB Github Page:  https://github.com/xraypy/XrayDB
.. _FFAST webpage:       https://www.nist.gov/pml/data/ffast/index.cfm
.. _PDF Version of this documentation:  https://xraypy.github.io/XrayDB/xraydb.pdf
.. _XrayDB Web App (xrayabsorption.org):  https://xraydb.xrayabsorption.org/
.. _XrayDB Web App (CARS, U Chicago):  https://millenia.cars.aps.anl.gov/xraydb

XrayDB provides atomic data, characteristic X-ray energies, and X-ray cross
sections for the elements in an SQLite3 database, ``xraydb.sqlite``.  This
file can be used directly with SQLite :cite:`sqlite` using standard SQL, or
from the many programming language that support SQLite.  Some of the
components of the database hold arrays of numbers which are stored in the
database as JSON-encoded strings, and will need to be unpacked to be used.

A Python module providing an interface to this database is also provided here.

The project began with the data from the compilation of basic atomic
properties and X-ray absorption edge energies, emission energies, and
absorption cross sections from :cite:`Elam_Ravel_Sieber`, who assembled
data from a several sources.  More data has been added from other sources.
Energy widths of core holes for excited electronic levels from
:cite:`Keski_Krause` and :cite:`Krause_Oliver`.  Elastic X-ray scattering
data, :math:`f_0(q)` is taken from :cite:`Waasmaier_Kirfel`.  Resonant
scattering cross sections :math:`f'(E)` and :math:`f''(E)` and absorption
cross sections from :cite:`Chantler` as from the `FFAST webpage`_ (but on
a finer energy grid, data from :cite:`Chantler2016`) are also included.

The values here use units that are SI and commonly used in X-ray work.
Cross sections are in cm^2/gr, and energies are in eV.  Energy-dependent
data for cross-sections are typically most reliable between about 250 eV to
about 250,000 eV.  Elements from Z=1 to 92 are supported, with some data
are included for elements between Z=93 and Z=98.

The current version of the XrayDB database is **9.1**, and the version of the
Python module is |release|.  A few useful resources using this library include:

   * `XrayDB Web App (xrayabsorption.org)`_ is an interactive web applications
     to browse the data in this database and make plots of X-ray attenuation,
     scattering factors, mirror reflectivity, and more.  Data tables and python
     code to generate that data are available for many of the calculations.

   * :ref:`periodic_tables` for printable Poster-sized Periodic tables of X-ray energies.

   * `XrayDB Github Page`_ has data sources, code, development and issues.

   * `PDF Version of this documentation`_


Table of Contents
-----------------------

.. toctree::
   :maxdepth: 3

   installation
   periodictable
   examples
   python
   overview
   dbschema
   biblio

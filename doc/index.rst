.. xraydb documentation master file

X-ray DB: X-ray Reference Data in SQLite
========================================

.. _XrayDB Github Page:  https://github.com/xraypy/XrayDB
.. _FFAST webpage:       https://www.nist.gov/pml/data/ffast/index.cfm

.. _PDF Version of this documentation:  https://xraypy.github.io/XrayDB/xraydb.pdf

XrayDB provides atomic data, characteristic X-ray energies, and X-ray cross
sections for the elements in an SQLite3 database, ``xraydb.sqlite``.  This
file can be used directly with SQLite :cite:`sqlite` using standard SQL, or
from the many programming language that suppor SQLite.  A Python module
providing such an interface is provided here.

Because some of the components of the database hold arrays of numbers
(for example, coefficients for interpolation), the arrays are stored in the
database as JSON-encoded strings, and will need to be unpacked to be used.

The project began with the data from the compilation of basic atomic
properties and X-ray absorption edge energies, emission energies, and
absorption cross sections from :cite:`Elam_Ravel_Sieber`, who assembled
data from a several sources.  More data has been added from other sources.
Energy widths of core holes for excited electronic levels from
:cite:`Keski_Krause` and :cite:`Krause_Oliver`.  Elastic X-ray scattering
data, :math:`f_0(q)` is taken from :cite:`Waasmaier_Kirfel`.  Resonant
scattering cross sections :math:`f'(E)` and :math:`f''(E)` and absorption
cross sections from :cite:`Chantler` (as from the `FFAST webpage`_) are
also included.

In general, cross sections are in cm^2/gr, and energies are given in eV.
Energy-dependent data for cross-sections are typically valid between about
250 eV to about 200,000 eV.  Elements with Z=1 to 92 are supported, and
some data is included for elements between Z=93 and Z=98.

   * The current version of the XrayDB is 4, and the Version for the Python
     module is |release|.

   * See `XrayDB Github Page`_ for data sources, code, development, and
     issues.

   * A `PDF Version of this documentation`_ is available.

Table of Contents
-----------------------

.. toctree::
   :maxdepth: 3

   installation
   periodictable
   overview
   dbschema
   python
   examples
   biblio

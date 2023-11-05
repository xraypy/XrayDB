Using the XrayDB  xraydb.sqlite
=====================================

All the data for the X-ray database is held in the SQLite3 file
``xraydb.sqlite``.  To use with SQLite, this file is all you need.  While
many programs and languages can access SQLite files, basic
usage with the ``sqlite3`` program (available from Windows, Mac OS X, and
Linux) can be as simple as::

   system~> sqlite3 xraydb.sqlite
   sqlite> .headers on
   sqlite> select * from elements where atomic_number=47;
   atomic_number|element|name|molar_mass|density
   47|Ag|silver|107.868|10.48


That is, you can retrieve the data using standard SQL queries built-in to
SQLite.  Of course, the expectation is that you'd want to use this database
within a programming environment.  Currently, wrappers exist only for
Python.


Overall Database Schema
-----------------------------

The schema for the SQLite3 database describes where data is held in the
database, and how to access it.  The schema for the current version (4)
looks like this::

    Table Version (id integer primary key,
                   tag text,
                   date text,
                   notes text);
    Table elements (atomic_number integer primary key,
                    element text,
                    name text,
                    molar_mass real,
                    density real);
    Table xray_levels (id integer primary key,
                       element text,
                       iupac_symbol text,
                       absorption_edge real,
                       fluorescence_yield real,
                       jump_ratio real);
    Table xray_transitions (id integer primary key,
                            element text,
                            iupac_symbol text,
                            siegbahn_symbol text,
                            initial_level text,
                            final_level text,
                            emission_energy real,
                            intensity real);
    Table Coster_Kronig (id integer primary key,
                         element text,
                         initial_level text,
                         final_level text,
                         transition_probability real,
                         total_transition_probability real);
    Table photoabsorption (id integer primary key,
                           element text,
                           log_energy text,
                           log_photoabsorption text,
                           log_photoabsorption_spline text);
    Table scattering (id integer primary key,
                      element text,
                      log_energy text,
                      log_coherent_scatter text,
                      log_coherent_scatter_spline text,
                      log_incoherent_scatter text,
                      log_incoherent_scatter_spline text);
    Table Waasmaier (id integer primary key,
                     atomic_number integer,
                     element text,
                     ion text,
                     offset real,
                     scale text,
                     exponents text);
    Table KeskiRahkonen_Krause (id integer primary key,
                                atomic_number integer,
                                element text,
                                edge text,
                                width float);
    Table Krause_Oliver (id integer primary key,
                         atomic_number integer,
                         element text,
                         edge text,
                         width float);
    Table corelevel_widths (id integer primary key,
                            atomic_number integer,
                            element text,
                            edge text,
                            width float);
    Table Chantler (id integer primary key,
                    element text,
                    sigma_mu real,
                    mue_f2 real,
                    density real,
                    corr_henke float,
                    corr_cl35 float,
                    corr_nucl float,
                    energy text,
                    f1 text,
                    f2 text,
                    mu_photo text,
                    mu_incoh text,
                    mu_total text);



More details for each table are given below.

.. note::

  in the tables below the type of `json array` means that arrays of numerical
  data are stored in the database as text of JSON-encoded arrays.

.. _db_version_sect:

Version Table
-----------------

The `Version` table holds data about the revisions to the database file
itself.  Each row represents a single revision.


.. index:: DB Table of Database Versions
.. _db_version_table:

   DB Table of Database Versions

    +----------------------+--------------+---------------------------------------+
    |  Column              |  Type        | Description                           |
    +======================+==============+=======================================+
    |  id                  | integer      | counter (primary tag)                 |
    +----------------------+--------------+---------------------------------------+
    |  tag                 |  text        | version name                          |
    +----------------------+--------------+---------------------------------------+
    |  date                |  text        | date string                           |
    +----------------------+--------------+---------------------------------------+
    |  notes               |  text        | notes on changes for version          |
    +----------------------+--------------+---------------------------------------+

.. _db_elements_sect:

Elements Table
-----------------

The `elements` table holds basic data about each element.  Each row
represents an element.


.. index:: DB Table of Basic Properties of the Elements
.. _db_elements_table:

   DB Table of Basic Properties of the Elements

    +----------------------+--------------+---------------------------------------+
    |  Column              |  Type        | Description                           |
    +======================+==============+=======================================+
    |  atomic_number       | integer      | Atomic Number, Z                      |
    +----------------------+--------------+---------------------------------------+
    |  element             | text         | Atomic symbol                         |
    +----------------------+--------------+---------------------------------------+
    |  name                | text         | English name of element               |
    +----------------------+--------------+---------------------------------------+
    |  molar_mass          |  float       | Atomic mass in AMU                    |
    +----------------------+--------------+---------------------------------------+
    |  density             |  float       | Density of pure element (gr/cm^3)     |
    +----------------------+--------------+---------------------------------------+

.. _db_xray_levels_sect:

Xray_Levels Table
------------------------

The `xray_levels` table holds data for electronic levels of atoms.  Each row
represents a core electronic level.

.. index:: DB Table of X-ray Levels
.. _db_xray_levels_table:

   DB Table of X-ray and core electronic levels.  `fluorescence yield`
   gives the probability of an empty level refilling by X-ray
   fluorescence. The `jump ratio` is the ratio of values for photo-electric
   cross section (that is, from :ref:`db_photoabsorption_sect`) 1 eV above
   the absorption edge to that 1 eV below the absorption edge.  See
   :ref:`Table of X-ray Edges <xraydb-edge_table>`

    +----------------------+--------------+---------------------------------------+
    |  Column              |  Type        | Description                           |
    +======================+==============+=======================================+
    |  id                  | integer      | Index (primary key)                   |
    +----------------------+--------------+---------------------------------------+
    | element              |  text        | Atomic symbol for element             |
    +----------------------+--------------+---------------------------------------+
    | iupac_symbol         |  text        | IUPAC symbol for level ('K','L3',...) |
    +----------------------+--------------+---------------------------------------+
    | absorption_edge      |  float       | binding energy for level (eV)         |
    +----------------------+--------------+---------------------------------------+
    | fluorescence_yield   |  float       | fluorescence yield (fraction)         |
    +----------------------+--------------+---------------------------------------+
    | jump_ratio           |  float       | ratio of mu_photo across edge         |
    +----------------------+--------------+---------------------------------------+

.. _db_xray_trans_sect:

Xray_Transitions Table
------------------------

The `xray_transitions` table holds data for transitions between electronic levels
of atoms.  Each row represents a transition between two levels.

.. index:: DB Table of X-ray Transitions
.. _db_xray_trans_table:

   DB Table of X-ray Transitions.  Both IUPAC and Siegbahn symbols are given (see
   :ref:`Table of X-ray emission lines <xraydb-lines_table>`), as
   well as the initial and final levels.  The `intensity` is the relative
   intensity of the transition for a given `initial level`.

    +----------------------+--------------+---------------------------------------+
    |  Column              |  Type        | Description                           |
    +======================+==============+=======================================+
    |  id                  | integer      | Index (primary key)                   |
    +----------------------+--------------+---------------------------------------+
    | element              |  text        | Atomic symbol for element             |
    +----------------------+--------------+---------------------------------------+
    | iupac_symbol         |  text        | IUPAC symbol for transition           |
    +----------------------+--------------+---------------------------------------+
    | siegbahn_symbol      |  text        | Siegbahn symbol for transition        |
    +----------------------+--------------+---------------------------------------+
    | initial_level        |  text        | IUPAC symbol for initial level        |
    +----------------------+--------------+---------------------------------------+
    | final_level          |  text        | IUPAC symbol for final level          |
    +----------------------+--------------+---------------------------------------+
    | emission_energy      |  float       | fluorescence energy (eV)              |
    +----------------------+--------------+---------------------------------------+
    | intensity            |  float       | relative intensity for transition     |
    +----------------------+--------------+---------------------------------------+

.. _db_photoabsorption_sect:

Photoabsorption Table
------------------------

The `photoabsorption` table holds data for the photo-electric absorption
cross sections in cm^2/gr.  Each row represents an element.

.. index:: DB Table of Photoabsorption Cross Sections
.. _db_photoabsorption_table:

   DB Table of Photoabsorption Cross Sections.  JSON-encoded arrays are held
   for logs of energy, cross section, and cross section spline (second
   derivative useful for spline interpolation).

    +----------------------------+--------------+---------------------------------------+
    |  Column                    |  Type        | Description                           |
    +============================+==============+=======================================+
    |  id                        | integer      | Index (primary key)                   |
    +----------------------------+--------------+---------------------------------------+
    | element                    |  text        | Atomic symbol for element             |
    +----------------------------+--------------+---------------------------------------+
    | log_energy                 |  json array  | log of Energy values (eV)             |
    +----------------------------+--------------+---------------------------------------+
    | log_photoabsorption        |  json array  | log of cross section (cm^2/gr)        |
    +----------------------------+--------------+---------------------------------------+
    | log_photoabsorption_spline |  json array  | log of cross section spline           |
    +----------------------------+--------------+---------------------------------------+

.. _db_scattering_sect:

Scattering Table
------------------------

The `scattering` table holds data for the coherent and incoherent X-ray scattering
cross sections, in cm^2/gr.  Each row represents an element.

.. index:: DB Table of Coherent and Incoherent Scattering Cross Sections
.. _db_scattering_table:

   DB Table of Coherent and Incoherent Scattering Cross Sections.  JSON-encoded
   arrays are held for logs of energy, cross section, and cross section spline
   (second derivative useful for spline interpolation).

    +-------------------------------+--------------+---------------------------------------+
    |  Column                       |  Type        | Description                           |
    +===============================+==============+=======================================+
    |  id                           | integer      | Index (primary key)                   |
    +-------------------------------+--------------+---------------------------------------+
    | element                       |  text        | Atomic symbol for element             |
    +-------------------------------+--------------+---------------------------------------+
    | log_energy                    |  json array  | log of Energy values (eV)             |
    +-------------------------------+--------------+---------------------------------------+
    | log_coherent_scatter          |  json array  | log of cross section (cm^2/gr)        |
    +-------------------------------+--------------+---------------------------------------+
    | log_coherent_scatter_spline   |  json array  | log of cross section spline           |
    +-------------------------------+--------------+---------------------------------------+
    | log_incoherent_scatter        |  json array  | log of cross section (cm^2/gr)        |
    +-------------------------------+--------------+---------------------------------------+
    | log_incoherent_scatter_spline |  json array  | log of cross section spline           |
    +-------------------------------+--------------+---------------------------------------+

.. _db_costerkronig_sect:

Coster_Kronig Table
------------------------

The `Coster_Kronig` table holds data for energy levels, partial and total
transition probabilities for the Coster-Kronig transitions (Auger processes
in which the empty core level is filled from an electron in a higher level
with the same principle quantum number).  The partial probability describes
direct transitions, while the total probability includes cascade effects.
Each row represents a transition.


.. index:: DB Table of Coster-Kronig Transitions
.. _db_costerkronig_table:

   DB Table of Coster-Kronig Transitions.

    +-------------------------------+--------------+---------------------------------------+
    |  Column                       |  Type        | Description                           |
    +===============================+==============+=======================================+
    |  id                           | integer      | Index (primary key)                   |
    +-------------------------------+--------------+---------------------------------------+
    | element                       |  text        | Atomic symbol for element             |
    +-------------------------------+--------------+---------------------------------------+
    | initial_level                 |  text        | IUPAC symbol for initial level        |
    +-------------------------------+--------------+---------------------------------------+
    | final_level                   |  text        | IUPAC symbol for final level          |
    +-------------------------------+--------------+---------------------------------------+
    | transition_probability        |  float       | direct transition probability         |
    +-------------------------------+--------------+---------------------------------------+
    | total_transition_probability  |  float       | total transition probability          |
    +-------------------------------+--------------+---------------------------------------+

.. _db_waasmaier_sect:

Waasmaier Table
------------------------

The `Waasmaier` table holds data for calculating elastic X-ray scattering
factors :math:`f_0(k)`, from :cite:`Waasmaier_Kirfel`.  The scattering
factor is unitless, and :math:`k=\sin(\theta)/\lambda` where :math:`\theta`
is the scattering angle and :math:`\lambda` is the X-ray wavelength.
available for many common ionic states for each element.  Each row
represents an ion.

.. index:: DB Table of Elastic Scattering Cross Section Coefficients
.. _db_waasmaier_table:

   DB Table of Elastic Scattering Cross Section Coefficients

    +-------------------------------+--------------+---------------------------------------+
    |  Column                       |  Type        | Description                           |
    +===============================+==============+=======================================+
    |  id                           | integer      | Index (primary key)                   |
    +-------------------------------+--------------+---------------------------------------+
    |  atomic_number                | integer      | Atomic Number, Z                      |
    +-------------------------------+--------------+---------------------------------------+
    | element                       |  text        | Atomic symbol for element             |
    +-------------------------------+--------------+---------------------------------------+
    | ion                           |  text        | symbol for element and ionization     |
    +-------------------------------+--------------+---------------------------------------+
    | offset                        |  float       | offset value                          |
    +-------------------------------+--------------+---------------------------------------+
    | scale                         |  json array  | coefficients for calculation          |
    +-------------------------------+--------------+---------------------------------------+
    | exponents                     |  json array  | coefficients for calculation          |
    +-------------------------------+--------------+---------------------------------------+


.. _db_keski_sect:

KeskiRahkonen_Krause Table
------------------------------

The `KeskiRahkonen_Krause` table holds data for energy widths of the core electronic
levels from :cite:`Keski_Krause`.  Values are in eV, and each row represents an
energy level for an element.

.. index:: DB Table of Core Hole Widths
.. _db_keski_table:

   DB Table of Core Hole Widths from Keski-Rahkonen and Krause

    +-------------------------------+--------------+---------------------------------------+
    |  Column                       |  Type        | Description                           |
    +===============================+==============+=======================================+
    |  id                           | integer      | Index (primary key)                   |
    +-------------------------------+--------------+---------------------------------------+
    |  atomic_number                | integer      | Atomic Number, Z                      |
    +-------------------------------+--------------+---------------------------------------+
    | element                       |  text        | Atomic symbol for element             |
    +-------------------------------+--------------+---------------------------------------+
    | edge                          |  text        | IUPAC symbol for energy level ('K')   |
    +-------------------------------+--------------+---------------------------------------+
    | width                         |  float       | width of level (eV)                   |
    +-------------------------------+--------------+---------------------------------------+



Krause_Oliver Table
------------------------------

The `Krause_Oliver` table holds data for energy widths of the core electronic
levels from :cite:`Krause_Oliver`.  Values are in eV, and each row represents an
energy level for an element.

.. index:: DB Table of Core Hole Widths
.. _db_krause_table:

   DB Table of Core Hole Widths from Krause and Oliver

    +-------------------------------+--------------+---------------------------------------+
    |  Column                       |  Type        | Description                           |
    +===============================+==============+=======================================+
    |  id                           | integer      | Index (primary key)                   |
    +-------------------------------+--------------+---------------------------------------+
    |  atomic_number                | integer      | Atomic Number, Z                      |
    +-------------------------------+--------------+---------------------------------------+
    | element                       |  text        | Atomic symbol for element             |
    +-------------------------------+--------------+---------------------------------------+
    | edge                          |  text        | IUPAC symbol for energy level ('K')   |
    +-------------------------------+--------------+---------------------------------------+
    | width                         |  float       | width of level (eV)                   |
    +-------------------------------+--------------+---------------------------------------+


Compton Energies  Table
------------------------------

The `Compton_energies` table holds data for median (90 deg scattering) and mean
values of the energies of Compton scattered X-rays, and the mean values of the
Compton-scattered electrons as a function of incident X-ray energy.  There is
only 1 row in this table, with all columns being json-encoded arrays of floats.
These values should be finely-spaced enough for linear interpolation


.. index:: DB Table of Compton Energies
.. _db_compton_table:

   DB Table of Compton-scattered energies.

    +---------------------------+--------------+---------------------------------------+
    |  Column                   |  Type        | Description                           |
    +===========================+==============+=======================================+
    |  incident                 | json_array   | Incident X-ray energies (eV)          |
    +---------------------------+--------------+---------------------------------------+
    |  xray_90deg               | json_array   | Median scattered X-ray energies (eV)  |
    +---------------------------+--------------+---------------------------------------+
    |  xray_mean                | json_array   | Mean scattered X-ray energies (eV)    |
    +---------------------------+--------------+---------------------------------------+
    |  electron_mean            | json_array   | Mean scattered electron energies (eV) |
    +---------------------------+--------------+---------------------------------------+



.. _db_chantler_sect:

Chantler Table
------------------------------

The `Chantler` table holds data for resonant X-ray scattering factors
:math:`f'(E)` and :math:`f''(E)` as well as photo-electric absorption,
coherent, and incoherent scattering factors from :cite:`Chantler`.  As
with other tables, scattering factors are unitless, and cross sections are
in cm^2/gr. Each row represents an element.

.. index:: DB Table of resonant scattering and mass attenuation coefficients from Chantler
.. _db_chantler_table:

   DB Table of resonant scattering and mass attenuation coefficients from Chantler.

    +-------------------------------+--------------+---------------------------------------+
    |  Column                       |  Type        | Description                           |
    +===============================+==============+=======================================+
    |  id                           | integer      | Index (primary key)                   |
    +-------------------------------+--------------+---------------------------------------+
    | element                       |  text        | Atomic symbol for element             |
    +-------------------------------+--------------+---------------------------------------+
    | mue_f2                        |  float       | factor to convert mu(E) to f''(E)     |
    +-------------------------------+--------------+---------------------------------------+
    | density                       |  float       | atomic density (gr/cm^3)              |
    +-------------------------------+--------------+---------------------------------------+
    | corr_henke                    |  float       | Henke correction to f`(E)             |
    +-------------------------------+--------------+---------------------------------------+
    | corr_cl35                     |  float       | Cromer-Liberman correction to f`(E)   |
    +-------------------------------+--------------+---------------------------------------+
    | corr_nucl                     |  float       | nuclear correction to f`(E)           |
    +-------------------------------+--------------+---------------------------------------+
    | energy                        |  json array  | energies for interpolation            |
    +-------------------------------+--------------+---------------------------------------+
    | f1                            |  json array  | f'(E)    (e)                          |
    +-------------------------------+--------------+---------------------------------------+
    | f2                            |  json array  | f''(E)   (e)                          |
    +-------------------------------+--------------+---------------------------------------+
    | mu_photo                      |  json array  | photoabsorption mu(E)  (cm^2/gr)      |
    +-------------------------------+--------------+---------------------------------------+
    | mu_incoh                      |  json array  | incoherent scattering  (cm^2/gr)      |
    +-------------------------------+--------------+---------------------------------------+
    | mu_total                      |  json array  | total attenuation (cm^2/gr)           |
    +-------------------------------+--------------+---------------------------------------+

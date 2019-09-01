Overview of Atomic and X-ray Data
======================================

The data provided in XrayDB includes Atomic data and characteristic
energies and cross sections for the interaction of X-rays with elements.  A
few definitions and conventions necessary for using this data are discussed
here.


Elements
-----------

Most of the data resources are accessed by an elements *Atomic Symbol*.
For the Python module, most methods will take `element` as the first
argument, and this can either be the integer atomic number or the string
for the atomic symbol.

Elemental densities are given in gr/cm^3, and molar masses are given in
AMU.

X-ray Edges
--------------

Several resources (database tables, python methods) take either an ``edge``
or a ``level`` argument to signify a core electronic level.  These must be
one of the levels listed in the :ref:`Table of X-ray edge names
<xraydb-edge_table>`.

.. index:: Table of X-ray Edges
.. _xraydb-edge_table:

   Table of X-ray Edges and Core electronic levels.  The Names are the
   IUPAC symbols for the core electronic levels.

    +-----+-------------------+-----+-------------------+
    |Name |electronic level   |Name |electronic level   |
    +=====+===================+=====+===================+
    | K   | :math:`1s`        | N5  | :math:`4d_{5/2}`  |
    +-----+-------------------+-----+-------------------+
    | L3  | :math:`2p_{3/2}`  | N4  | :math:`4d_{3/2}`  |
    +-----+-------------------+-----+-------------------+
    | L2  | :math:`2p_{1/2}`  | N3  | :math:`4p_{3/2}`  |
    +-----+-------------------+-----+-------------------+
    | L1  | :math:`2s`        | N2  | :math:`4p_{1/2}`  |
    +-----+-------------------+-----+-------------------+
    | M5  | :math:`3d_{5/2}`  | N1  | :math:`4s`        |
    +-----+-------------------+-----+-------------------+
    | M4  | :math:`3d_{3/2}`  | O3  |  :math:`5p_{3/2}` |
    +-----+-------------------+-----+-------------------+
    | M3  | :math:`3p_{3/2}`  | O2  |  :math:`5p_{1/2}` |
    +-----+-------------------+-----+-------------------+
    | M2  | :math:`3p_{1/2}`  | O1  |  :math:`5s`       |
    +-----+-------------------+-----+-------------------+
    | M1  | :math:`3s`        | P3  |  :math:`6p_{3/2}` |
    +-----+-------------------+-----+-------------------+
    | N7  | :math:`4f_{7/2}`  | P2  |  :math:`6p_{1/2}` |
    +-----+-------------------+-----+-------------------+
    | N6  | :math:`4f_{5/2}`  | P1  |  :math:`6s`       |
    +-----+-------------------+-----+-------------------+


X-ray Lines
--------------

Many resources (database tables or methods) take emission line arguments.
These follow the latinized version of the Siegbahn notation as indicated in
the :ref:`Table of X-ray emission line names <xraydb-lines_table>`.


.. index:: Table of X-ray emission lines
.. _xraydb-lines_table:

    Table of X-ray emission line names and the corresponding Siegbahn and IUPAC notations

   +--------+-----------+-----------------------------+--------+-------------+-----------------------------+
   | Name   | IUPAC     | Siegbahn                    | Name   | IUPAC       | Siegbahn                    |
   +========+===========+=============================+========+=============+=============================+
   | Ka1    | K-L3      | :math:`K\alpha_1`           | Lb4    | L1-M2       | :math:`L\beta_4`            |
   +--------+-----------+-----------------------------+--------+-------------+-----------------------------+
   | Ka2    | K-L2      | :math:`K\alpha_2`           | Lb5    | L3-O4,5     | :math:`L\beta_5`            |
   +--------+-----------+-----------------------------+--------+-------------+-----------------------------+
   | Ka3    | K-L1      | :math:`K\alpha_3`           | Lb6    | L3-N1       | :math:`L\beta_6`            |
   +--------+-----------+-----------------------------+--------+-------------+-----------------------------+
   | Kb1    | K-M3      | :math:`K\beta_1`            | Lg1    | L2-N4       | :math:`L\gamma_1`           |
   +--------+-----------+-----------------------------+--------+-------------+-----------------------------+
   | Kb2    | K-N2,3    | :math:`K\beta_2`            | Lg2    | L1-N2       | :math:`L\gamma_2`           |
   +--------+-----------+-----------------------------+--------+-------------+-----------------------------+
   | Kb3    | K-M2      | :math:`K\beta_3`            | Lg3    | L1-N3       | :math:`L\gamma_3`           |
   +--------+-----------+-----------------------------+--------+-------------+-----------------------------+
   | Kb4    | K-N4,5    | :math:`K\beta_2`            | Lg6    | L2-O4       | :math:`L\gamma_6`           |
   +--------+-----------+-----------------------------+--------+-------------+-----------------------------+
   | Kb5    | K-M4,5    | :math:`K\beta_3`            | Ll     | L3-M1       | :math:`Ll`                  |
   +--------+-----------+-----------------------------+--------+-------------+-----------------------------+
   | La1    | L3-M5     | :math:`L\alpha_1`           | Ln     | L2-M1       | :math:`L\nu`                |
   +--------+-----------+-----------------------------+--------+-------------+-----------------------------+
   | La2    | L3-M4     | :math:`L\alpha_1`           | Ma     | M5-N6,7     | :math:`M\alpha`             |
   +--------+-----------+-----------------------------+--------+-------------+-----------------------------+
   | Lb1    | L2-M4     | :math:`L\beta_1`            | Mb     | M4-N6       | :math:`M\beta`              |
   +--------+-----------+-----------------------------+--------+-------------+-----------------------------+
   | Lb2,15 | L3-N4,5   |:math:`L\beta_2,L\beta_{15}` | Mg     | M3-N5       | :math:`M\gamma`             |
   +--------+-----------+-----------------------------+--------+-------------+-----------------------------+
   | Lb3    | L1-M3     | :math:`L\beta_3`            | Mz     | M4,5-N6,7   | :math:`M\zeta`              |
   +--------+-----------+-----------------------------+--------+-------------+-----------------------------+

Energies
---------------

Unless otherwise stated, all energies are in units of eV.


Cross Sections
------------------

The photoabsorption and scattering cross sections from :cite:`Elam_Ravel_Sieber`
and :cite:`Chantler` are in cm^2/gr.

The data from :cite:`Elam_Ravel_Sieber` is held as logarithms of energy, cross
section, and logarithm of the 2nd derivative of cross section that allows
for cubic spline interpolation in log-log space.

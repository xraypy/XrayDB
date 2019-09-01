Using XrayDB from Python
=========================


The wrappers/python directly contains a Python module for XrayDB.  This
module gives a higher-level wrapping of the XrayDB, including the
conversion of data from json-encoded data to numpy arrays.  The module
requires the json, numpy, and sqlalchemy modules, and can be installed
with::

    python setup.py install


XrayDB module
---------------

.. module:: xraydb

To use the XrayDB from python, create an instance, and start using it:

    >>> from xraydb import XrayDB
    >>> xdb = XrayDB()
    >>> xdb.xray_edge('Ag', 'K')
    XrayEdge(edge=25514.0, fyield=0.821892, jump_ratio=6.334)


.. index:: XrayDB methods
.. _xraydb-methods_table:

    Table of XrayDB methods for Atomic and X-ray data for the elements.
    calculate and return some element-specific properties, given the
    element symbol or atomic number.  Most data extends to Z=98 (Cf), but
    much data for elements with atomic number > 92 (U) may not be
    available, and may not be very reliable when provided.  Except where
    noted, the data comes from :cite:`Elam_Ravel_Sieber`.

     ===================================== =======================================================================
      XrayDB method                              description
     ===================================== =======================================================================
      :meth:`XrayDB.atomic_number`           atomic number from symbol
      :meth:`XrayDB.atomic_number`           atomic number from symbol
      :meth:`XrayDB.symbol`                  atomic symbol from number
      :meth:`XrayDB.molar_mass`              atomic mass
      :meth:`XrayDB.density`                 density of pure element
      :meth:`XrayDB.xray_edge`               xray edge data for a particular element and edge
      :meth:`XrayDB.xray_edges`              dictionary of all X-ray edges data for an element
      :meth:`XrayDB.xray_lines`              dictionary of all X-ray emission line data for an element
      :meth:`XrayDB.xray_line_strengths`     absolute line strength in cm^2/gr for all available lines
      :meth:`XrayDB.mu_elam`                 absorption cross sectionm photo-electric or total
      :meth:`XrayDB.cross_section_elam`      photo-electric, coherent, or incoherent cross sections.
      :meth:`XrayDB.corehole_width`          core level width for an element and edge (:cite:`Keski_Krause`)
      :meth:`XrayDB.f0`                      elastic scattering factor (:cite:`Waasmaier_Kirfel`)
      :meth:`XrayDB.f0_ions`                 list of valid "ions" for :meth:`f0`  (:cite:`Waasmaier_Kirfel`)
      :meth:`XrayDB.chantler_energies`       energies of tabulation for Chantler data (:cite:`Chantler`)
      :meth:`XrayDB.f1_chantler`             :math:`f'(E)` anomalous scattering factor (:cite:`Chantler`)
      :meth:`XrayDB.f2_chantler`             :math:`f"(E)` anomalous scattering factor (:cite:`Chantler`)
      :meth:`XrayDB.mu_chantler`             absorption cross section (:cite:`Chantler`)
     ===================================== =======================================================================


.. autoclass:: XrayDB

    .. automethod:: atomic_number

    .. automethod:: symbol

    .. automethod:: molar_mass

    .. automethod:: density

    .. automethod:: xray_edges

    .. automethod:: xray_edge

    .. automethod:: xray_lines

    .. automethod:: xray_line_strengths

    .. automethod:: ck_probability

    .. automethod:: corehole_width

    .. automethod:: cross_section_elam

    .. automethod:: mu_elam

    .. automethod:: chantler_energies

    .. automethod:: f1_chantler

    .. automethod:: f2_chantler

    .. automethod:: mu_chantler

    .. automethod:: f0_ions

    .. automethod:: f0

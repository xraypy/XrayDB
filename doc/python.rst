Using XrayDB from Python
=========================


The `python` directory contains the source code for a Python module for
XrayDB.  This module gives a user-friendly wrapping of the XrayDB, and
automates the the conversion of data from sqlite database into Python and
numpy arrays. The module requires the numpy, scipy and sqlalchemy modules,
and can be installed with::

    pip install xraydb


The Python xraydb module
----------------------------------



To use the XrayDB from Python, you can import the `xraydb` module and start
using it:

    >>> import xraydb
    >>> xraydb.xray_edge('Ag', 'K')
    XrayEdge(energy=25514.0, fyield=0.821892, jump_ratio=6.334)


.. index:: methods of the xraydb Python module
.. _xraydb-methods_table:

    Table of XrayDB methods for Atomic and X-ray data for the elements.
    calculate and return some element-specific properties, given the
    element symbol or atomic number.  Most data extends to Z=98 (Cf), but
    much data for elements with atomic number > 92 (U) may not be
    available, and may not be very reliable when provided.  Except where
    noted, the data comes from :cite:`Elam_Ravel_Sieber`.

     =============================== =======================================================================
      xraydb method                              description
     =============================== =======================================================================
      :meth:`atomic_number`           atomic number from symbol
      :meth:`atomic_symbol`           atomic symbol from number
      :meth:`atomic_mass`             atomic mass
      :meth:`atomic_density`          density of pure element
      :meth:`xray_edge`               xray edge data for a particular element and edge
      :meth:`xray_edges`              dictionary of all X-ray edges data for an element
      :meth:`xray_lines`              dictionary of all X-ray emission line data for an element
      :meth:`mu_elam`                 absorption cross sectionm photo-electric or total
      :meth:`core_width`              core level width for an element and edge (:cite:`Keski_Krause`)
      :meth:`f0`                      elastic scattering factor (:cite:`Waasmaier_Kirfel`)
      :meth:`f0_ions`                 list of valid "ions" for :meth:`f0`  (:cite:`Waasmaier_Kirfel`)
      :meth:`chantler_energies`       energies of tabulation for Chantler data (:cite:`Chantler`)
      :meth:`f1_chantler`             :math:`f'(E)` anomalous scattering factor (:cite:`Chantler`)
      :meth:`f2_chantler`             :math:`f"(E)` anomalous scattering factor (:cite:`Chantler`)
      :meth:`mu_chantler`             absorption cross section (:cite:`Chantler`)
     =============================== =======================================================================



.. module:: xraydb

.. automethod:: xray.atomic_number

.. automethod:: xray.atomic_symbol

.. automethod:: xray.atomic_mass

.. automethod:: xray.atomic_density

.. automethod:: xray.f0

.. automethod:: xray.f0_ions


.. automethod:: xray.xray_edge

.. automethod:: xray.xray_edges

.. automethod:: xray.xray_lines

.. automethod:: xray.ck_probability

.. automethod:: xray.core_width

.. automethod:: xray.mu_elam

.. automethod:: xray.coherent_cross_section_elam

.. automethod:: xray.incoherent_cross_section_elam

.. automethod:: xray.chantler_energies

.. automethod:: xray.f1_chantler

.. automethod:: xray.f2_chantler

.. automethod:: xray.mu_chantler


.. automethod:: chemparser.chemparse

.. automethod:: materials.material_mu

.. automethod:: materials.material_mu_components

.. automethod:: materials.get_material

.. automethod:: materials.add_material

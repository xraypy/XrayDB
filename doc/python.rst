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

.. module:: xraydb

To use the XrayDB from Python, you can import the `xraydb` module and start
using it:

    >>> import xraydb
    >>> xraydb.xray_edge('Ag', 'K')
    XrayEdge(energy=25514.0, fyield=0.821892, jump_ratio=6.334)


.. index:: xraydb Python module
.. _xraydb-function_table:

   **Table of XrayDB function for Atomic and X-ray data for the elements**

   Most of these function return some element-specific property from the
   element symbol or atomic number.  Some of the data extends to Z=98 (Cf),
   but some data may not be available for Z > 92 (U).  Except where noted,
   the data comes from :cite:`Elam_Ravel_Sieber`.

     ======================================= =======================================================================
      xraydb functions                             description
     ======================================= =======================================================================
      :func:`atomic_number`                   atomic number from symbol
      :func:`atomic_symbol`                   atomic symbol from number
      :func:`atomic_mass`                     atomic mass
      :func:`atomic_density`                  density of pure element
      :func:`f0`                              elastic scattering factor (:cite:`Waasmaier_Kirfel`)
      :func:`f0_ions`                         list of valid "ions" for :func:`f0`  (:cite:`Waasmaier_Kirfel`)
      :func:`xray_edge`                       xray edge data for a particular element and edge
      :func:`xray_edges`                      dictionary of all X-ray edges data for an element
      :func:`xray_lines`                      dictionary of all X-ray emission line data for an element
      :func:`fluor_yield`                     fluorescent yield for an X-ray emission line
      :func:`ck_probability`                  Coster-Kronig transition probability between two atomic levels
      :func:`mu_elam`                         absorption cross-section, photo-electric or total for an element
      :func:`coherent_cross_section_elam`     coherent scattering cross-section for an element
      :func:`incoherent_cross_section_elam`   incoherent scattering cross-section for an element
      :func:`chantler_energies`               energies of tabulation for Chantler data (:cite:`Chantler`)
      :func:`f1_chantler`                     :math:`f'(E)` anomalous scattering factor (:cite:`Chantler`)
      :func:`f2_chantler`                     :math:`f"(E)` anomalous scattering factor (:cite:`Chantler`)
      :func:`mu_chantler`                     absorption cross section (:cite:`Chantler`)
      :func:`guess_edge`                      guess element and edge from energy of absorption edge
      :func:`chemparse`                       parse a chemical formula to atomic abundances
      :func:`material_mu`                     absorption cross-section for a material at X-ray energies
      :func:`material_mu_components`          dictionary of elemental components of `mu` for material
      :func:`get_material`                    get a material (name, formula, density from materials database
      :func:`add_material`                    add a material (name, formula, density) to local materials database
      :func:`xray_delta_beta`                 return anomalous index of refraction for material and energy
     ======================================= =======================================================================

:mod:`xraydb` functions
------------------------------


.. autofunction:: atomic_number

.. autofunction:: atomic_symbol

.. autofunction:: atomic_mass

.. autofunction:: atomic_density

.. autofunction:: f0

.. autofunction:: f0_ions

.. autofunction:: xray_edge

.. autofunction:: xray_edges

.. autofunction:: xray_lines

.. autofunction:: fluor_yield

.. autofunction:: ck_probability

.. autofunction:: core_width

.. autofunction:: mu_elam

.. autofunction:: coherent_cross_section_elam

.. autofunction:: incoherent_cross_section_elam

.. autofunction:: chantler_energies

.. autofunction:: f1_chantler

.. autofunction:: f2_chantler

.. autofunction:: mu_chantler

.. autofunction:: guess_edge

.. autofunction:: xray_delta_beta

.. autofunction:: chemparse

.. autofunction:: material_mu

.. autofunction:: material_mu_components

.. autofunction:: get_material

.. autofunction:: add_material

.. autofunction:: get_xraydb

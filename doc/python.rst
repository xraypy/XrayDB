Using XrayDB from Python
=========================


The `python` directory contains the source code for a Python module for
XrayDB.  This module gives a user-friendly wrapping of the XrayDB, and
automates the the conversion of data from sqlite database into Python and
numpy arrays. The module requires the `numpy`, `scipy` and `sqlalchemy`
modules, all of which are readily available and can be installed with::

    pip install xraydb

The current version of the Python module is |release|, corresponding to
version 4 of `xraydb.sqlite`.

The Python xraydb module
----------------------------------

.. module:: xraydb

To use the XrayDB from Python, you can import the `xraydb` module and start
using it:

    >>> import xraydb
    >>> xraydb.atomic_number('Ag')
    47
    #
    # X-ray elastic (Thomson) scattering factors:
    >>> import numpy as np
    >>> q =np.linspace(0, 5, 11)
    >>> xraydb.f0('Fe', q)
    array([25.994603  , 11.50848469,  6.55945765,  4.71039413,  3.21048827,
           2.20939146,  1.65112769,  1.36705887,  1.21133507,  1.10155689,
           1.0035555 ])
    #
    # X-ray emission lines:
    >>> for name, line in xraydb.xray_lines('Zn', 'K').items():
    ...     print(name, ' = ', line)
    ...
    Ka3  =  XrayLine(energy=8462.8, intensity=0.000316256, initial_level='K', final_level='L1')
    Ka2  =  XrayLine(energy=8614.1, intensity=0.294353, initial_level='K', final_level='L2')
    Ka1  =  XrayLine(energy=8637.2, intensity=0.576058, initial_level='K', final_level='L3')
    Kb3  =  XrayLine(energy=9567.6, intensity=0.0438347, initial_level='K', final_level='M2')
    Kb1  =  XrayLine(energy=9570.4, intensity=0.0846229, initial_level='K', final_level='M3')
    Kb5  =  XrayLine(energy=9648.8, intensity=0.000815698, initial_level='K', final_level='M4,5')
    #
    # X-ray absorption edges:
    >>> xraydb.xray_edge('As', 'K')
    XrayEdge(energy=11867.0, fyield=0.548989, jump_ratio=7.314)
    #
    # X-ray attenuation factors:
    >>> as_kedge = xraydb.xray_edge('As', 'K').energy
    >>> energies = np.linspace(-50, 50, 5) + as_kedge
    >>> muvals = xraydb.mu_elam('As', energies)
    >>> for en, mu in zip(energies, muvals):
    ...     print("{:.0f}   {:8.2f}".format(en, mu))
    ...
    11817      26.07
    11842      25.92
    11867      25.77
    11892     178.32
    11917     177.38

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
      :func:`mu_chantler`                     absorption cross-section (:cite:`Chantler`)
      :func:`guess_edge`                      guess element and edge from energy of absorption edge
      :func:`chemparse`                       parse a chemical formula to atomic abundances
      :func:`validate_formula`                test whether a chemical formula can be parsed.
      :func:`material_mu`                     absorption cross-section for a material at X-ray energies
      :func:`material_mu_components`          dictionary of elemental components of `mu` for material
      :func:`get_material`                    get a material (name, formula, density from materials database
      :func:`add_material`                    add a material (name, formula, density) to local materials database
      :func:`xray_delta_beta`                 return anomalous index of refraction for material and energy
     ======================================= =======================================================================

:mod:`xraydb` functions
------------------------------


Atomic Properties
~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: atomic_number

.. autofunction:: atomic_symbol

.. autofunction:: atomic_mass

.. autofunction:: atomic_density

Elastic Scattering Factors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: f0

.. autofunction:: f0_ions

X-ray Edges
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: xray_edge

.. autofunction:: xray_edges

.. autofunction:: core_width

.. autofunction:: guess_edge

X-ray Emission Lines
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: xray_lines

.. autofunction:: fluor_yield

.. autofunction:: ck_probability

Absorption and Scattering Cross-sections
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: mu_elam

.. autofunction:: coherent_cross_section_elam

.. autofunction:: incoherent_cross_section_elam

.. autofunction:: chantler_energies

.. autofunction:: f1_chantler

.. autofunction:: f2_chantler

.. autofunction:: mu_chantler

Chemical and Materials calculations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: xray_delta_beta

.. autofunction:: chemparse

.. autofunction:: validate_formula

.. autofunction:: material_mu

.. autofunction:: material_mu_components

.. autofunction:: get_material

.. autofunction:: add_material

.. autofunction:: get_xraydb

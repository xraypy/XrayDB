"""Python interface to XrayDB:

   X-ray Reference Data for the Elements

   last update: 30-August-2019
   License: Public Domain
   Author:  Matthew Newville <newville@cars.uchicago.edu>
            Center for Advanced Radiation Sources,
            The University of Chicago
"""


from .xraydb import XrayDB

from .chemparser import chemparse, validate_formula

from .materials import (material_mu, material_mu_components, get_materials,
                        get_material, find_material, add_material)

from .xray import (atomic_number, atomic_symbol, atomic_mass,
                   atomic_density, xray_edges, xray_edge, xray_lines,
                   xray_line, fluor_yield, ck_probability, core_width, f0,
                   f0_ions, chantler_energies, f1_chantler, f2_chantler,
                   mu_chantler, mu_elam, coherent_cross_section_elam,
                   incoherent_cross_section_elam, guess_edge,
                   xray_delta_beta, get_xraydb,
                   mirror_reflectivity, ionchamber_fluxes,
                   ionization_potential)

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

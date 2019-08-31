#!/usr/bin/env python
""" Tests of Larch Scripts  """
import time
import pytest
import numpy as np
from numpy.testing import assert_allclose

from xraydb import (chemparse, material_mu, material_mu_components,
                    get_material, add_material, f0, f0_ions,
                    chantler_energies, f1_chantler, f2_chantler,
                    mu_chantler, mu_elam, coherent_cross_section_elam,
                    incoherent_cross_section_elam, atomic_number,
                    atomic_symbol, atomic_mass, atomic_density, xray_edges,
                    xray_edge, xray_lines, xray_line, fluo_yield,
                    ck_probability, core_width, guess_edge,
                    xray_delta_beta, XrayDB)



def test_chemparse():
    examples = {'H2O': {'H':2, 'O':1},
                'Mn(SO4)2(H2O)7':  {'H': 14.0, 'S': 2.0, 'Mn': 1, 'O': 15.0},
                'Mg(SO4)2': {'Mg': 1, 'S': 2, 'O':8},
                'Mg0.5Fe0.5' : {'Mg': 0.5, 'Fe': 0.5},
                'CO': {'C': 1, 'O': 1},
                }

    for formula, cert in examples.items():
        ret = chemparse(formula)
        for elem, quant in cert.items():
            v = ret.pop(elem)
            assert_allclose(v, quant, rtol=1.e3)
        assert len(ret)==0

def test_atomic_data():
    assert atomic_number('zn') == 30
    assert atomic_symbol(26) == 'Fe'
    assert atomic_mass(45) > 102.8
    assert atomic_mass(45) < 103.0
    assert atomic_density(29) == atomic_density('cu')
    assert atomic_density(22) > 4.51


def test_edge_energies():
    from xraydb.xray import _edge_energies

    assert xray_edge(30, 'K') == xray_edge('Zn', 'K')

    for edge in ('k', 'l3', 'l2'):
        for iz in range(1, 98):
            _edge = xray_edge(iz, edge)
            if _edge is not None:
                en = _edge.energy
                assert _edge_energies[edge][iz] < en + 0.5
                assert _edge_energies[edge][iz] > en - 0.5

def test_emission_lines():
    cu_lines = xray_lines('Cu')
    for lname in ('Ka3', 'Ka2', 'Ka1', 'Kb3', 'Kb1', 'Kb5',
                  'Lb4', 'Lb3', 'Ln', 'Lb1', 'Ll', 'La2', 'La1'):
        assert(lname in cu_lines)

    assert cu_lines['Ka1'].energy > 8045.0
    assert cu_lines['Ka1'].energy < 8047.0
    assert cu_lines['Ka1'].initial_level == 'K'
    assert cu_lines['Ka1'].final_level == 'L3'

#!/usr/bin/env python
""" Tests of Larch Scripts  """
import os
import time
import shutil
import pytest
import numpy as np
from numpy.testing import assert_allclose

from xraydb import (chemparse, validate_formula, material_mu,
                    material_mu_components, find_material, get_materials,
                    get_material, add_material)

from xraydb.materials import get_user_materialsfile

def test_chemparse():
    examples = {'H2O': {'H':2, 'O':1},
                'Mn(SO4)2(H2O)7':  {'H': 14.0, 'S': 2.0, 'Mn': 1, 'O': 15.0},
                'Mg(SO4)2': {'Mg': 1, 'S': 2, 'O':8},
                'Mg0.5Fe0.5' : {'Mg': 0.5, 'Fe': 0.5},
                'CO': {'C': 1, 'O': 1} }
    for formula, cert in examples.items():
        ret = chemparse(formula)
        for elem, quant in cert.items():
            v = ret.pop(elem)
            assert_allclose(v, quant, rtol=1.e3)
        assert len(ret)==0

def test_validate_formula():
    examples = {'H2O': True,
                'Mn(SO4)2(H2O)7':  True,
                'Mn(SO42(H2O)7': False,
                'Z': False}
    for formula, cert in examples.items():
        ret = validate_formula(formula)
        assert (ret == cert)

def test_get_materials():
    examples = {'water': True, 'lead': True, 'acetone': True,
                'kapton': True, 'sapphire': True,
                'cheese': False, 'spice': False, 'bicycle': False}

    known_materials = get_materials()
    for name, found in examples.items():
        if found:
            assert (name in known_materials)
        else:
            assert (name not in known_materials)

def test_material_mu1():
    en = np.linspace(8500, 9500, 21)
    known_mu = np.array([236.2, 232.4, 228.7, 225.1, 221.5, 218.1, 214.7,
                         211.4, 208.1, 204.9, 1403.6, 1385.6, 1367.9, 1350.6,
                         1333.5, 1316.7, 1300.3, 1284.0, 1268.1, 1252.4,
                         1237.0])

    mu = material_mu('CuO', en, density=6.3)
    assert_allclose(mu, known_mu, rtol=0.005)

def test_material_mu2():
    en = np.linspace(5000, 10000, 21)
    known_mu = np.array([0.04934, 0.04267, 0.03715, 0.03254, 0.02866,
                         0.02538, 0.02257, 0.02016, 0.01809, 0.01629,
                         0.01472, 0.01334, 0.01214, 0.01108, 0.01014,
                         0.00930, 0.00856, 0.00789, 0.00729, 0.00675,
                         0.00626])

    mu = material_mu('air', en)
    assert_allclose(mu, known_mu, rtol=0.05)

    air_formula, air_density = get_material('air')

    air_comps = chemparse(air_formula)

    assert air_comps['Ar'] < 0.013
    assert air_comps['Ar'] > 0.007

    mu = material_mu('air', en, density=2.0*air_density)
    assert_allclose(mu, 2.0*known_mu, rtol=0.05)

def test_material_mu3():
    en = np.linspace(5000, 10000, 21)

    known_mu = np.array([42.592, 36.801, 32.006, 28.005, 24.641, 21.794,
                         19.367, 17.288, 15.496, 13.943, 12.592, 11.411,
                         10.373, 9.458, 8.649, 7.931, 7.291, 6.719, 6.206,
                         5.745, 5.330])

    mu = material_mu('H2O', en)
    assert_allclose(mu, known_mu, rtol=0.05)

def test_material_mu4():
    en = np.linspace(5000, 10000, 21)

    known_mu = np.array([42.592, 36.801, 32.006, 28.005, 24.641, 21.794,
                         19.367, 17.288, 15.496, 13.943, 12.592, 11.411,
                         10.373, 9.458, 8.649, 7.931, 7.291, 6.719, 6.206,
                         5.745, 5.330])

    with pytest.raises(Warning):
        out = material_mu('H2SO4', en)


def test_material_mu_components1():
    mu = material_mu('quartz', 10000)
    assert_allclose(mu, 50.368, rtol=0.001)

    comps = material_mu_components('quartz', 10000)

    known_comps =  {'mass': 60.08, 'density': 2.65, 'elements': ['Si', 'O'],
                    'Si': (1, 28.1, 33.879), 'O': (2.0, 16.0, 5.953)}


    assert 'Si'in comps['elements']
    assert 'O'in comps['elements']

    for attr in ('mass', 'density'):
        assert_allclose(comps[attr], known_comps[attr], rtol=0.01)

    for attr in ('Si', 'O'):
        assert_allclose(comps[attr][0], known_comps[attr][0], rtol=0.01)
        assert_allclose(comps[attr][1], known_comps[attr][1], rtol=0.01)
        assert_allclose(comps[attr][2], known_comps[attr][2], rtol=0.01)


def test_material_mu_components2():
    mu = material_mu('TiO2', 10000, density=4.23)
    assert_allclose(mu, 290.7, rtol=0.001)

    mu = material_mu('TiO2', 10000)
    assert_allclose(mu, 290.7, rtol=0.001)

    mu = material_mu('TiO2', 10000, density=4.5)
    assert_allclose(mu, 309.26, rtol=0.001)

    comps = material_mu_components('TiO2', 10000, density=4.23)


    known_comps =  {'mass': 79.88, 'density': 4.23, 'elements': ['Ti', 'O'],
                    'Ti': (1, 47.88, 110.676), 'O': (2.0, 15.9994, 5.953)}

    assert 'Ti'in comps['elements']
    assert 'O'in comps['elements']

    for attr in ('mass', 'density'):
        assert_allclose(comps[attr], known_comps[attr], rtol=0.01)

    for attr in ('Ti', 'O'):
        assert_allclose(comps[attr][0], known_comps[attr][0], rtol=0.01)
        assert_allclose(comps[attr][1], known_comps[attr][1], rtol=0.01)
        assert_allclose(comps[attr][2], known_comps[attr][2], rtol=0.01)

    with pytest.raises(Warning):
        c = material_mu_components('TiO2', 10000)


def test_material_find():
    mat_  = {'kapton': ('C22H10N2O5', 1.43, 'polymer'),
             'lead': ('Pb', 11.34, 'metal'),
             'aluminum': ('Al', 2.72, 'metal'),
             'water': ('H2O', 1.0, 'solvent')}
    for mname, mdat in mat_.items():
        mat = find_material(mname)
        f1 = chemparse(mat.formula)
        f2 = chemparse(mdat[0])
        for k, v in f2.items():
            assert v == f1[k]
        assert_allclose(mat.density, mdat[1], rtol=0.1)
        assert(mdat[2] in mat.categories)

    for formula in ('WSO3', 'CdAs140CO3', 'KAs'):
        out = find_material(formula)
        assert out == None


def test_material_get():
    mat_  = {'kapton': ('C22H10N2O5', 1.43),
             'lead': ('Pb', 11.34),
             'aluminum': ('Al', 2.72),
             'water': ('H2O', 1.0)}

    for mname in mat_.keys():
        formula, density = get_material(mname)
        f1 = chemparse(formula)
        f2 = chemparse(mat_[mname][0])
        for k, v in f2.items():
            assert v == f1[k]
        assert_allclose(density, mat_[mname][1], rtol=0.1)

    for formula, density in mat_.values():
        _f, _d = get_material(formula)
        assert _f == formula
        assert_allclose(density, _d, rtol=0.1)

    for formula in ('WSO3', 'CdAs140CO3', 'KAs'):
        out = get_material(formula)
        assert out == None


def test_material_add():
    matfile = get_user_materialsfile()
    savefile = matfile + '_Save'
    if os.path.exists(matfile):
        had_matfile = True
        shutil.move(matfile, savefile)
        time.sleep(2.0)

    add_material('caffeine', 'C8H10N4O2', density=1.23)
    assert get_material('caffeine') is not None

    time.sleep(2.0)

    add_material('rutile', 'TiO2', density=4.23)

    with open(matfile, 'r') as fh:
        text = fh.read()

    assert 'caffeine' in text
    assert 'rutile' in text

    os.unlink(matfile)
    if os.path.exists(savefile):
        shutil.move(savefile, matfile)

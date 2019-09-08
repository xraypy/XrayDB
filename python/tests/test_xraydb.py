#!/usr/bin/env python
""" Tests of xraydb interface  """
import time
import pytest
import numpy as np
from numpy.testing import assert_allclose

from xraydb import XrayDB

def test_xraydb_version():
    xdb = XrayDB()
    version = xdb.get_version()
    assert 'XrayDB Version: 4.0, Python' in version

    hist = xdb.get_version(with_history=True)
    assert len(hist) > 350
    hist = hist.split('\n')
    assert len(hist) > 4

def test_molar_mass():
    xdb = XrayDB()
    assert_allclose(xdb.molar_mass('Co'), 58.932, rtol=0.001)

    with pytest.raises(ValueError):
        xdb.molar_mass('Mx')

def test_density():
    xdb = XrayDB()
    assert_allclose(xdb.molar_mass('Pb'), 207.2, rtol=0.001)

    with pytest.raises(ValueError):
        xdb.density('Mx')

def test_atomic_number():
    xdb = XrayDB()
    assert xdb.atomic_number('Ne') == 10

    with pytest.raises(ValueError):
        xdb.atomic_number('Mx')

def test_symbol():
    xdb = XrayDB()
    assert xdb.symbol(40) == 'Zr'

def test_xray_line_strengths():
    xdb = XrayDB()
    assert len(xdb.xray_line_strengths('Hg', excitation_energy=2800)) == 2
    assert len(xdb.xray_line_strengths('Hg', excitation_energy=12000)) == 3
    assert len(xdb.xray_line_strengths('Hg', excitation_energy=12500)) == 9
    assert len(xdb.xray_line_strengths('Hg', excitation_energy=14300)) == 13
    assert len(xdb.xray_line_strengths('Hg', excitation_energy=16000)) == 17

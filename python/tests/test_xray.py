#!/usr/bin/env python
""" Tests of xray interface  """
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
                    xray_edge, xray_lines, xray_line, fluor_yield,
                    ck_probability, core_width, guess_edge,
                    xray_delta_beta, mirror_reflectivity,
                    ionchamber_fluxes, XrayDB)


from xraydb.xray import chantler_data

def test_atomic_data():
    assert atomic_number('zn') == 30
    assert atomic_symbol(26) == 'Fe'
    assert atomic_mass(45) > 102.8
    assert atomic_mass(45) < 103.0
    assert atomic_density(29) == atomic_density('cu')
    assert atomic_density(22) > 4.50
    assert atomic_density(79) > 19.2


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

    assert_allclose(xray_edge('Zn', 'K', energy_only=True), 9660, rtol=0.01)

    sr_edges = xray_edges('Sr')

    assert_allclose(sr_edges['K'].energy, 16105.0,  rtol=0.001)
    assert_allclose(sr_edges['L1'].energy, 2216.0, rtol=0.001)
    assert_allclose(sr_edges['L2'].energy, 2007.0, rtol=0.001)
    assert_allclose(sr_edges['L3'].energy, 1940.0, rtol=0.001)
    assert_allclose(sr_edges['M1'].energy, 358.7, rtol=0.001)
    assert_allclose(sr_edges['M2'].energy, 280.3, rtol=0.001)
    assert_allclose(sr_edges['M3'].energy, 270.0, rtol=0.001)
    assert_allclose(sr_edges['M4'].energy, 136.0, rtol=0.001)
    assert_allclose(sr_edges['M5'].energy, 134.2, rtol=0.001)
    assert_allclose(sr_edges['N1'].energy, 38.9, rtol=0.001)
    assert_allclose(sr_edges['N2'].energy, 21.6, rtol=0.001)
    assert_allclose(sr_edges['N3'].energy, 20.1, rtol=0.001)


    assert_allclose(sr_edges['K'].fyield, 0.664652, rtol=0.001)
    assert_allclose(sr_edges['L1'].fyield, 0.0051, rtol=0.001)
    assert_allclose(sr_edges['L2'].fyield, 0.024, rtol=0.001)
    assert_allclose(sr_edges['L3'].fyield, 0.026, rtol=0.001)
    assert_allclose(sr_edges['M1'].fyield, 5.95e-05, rtol=0.001)
    assert_allclose(sr_edges['M2'].fyield, 3.7e-05, rtol=0.001)
    assert_allclose(sr_edges['M3'].fyield, 0.000105, rtol=0.001)
    assert_allclose(sr_edges['M4'].fyield, 0.0027, rtol=0.001)
    assert_allclose(sr_edges['M5'].fyield, 0.0, rtol=0.001)
    assert_allclose(sr_edges['N1'].fyield, 1.2e-05, rtol=0.001)
    assert_allclose(sr_edges['N2'].fyield, 0.013, rtol=0.001)
    assert_allclose(sr_edges['N3'].fyield, 0.013, rtol=0.001)


    assert_allclose(sr_edges['K'].jump_ratio, 6.888, rtol=0.01)
    assert_allclose(sr_edges['L1'].jump_ratio, 1.1415, rtol=0.01)
    assert_allclose(sr_edges['L2'].jump_ratio, 1.4, rtol=0.01)
    assert_allclose(sr_edges['L3'].jump_ratio, 3.982, rtol=0.01)
    assert_allclose(sr_edges['M1'].jump_ratio, 1.04, rtol=0.01)
    assert_allclose(sr_edges['M2'].jump_ratio, 1.058, rtol=0.01)
    assert_allclose(sr_edges['M3'].jump_ratio, 1.12491, rtol=0.01)
    assert_allclose(sr_edges['M4'].jump_ratio, 1.139, rtol=0.01)
    assert_allclose(sr_edges['M5'].jump_ratio, 1.808, rtol=0.01)
    assert_allclose(sr_edges['N1'].jump_ratio, 1.0, rtol=0.01)
    assert_allclose(sr_edges['N2'].jump_ratio, 1.0, rtol=0.01)
    assert_allclose(sr_edges['N3'].jump_ratio, 1.0, rtol=0.01)


def test_emission_lines():
    cu_lines = xray_lines('Cu')
    for lname in ('Ka3', 'Ka2', 'Ka1', 'Kb3', 'Kb1', 'Kb5',
                  'Lb4', 'Lb3', 'Ln', 'Lb1', 'Ll', 'La2', 'La1'):
        assert(lname in cu_lines)

    assert cu_lines['Ka1'].energy > 8045.0
    assert cu_lines['Ka1'].energy < 8047.0
    assert cu_lines['Ka1'].initial_level == 'K'
    assert cu_lines['Ka1'].final_level == 'L3'

def test_f0():
    q = np.linspace(0, 5, 21)
    known_f = np.array([21.998, 14.569, 9.142, 6.958, 5.743, 4.639, 3.664,
                        2.880, 2.296, 1.890, 1.621, 1.445, 1.326, 1.240,
                        1.170, 1.108, 1.050, 0.992, 0.936, 0.880, 0.826])

    assert_allclose(known_f, f0('Ti', q), rtol=0.005)
    assert_allclose(known_f, f0(22, q), rtol=0.005)

    with pytest.raises(ValueError):
        f = f0('Ti5+', q)


def test_f0_ions():
    ions = f0_ions()
    assert len(ions) > 200
    for ion in ('Li', 'Cl', 'Fe2+', 'Sr2+', 'Cd2+', 'Nd', 'Lu3+', 'Pb', 'Pu'):
        assert ion in ions

    ions = f0_ions('Eu')
    assert len(ions) == 3

    ions = f0_ions('Ti')
    assert len(ions) == 4


def test_mu_elam():
    en = np.linspace(13000, 17000, 51)

    mu_total = np.array([67.46, 160.62, 158.03, 155.50, 153.03, 150.61, 148.24,
                         145.92, 143.66, 141.44, 139.27, 137.14, 135.06, 133.02,
                         131.03, 129.07, 127.16, 125.28, 123.45, 121.65, 119.88,
                         118.15, 116.46, 114.80, 113.17, 111.57, 110.03, 108.52,
                         147.60, 145.79, 144.01, 142.26, 140.54, 138.86, 137.21,
                         135.58, 154.36, 152.41, 150.50, 148.63, 146.79, 144.97,
                         143.19, 141.45, 139.73, 138.04, 136.37, 134.74, 133.13,
                         131.55, 130.00])

    mu_photo = np.array([63.54, 156.73, 154.16, 151.66, 149.21, 146.81, 144.46,
                         142.17, 139.93, 137.73, 135.58, 133.48, 131.42, 129.40,
                         127.43, 125.50, 123.61, 121.75, 119.94, 118.16, 116.41,
                         114.71, 113.03, 111.39, 109.78, 108.21, 106.69, 105.19,
                         144.30, 142.50, 140.74, 139.01, 137.31, 135.65, 134.01,
                         132.41, 151.20, 149.27, 147.38, 145.52, 143.70, 141.90,
                         140.14, 138.41, 136.71, 135.03, 133.39, 131.77, 130.18,
                         128.62, 127.08])

    mu_coh = np.array([3.86, 3.84, 3.82, 3.79, 3.77, 3.74, 3.72, 3.70, 3.67,
                       3.65, 3.63, 3.60, 3.58, 3.56, 3.54, 3.52, 3.49, 3.47,
                       3.45, 3.43, 3.41, 3.39, 3.37, 3.35, 3.33, 3.31, 3.29,
                       3.27, 3.25, 3.23, 3.21, 3.19, 3.17, 3.15, 3.13, 3.12,
                       3.10, 3.08, 3.06, 3.04, 3.03, 3.01, 2.99, 2.97, 2.96,
                       2.94, 2.92, 2.91, 2.89, 2.87, 2.86])

    mu_incoh = np.array([0.05432, 0.05453, 0.05474, 0.05495, 0.05515, 0.05536,
                         0.05556, 0.05576, 0.05596, 0.05616, 0.05636, 0.05656,
                         0.05675, 0.05695, 0.05714, 0.05734, 0.05753, 0.05772,
                         0.05791, 0.05810, 0.05828, 0.05847, 0.05865, 0.05884,
                         0.05902, 0.05920, 0.05939, 0.05957, 0.05974, 0.05992,
                         0.06010, 0.06028, 0.06045, 0.06063, 0.06080, 0.06097,
                         0.06114, 0.06132, 0.06149, 0.06166, 0.06182, 0.06199,
                         0.06216, 0.06232, 0.06249, 0.06265, 0.06282, 0.06298,
                         0.06314, 0.06330, 0.06346])

    assert_allclose(mu_total, mu_elam('Pb', en), rtol=0.01)
    assert_allclose(mu_photo, mu_elam('Pb', en, kind='photo'), rtol=0.01)
    assert_allclose(mu_incoh, mu_elam('Pb', en, kind='incoh'), rtol=0.01)
    assert_allclose(mu_coh,   mu_elam('Pb', en, kind='coh'), rtol=0.01)

    with pytest.raises(ValueError):
        mu_elam('Pb', en, kind='all')

def test_elam_coh_incoh():
    en = np.linspace(13000, 17000, 51)

    incoh = np.array([0.08085165, 0.08112906, 0.08140468, 0.08167853,
                      0.08195061, 0.08222095, 0.08248954, 0.0827564 ,
                      0.08302154, 0.08328497, 0.0835467 , 0.08380673,
                      0.08406508, 0.08432176, 0.08457678, 0.08483014,
                      0.08508186, 0.08533195, 0.08558041, 0.08582725,
                      0.08607249, 0.08631613, 0.08655818, 0.08679866,
                      0.08703756, 0.08727491, 0.0875107 , 0.08774495,
                      0.08797767, 0.08820887, 0.08843856, 0.08866675,
                      0.08889345, 0.08911867, 0.08934242, 0.08956471,
                      0.08978554, 0.09000494, 0.09022291, 0.09043946,
                      0.09065459, 0.09086832, 0.09108066, 0.09129161,
                      0.09150119, 0.0917094 , 0.09191626, 0.09212176,
                      0.09232593, 0.09252877, 0.09273028])

    coh = np.array([1.34896099, 1.33854813, 1.32825911, 1.31809228,
                    1.308046 , 1.29811866, 1.28830866, 1.27861442,
                    1.26903438, 1.259567 , 1.25021075, 1.24096413,
                    1.23182566, 1.22279385, 1.21386727, 1.20504448,
                    1.19632407, 1.18770464, 1.17918482, 1.17076326,
                    1.1624386 , 1.15420954, 1.14607477, 1.138033 ,
                    1.13008296, 1.12222341, 1.11445296, 1.10677039,
                    1.09917435, 1.09166353, 1.08423663, 1.07689238,
                    1.06962952, 1.06244685, 1.05534314, 1.04831724,
                    1.04136798, 1.03449422, 1.02769486, 1.02096879,
                    1.01431496, 1.0077323 , 1.00121977, 0.99477638,
                    0.98840111, 0.98209299, 0.97585106, 0.96967437,
                    0.96356201, 0.95751305, 0.9515266 ])

    assert_allclose(coherent_cross_section_elam('Br', en), coh, rtol=0.01)
    assert_allclose(incoherent_cross_section_elam('Br', en), incoh, rtol=0.01)


def test_mu_chantler():
    en = np.linspace(13000, 17000, 51)

    mu_total = np.array([64.44, 141.67, 142.46, 143.20, 143.97, 144.66, 144.12,
                         142.86, 140.56, 138.30, 136.10, 133.99, 131.92, 129.85,
                         127.82, 125.84, 123.90, 122.01, 120.21, 118.44, 116.67,
                         114.91, 113.16, 111.48, 109.87, 108.29, 106.74, 105.16,
                         144.38, 142.63, 141.02, 139.34, 137.71, 136.15, 134.59,
                         133.04, 149.40, 147.61, 145.77, 143.97, 142.19, 140.45,
                         138.75, 137.07, 135.43, 133.82, 132.24, 130.69, 129.17,
                         127.64, 126.13])

    mu_photo = np.array([63.33, 153.06, 151.92, 149.80, 147.54, 145.26, 142.98,
                         140.74, 138.56, 136.39, 134.26, 132.17, 130.13, 128.12,
                         126.15, 124.23, 122.34, 120.50, 118.69, 116.92, 115.18,
                         113.49, 111.83, 110.22, 108.64, 107.16, 105.74, 104.99,
                         142.95, 141.64, 139.85, 137.97, 136.13, 134.35, 132.63,
                         131.28, 145.78, 146.64, 145.03, 143.28, 141.54, 139.80,
                         138.09, 136.41, 134.75, 133.11, 131.49, 129.90, 128.33,
                         126.78, 125.25])


    mu_incoh = np.array([3.92, 3.89, 3.87, 3.84, 3.82, 3.79, 3.77, 3.75, 3.72,
                         3.70, 3.68, 3.66, 3.63, 3.61, 3.59, 3.57, 3.55, 3.52,
                         3.50, 3.48, 3.46, 3.44, 3.42, 3.40, 3.38, 3.36, 3.34,
                         3.32, 3.30, 3.28, 3.26, 3.25, 3.23, 3.21, 3.19, 3.17,
                         3.15, 3.14, 3.12, 3.10, 3.08, 3.07, 3.05, 3.03, 3.02,
                         3.00, 2.98, 2.97, 2.95, 2.94, 2.92])


    assert_allclose(mu_total, mu_chantler('Pb', en), rtol=0.01)
    assert_allclose(mu_photo, mu_chantler('Pb', en, photo=True), rtol=0.01)
    assert_allclose(mu_incoh, mu_chantler('Pb', en, incoh=True), rtol=0.01)
    assert_allclose(mu_incoh, chantler_data('Pb', en, 'mu_incoh'), rtol=0.01)
    assert_allclose(mu_photo, chantler_data('Pb', en, 'mu_photo'), rtol=0.01)
    assert_allclose(mu_total, chantler_data('Pb', en, 'mu_total'), rtol=0.01)
    assert_allclose(mu_total, chantler_data('Pb', en, 'mu'), rtol=0.01)

    assert_allclose(64.44, chantler_data('Pb', 13000, 'mu'), rtol=0.01)


def test_f1f2_chantler():
    en = np.linspace(10000, 15000, 51)

    f1 = np.array([-5.97, -6.08, -6.20, -6.33, -6.46, -6.60, -6.75, -6.91,
                   -7.09, -7.28, -7.49, -7.72, -7.99, -8.28, -8.64, -9.06,
                   -9.60, -10.33, -11.54, -15.14, -12.27, -10.64, -9.78,
                   -9.18, -8.76, -8.43, -8.18, -7.98, -7.83, -7.73, -7.66,
                   -7.64, -7.66, -7.73, -7.87, -8.13, -8.58, -9.91, -9.18,
                   -8.19, -7.73, -7.46, -7.36, -7.61, -7.43, -6.61, -6.13,
                   -5.77, -5.46, -5.20, -4.96 ])

    f2 = np.array([5.12, 5.04, 4.96, 4.87, 4.80, 4.72, 4.64, 4.57, 4.50,
                   4.43, 4.37, 4.30, 4.24, 4.18, 4.12, 4.06, 4.01, 3.97,
                   3.93, 4.15, 9.94, 9.83, 9.70, 9.57, 9.43, 9.30, 9.17,
                   9.05, 8.92, 8.80, 8.69, 8.57, 8.46, 8.35, 8.25, 8.14,
                   8.05, 8.02, 10.94, 10.83, 10.71, 10.59, 10.47, 10.39,
                   11.75, 11.67, 11.56, 11.44, 11.33, 11.21, 11.10])


    assert_allclose(f1, f1_chantler('Au', en), rtol=0.01)
    assert_allclose(f2, f2_chantler('Au', en), rtol=0.01)
    assert_allclose(f1, chantler_data('Au', en, 'f1'), rtol=0.01)
    assert_allclose(f2, chantler_data('Au', en, 'f2'), rtol=0.01)

def test_chantler_energies():

    en = np.array([6876.64, 6945.41, 7014.86, 7085.01, 7155.86, 7227.42,
                   7299.69, 7372.69, 7446.42, 7520.88, 7596.09, 7672.05,
                   7748.77, 7826.26, 7904.52, 7983.56, 8063.40, 8144.03,
                   8225.47, 8307.73, 8390.81, 8474.71, 8559.46, 8645.06,
                   8731.51, 8818.82, 8907.01, 8996.08, 9086.04, 9176.90,
                   9268.67, 9361.36, 9454.97, 9549.52, 9609.00, 9633.80,
                   9645.01, 9646.20, 9652.40, 9655.50, 9657.10, 9660.10,
                   9661.70, 9664.80, 9671.00, 9683.40, 9708.20, 9741.46,
                   9838.88, 9937.27, 10036.64, 10137.01, 10238.38,
                   10340.76, 10444.17, 10548.61, 10654.09, 10760.64,
                   10868.24, 10976.92, 11086.69, 11197.56, 11309.54,
                   11422.63, 11536.86, 11652.23, 11768.75, 11886.44,
                   12005.30, 12125.35])
    assert_allclose(en, chantler_energies('Zn', emin=7000, emax=12000), rtol=0.01)

    eall_ge = chantler_energies('Ge')
    assert len(eall_ge) > 1425
    assert eall_ge[0] < 1.2
    assert eall_ge[0] > 0.9
    assert eall_ge[-1] < 1e6
    assert eall_ge[-1] > 9.5e5

def test_guess_edge():
    vals = ((1607.22, 'Al', 'K'), (2260.35, 'P', 'K'), (2411.97, 'S', 'K'),
            (2559.74, 'S', 'K'), (2867.76, 'Mo', 'L1'), (3696.58, 'K', 'K'),
            (3971.10, 'Ca', 'K'), (4421.73, 'Sc', 'K'), (4765.58, 'Xe', 'L3'),
            (6278.32, 'La', 'L1'), (6375.02, 'Mn', 'K'), (6447.24, 'Pr', 'L2'),
            (6745.03, 'Nd', 'L2'), (6831.54, 'Pr', 'L1'), (6897.72, 'Fe', 'K'),
            (7074.41, 'Fe', 'K'), (7297.04, 'Sm', 'L2'), (7981.74, 'Gd', 'L2'),
            (8111.00, 'Ho', 'L3'), (8289.68, 'Ni', 'K'), (8787.12, 'Cu', 'K'),
            (8893.41, 'Cu', 'K'), (9032.98, 'Cu', 'K'), (9690.75, 'Zn', 'K'),
            (9694.53, 'Zn', 'K'), (10354.47, 'Ga', 'K'), (10442.38, 'Ga', 'K'),
            (10455.03, 'Ga', 'K'), (11150.30, 'Ge', 'K'), (11963.31, 'Re',
            'L2'), (12774.25, 'Se', 'K'), (13268.59, 'Pt', 'L2'), (13971.48,
            'Po', 'L3'), (14009.96, 'Kr', 'K'), (14192.88, 'Hg', 'L2'),
            (14248.22, 'At', 'L3'), (14601.50, 'Rn', 'L3'), (14754.45, 'Tl',
            'L2'), (15058.15, 'Fr', 'L3'), (15529.31, 'Rb', 'K'), (15846.94,
            'Ac', 'L3'), (16800.91, 'At', 'L2'), (16923.31, 'Y', 'K'),
            (17235.13, 'Y', 'K'), (17452.53, 'Y', 'K'), (17455.89, 'Y', 'K'),
            (18327.81, 'Zr', 'K'), (18478.71, 'Ra', 'L2'), (18895.14, 'Nb',
            'K'), (18917.70, 'Nb', 'K'), (19015.14, 'Nb', 'K'), (20259.03, 'Mo',
            'K'), (20325.21, 'Pa', 'L2'), (20329.70, 'Pa', 'L2'), (20489.15,
            'Th', 'L1'), (20520.48, 'Th', 'L1'), (20905.52, 'Tc', 'K'),
            (20997.74, 'Tc', 'K'), (21606.63, 'Np', 'L2'), (21894.47, 'Ru',
            'K'), (22424.97, 'Np', 'L1'), (23101.67, 'Pu', 'L1'), (24929.69,
            'Pd', 'K'), (25507.23, 'Ag', 'K'), (26291.15, 'Cd', 'K'), (26523.45,
            'Cd', 'K'), (26730.45, 'Cd', 'K'), (27496.51, 'In', 'K'), (27534.86,
            'In', 'K'), (28524.18, 'In', 'K'), (29220.68, 'Sn', 'K'), (29563.18,
            'Sn', 'K'), (30148.46, 'Sb', 'K'), (30178.67, 'Sb', 'K'), (30692.73,
            'Sb', 'K'), (31006.32, 'Sb', 'K'), (31375.27, 'Te', 'K'), (31511.43,
            'Te', 'K'), (31539.46, 'Te', 'K'), (31549.18, 'Te', 'K'), (31781.82,
            'Te', 'K'), (32113.33, 'Te', 'K'), (32529.16, 'I', 'K'), (32769.91,
            'I', 'K'), (32945.96, 'I', 'K'), (33162.58, 'I', 'K'), (33861.76,
            'I', 'K'), (34282.18, 'Xe', 'K'), (34616.82, 'Xe', 'K'), (35048.42,
            'Xe', 'K'), (35451.22, 'Cs', 'K'), (35732.84, 'Cs', 'K'), (36226.88,
            'Cs', 'K'), (37011.63, 'Ba', 'K'), (37119.11, 'Ba', 'K'), (37687.55,
            'Ba', 'K'), (38255.21, 'La', 'K'), (38534.03, 'La', 'K'), (39383.09,
            'La', 'K'), (39597.61, 'La', 'K'), (39985.10, 'Ce', 'K'), (40189.85,
            'Ce', 'K'), (40299.94, 'Ce', 'K'), (40803.37, 'Ce', 'K'), (41062.46,
            'Ce', 'K'), (41563.00, 'Pr', 'K'), (41604.41, 'Pr', 'K'), (41914.19,
            'Pr', 'K'), (41947.64, 'Pr', 'K'), (42090.33, 'Pr', 'K'), (42995.34,
            'Nd', 'K'), (43296.60, 'Nd', 'K'), (44306.16, 'Nd', 'K'), (44470.03,
            'Pm', 'K'), (45936.49, 'Pm', 'K'), (45992.17, 'Pm', 'K'), (45998.94,
            'Pm', 'K'), (47495.02, 'Sm', 'K'), (47674.10, 'Sm', 'K'), (47942.94,
            'Eu', 'K'), (48996.75, 'Eu', 'K'), (49840.90, 'Gd', 'K'), (50129.53,
            'Gd', 'K'), (50525.35, 'Gd', 'K'), (51211.59, 'Tb', 'K'), (51574.05,
            'Tb', 'K'), (51872.86, 'Tb', 'K'), (52198.93, 'Tb', 'K'), (52448.10,
            'Tb', 'K'), (53243.79, 'Dy', 'K'), (53409.52, 'Dy', 'K'), (53945.61,
            'Dy', 'K'), (53970.83, 'Dy', 'K'), (55202.28, 'Ho', 'K'), (55573.56,
            'Ho', 'K'), (56150.05, 'Ho', 'K'), (56361.18, 'Ho', 'K'), (56372.13,
            'Ho', 'K'), (58278.64, 'Er', 'K'), (58712.03, 'Tm', 'K'), (58804.02,
            'Tm', 'K'), (59170.93, 'Tm', 'K'), (59295.42, 'Tm', 'K'), (59777.61,
            'Tm', 'K'), (59795.79, 'Tm', 'K'), (60196.31, 'Tm', 'K'), (60733.44,
            'Yb', 'K'), (60829.65, 'Yb', 'K'), (60877.42, 'Yb', 'K'), (60958.45,
            'Yb', 'K'), (64355.51, 'Hf', 'K'), (64528.43, 'Hf', 'K'), (64807.76,
            'Hf', 'K'), (67037.59, 'Ta', 'K'), (67684.42, 'Ta', 'K'), (68153.83,
            'Ta', 'K'), (68190.34, 'Ta', 'K'), (68223.59, 'Ta', 'K'), (68281.45,
            'Ta', 'K'), (68454.23, 'Ta', 'K'), (68645.09, 'W', 'K'), (69098.00,
            'W', 'K'), (69375.45, 'W', 'K'), (69629.24, 'W', 'K'), (69917.35,
            'W', 'K'), (70279.29, 'W', 'K'), (71077.63, 'Re', 'K'), (71181.95,
            'Re', 'K'), (71218.00, 'Re', 'K'), (71726.69, 'Re', 'K'), (72635.91,
            'Re', 'K'), (73524.97, 'Os', 'K'), (73609.73, 'Os', 'K'), (73924.75,
            'Os', 'K'), (74544.48, 'Os', 'K'), (75531.12, 'Ir', 'K'), (76370.20,
            'Ir', 'K'), (76460.23, 'Ir', 'K'), (77749.62, 'Pt', 'K'), (78466.63,
            'Pt', 'K'), (79382.39, 'Pt', 'K'), (79752.40, 'Au', 'K'), (80068.68,
            'Au', 'K'), (81540.62, 'Au', 'K'), (82353.66, 'Hg', 'K'), (82571.70,
            'Hg', 'K'), (82672.30, 'Hg', 'K'), (82932.53, 'Hg', 'K'), (83155.18,
            'Hg', 'K'), (83452.92, 'Hg', 'K'), (83669.34, 'Hg', 'K'), (83823.59,
            'Hg', 'K'), (84319.11, 'Tl', 'K'), (84434.41, 'Tl', 'K'), (84538.14,
            'Tl', 'K'), (85183.11, 'Tl', 'K'), (85213.28, 'Tl', 'K'), (85276.74,
            'Tl', 'K'), (85352.80, 'Tl', 'K'), (85377.82, 'Tl', 'K'))

    for en, elem, edge in vals:
        _elem, _edge = guess_edge(en)
        assert elem == _elem
        assert edge == _edge

    _elem, _edge = guess_edge(1608, edges=['K', 'L1', 'L2', 'L3', 'M5', 'M3'])
    assert _elem == 'Tb'
    assert _edge == 'M3'

def test_fluor_yeild():
    fy1  = (0.351, 6400.75, 0.8746)
    assert_allclose(fy1, fluor_yield('Fe', 'K', 'Ka', 8000), rtol=0.001)

    fy2 = 0.0, 6400.752, 0.8746
    assert_allclose(fy2, fluor_yield('Fe', 'K', 'Ka', 6000), rtol=0.001)

    fy3 = 0.052, 2982.13, 0.8619
    assert_allclose(fy3, fluor_yield('Ag', 'L3', 'La', 6000), rtol=0.001)


def test_core_width():
    kwid_known = np.array([0.0201, 0.0269, 0.036, 0.0483, 0.0647, 0.0868,
                           0.1163, 0.1559, 0.2089, 0.24, 0.3, 0.36, 0.42,
                           0.48, 0.53, 0.59, 0.64, 0.68, 0.74, 0.81, 0.86,
                           0.94, 1.01, 1.08, 1.16, 1.25, 1.33, 1.44, 1.55,
                           1.67, 1.82, 1.96, 2.14, 2.33, 2.52, 2.75, 2.99,
                           3.25, 3.52, 3.84, 4.14, 4.52, 4.91, 5.33, 5.77,
                           6.24, 6.75, 7.28, 7.91, 8.49, 9.16, 9.89, 10.6,
                           11.4, 12.3, 13.2, 14.1, 15.1, 16.2, 17.3, 18.5,
                           19.7, 21.0, 22.3, 23.8, 25.2, 26.8, 28.4, 30.1,
                           31.9, 33.7, 35.7, 37.7, 39.9, 42.1, 44.4, 46.8,
                           49.3, 52.0, 54.6, 57.4, 60.4, 63.4, 66.6, 69.8,
                           73.3, 76.8, 80.4, 84.1, 88.0, 91.9, 96.1, 100.0,
                           105.0, 109.0, 114.0, 119.0, 124.0])

    kwid = np.array([core_width(i, 'K') for i in range(1, 99)])

    assert_allclose(kwid, kwid_known, rtol=0.01)

    l3wid_known = np.array([0.17, 0.19, 0.22, 0.24, 0.27, 0.32, 0.36, 0.43,
                            0.48, 0.56, 0.65, 0.76, 0.82, 0.94, 1.0, 1.08,
                            1.17, 1.27, 1.39, 1.5, 1.57, 1.66, 1.78, 1.91,
                            2.0, 2.13, 2.25, 2.4, 2.5, 2.65, 2.75, 2.87,
                            2.95, 3.08, 3.13, 3.25, 3.32, 3.41, 3.48, 3.6,
                            3.65, 3.75, 3.86, 3.91, 4.01, 4.12, 4.17, 4.26,
                            4.35, 4.48, 4.6, 4.68, 4.8, 4.88, 4.98, 5.04,
                            5.16, 5.25, 5.31, 5.41, 5.5, 5.65, 5.81, 5.98,
                            6.13, 6.29, 6.41, 6.65, 6.82, 6.98, 7.13, 7.33,
                            7.43, 7.59, 7.82, 8.04, 8.26, 8.55, 8.75])
    l3wid = np.array([core_width(i, 'L3') for i in range(20, 99)])
    assert_allclose(l3wid, l3wid_known, rtol=0.01)


def test_xray_line():
    cuk = xray_line('Cu', 'K')
    assert_allclose(cuk.energy, 8039.626, rtol=0.001)
    assert_allclose(cuk.intensity, 0.8716833, rtol=0.001)
    assert cuk.final_level == 'L'

    cuka = xray_line('Cu', 'Ka1')
    assert_allclose(cuka.energy, 8046.3, rtol=0.001)
    assert_allclose(cuka.intensity, 0.5771, rtol=0.001)
    assert cuka.final_level == 'L3'

    ti_klines = xray_lines('Ti', 'K')
    for line in ('Ka1', 'Ka2', 'Ka3', 'Kb1', 'Kb3', 'Kb5'):
        assert ti_klines[line].initial_level == 'K'

    assert_allclose(ti_klines['Ka1'].energy, 4512.2, rtol=0.001)
    assert_allclose(ti_klines['Ka2'].energy, 4505.8, rtol=0.001)
    assert_allclose(ti_klines['Ka3'].energy, 4405.1, rtol=0.001)
    assert_allclose(ti_klines['Kb1'].energy, 4933.4, rtol=0.001)
    assert_allclose(ti_klines['Kb3'].energy, 4933.4, rtol=0.001)
    assert_allclose(ti_klines['Kb5'].energy, 4964.0, rtol=0.001)

    assert_allclose(ti_klines['Ka1'].intensity, 0.58455, rtol=0.001)
    assert_allclose(ti_klines['Ka2'].intensity, 0.29369, rtol=0.001)
    assert_allclose(ti_klines['Ka3'].intensity, 0.000235, rtol=0.01)
    assert_allclose(ti_klines['Kb1'].intensity, 0.07965, rtol=0.001)
    assert_allclose(ti_klines['Kb3'].intensity, 0.04126, rtol=0.001)
    assert_allclose(ti_klines['Kb5'].intensity, 0.000607, rtol=0.01)
    assert_allclose(ti_klines['Ka1'].intensity, 0.58455, rtol=0.001)

    assert ti_klines['Ka1'].final_level == 'L3'
    assert ti_klines['Ka2'].final_level == 'L2'
    assert ti_klines['Ka3'].final_level == 'L1'
    assert ti_klines['Kb1'].final_level == 'M3'
    assert ti_klines['Kb3'].final_level == 'M2'
    assert ti_klines['Kb5'].final_level == 'M4,5'


def test_xray_lines_levels():
    assert len(xray_lines('Hg', excitation_energy=2800)) == 2
    assert len(xray_lines('Hg', excitation_energy=12000)) == 3
    assert len(xray_lines('Hg', excitation_energy=12500)) == 9
    assert len(xray_lines('Hg', excitation_energy=14300)) == 13
    assert len(xray_lines('Hg', excitation_energy=16000)) == 17


def test_ck_probability():
    assert_allclose(ck_probability('W', 'L1', 'L3'), 0.3, rtol=0.01)


def test_delta_beta():

    delta = np.array([2.31879798e-05, 2.30263614e-05, 2.28655690e-05,
                      2.27055461e-05, 2.25462258e-05, 2.23875379e-05,
                      2.22294125e-05, 2.20717621e-05, 2.19144854e-05,
                      2.17574831e-05, 2.16006447e-05, 2.14438386e-05,
                      2.12869338e-05, 2.11297790e-05, 2.09721149e-05,
                      2.08136556e-05, 2.06541214e-05, 2.04932245e-05,
                      2.03306727e-05, 2.01661788e-05, 1.99990853e-05,
                      1.98278335e-05, 1.96507644e-05, 1.94662663e-05,
                      1.92728472e-05, 1.90690943e-05, 1.88535304e-05,
                      1.86137126e-05, 1.83166396e-05, 1.79263695e-05,
                      1.72644728e-05, 1.68846677e-05, 1.75514931e-05,
                      1.77905451e-05, 1.79131927e-05, 1.79732450e-05,
                      1.79928595e-05, 1.79928689e-05, 1.79824646e-05,
                      1.79627078e-05, 1.79344673e-05, 1.78986834e-05,
                      1.78566159e-05, 1.78095782e-05, 1.77588480e-05,
                      1.77052893e-05, 1.76492014e-05, 1.75908356e-05,
                      1.75304432e-05, 1.74683253e-05, 1.74048109e-05])

    beta = np.array([4.15330456e-07, 4.10533886e-07, 4.05807206e-07,
                     4.01142710e-07, 3.96544748e-07, 3.92013242e-07,
                     3.87546123e-07, 3.83142560e-07, 3.78802101e-07,
                     3.74526554e-07, 3.70319235e-07, 3.66171556e-07,
                     3.62082498e-07, 3.58040827e-07, 3.54055453e-07,
                     3.50126039e-07, 3.46263146e-07, 3.42462535e-07,
                     3.38714592e-07, 3.35014122e-07, 3.31343582e-07,
                     3.27723749e-07, 3.24153777e-07, 3.20645679e-07,
                     3.17190186e-07, 3.13781696e-07, 3.10416648e-07,
                     3.07089178e-07, 3.03806706e-07, 3.00558985e-07,
                     2.97367605e-07, 2.10914637e-06, 2.08861169e-06,
                     2.06826314e-06, 2.04838399e-06, 2.02875052e-06,
                     2.00935901e-06, 1.99017262e-06, 1.97120233e-06,
                     1.95246442e-06, 1.93395484e-06, 1.91563532e-06,
                     1.89753871e-06, 1.87966170e-06, 1.86198608e-06,
                     1.84449823e-06, 1.82722124e-06, 1.81015203e-06,
                     1.79327486e-06, 1.77659378e-06, 1.76011187e-06])

    beta_photo = np.array([3.90526978e-07, 3.86063935e-07, 3.81665372e-07,
                        3.77336646e-07, 3.73071089e-07, 3.68866519e-07,
                        3.64729098e-07, 3.60655470e-07, 3.56639426e-07,
                        3.52684594e-07, 3.48796990e-07, 3.44963677e-07,
                        3.41183740e-07, 3.37480438e-07, 3.33829590e-07,
                        3.30228863e-07, 3.26702653e-07, 3.23242941e-07,
                        3.19829864e-07, 3.16477854e-07, 3.13244987e-07,
                        3.10054443e-07, 3.06905547e-07, 3.03998036e-07,
                        3.01199959e-07, 2.98435746e-07, 2.96106878e-07,
                        2.94958918e-07, 2.93820876e-07, 2.93903973e-07,
                        3.11478882e-07, 2.10154368e-06, 2.11105335e-06,
                        2.09391918e-06, 2.07224074e-06, 2.05084613e-06,
                        2.02973085e-06, 2.00827838e-06, 1.98675441e-06,
                        1.96551940e-06, 1.94456638e-06, 1.92374766e-06,
                        1.90320773e-06, 1.88294210e-06, 1.86292819e-06,
                        1.84314908e-06, 1.82363251e-06, 1.80437431e-06,
                        1.78600492e-06, 1.76816730e-06, 1.75055477e-06])

    atten = np.array([0.00365468, 0.00368604, 0.00371757, 0.00374933,
                      0.00378128, 0.0038134 , 0.0038457 , 0.00387818,
                      0.00391084, 0.00394364, 0.00397654, 0.00400961,
                      0.00404286, 0.0040764 , 0.00411013, 0.00414403,
                      0.00417797, 0.00421199, 0.00424618, 0.0042806 ,
                      0.00431548, 0.00435053, 0.00438577, 0.00442101,
                      0.00445637, 0.00449191, 0.00452767, 0.00456372,
                      0.00459996, 0.00463653, 0.00467309, 0.00065701,
                      0.00066161, 0.00066625, 0.00067084, 0.00067545,
                      0.00068008, 0.00068474, 0.00068943, 0.00069413,
                      0.00069886, 0.00070361, 0.00070839, 0.00071318,
                      0.000718, 0.00072285, 0.00072772, 0.0007326,
                      0.00073751, 0.00074245, 0.0007474 ])

    en = np.linspace(6500, 7500, 51)
    d, b, a = xray_delta_beta('Fe2O3', 5.25, en)

    assert_allclose(delta, d, rtol=0.005)
    assert_allclose(beta_photo, b, rtol=0.005)
    assert_allclose(atten, a, rtol=0.005)

def test_mirror_reflectivity():
    rh1 = np.array([0.97199571, 0.97748356, 0.95360848, 0.92357963, 0.93588329,
                    0.94249572, 0.94771043, 0.95137756, 0.95416567, 0.95693941,
                    0.95906606, 0.9606963 , 0.96193867, 0.96298571, 0.9637671 ,
                    0.96434822, 0.96458685, 0.96443861, 0.963873  , 0.96273628,
                    0.9607325 , 0.95705164, 0.94578432, 0.69383757, 0.65937538,
                    0.57222587, 0.40829232, 0.26919575, 0.18904094, 0.14024917])
    r1 = mirror_reflectivity('Rh', 0.0025, np.arange(1000, 31000, 1000))
    assert_allclose(rh1, r1, rtol=0.005)    

    assert_allclose(mirror_reflectivity('Pt', 0.001, 80000), 0.74, rtol=0.005)

    
def test_ionchamber_fluxes():
        ic1 = ionchamber_fluxes(gas='helium', volts=1.25, length=200.0,
                              energy=10000.0, sensitivity=1.e-9)

        assert_allclose(ic1.photo, 16110895.3, rtol=0.01)
        assert_allclose(ic1.transmitted, 15316549138.8, rtol=0.01)

        ic2 = ionchamber_fluxes(gas='nitrogen', volts=1.25, length=200.0,
                                energy=10000.0, sensitivity=1.e-9)

        assert_allclose(ic2.photo, 13575282.2, rtol=0.01)
        assert_allclose(ic2.incident, 23102328.0, rtol=0.01)
        
        ic3 = ionchamber_fluxes(gas={'nitrogen':0.5, 'helium': 0.5}, volts=1.25,
                                length=200.0, energy=10000.0, sensitivity=1.e-9)

        assert_allclose(ic3.photo, 14843088.8, rtol=0.01)
        assert_allclose(ic3.incident, 7737855176.4, rtol=0.01)
        assert_allclose(ic3.transmitted, 7662654298.8, rtol=0.01)

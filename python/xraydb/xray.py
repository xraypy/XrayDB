import sys
from collections import namedtuple
import numpy as np

from .utils import (R_ELECTRON_CM, AVOGADRO, PLANCK_HC,
                    QCHARGE, SI_PREFIXES, index_nearest)


from .xraydb import XrayDB,  XrayLine
from .chemparser import chemparse

fluxes = namedtuple('IonChamberFluxes', ('photo',
                                         'incident',
                                         'transmitted'))


_edge_energies = {'k': np.array([-1.0, 13.6, 24.6, 54.7, 111.5, 188.0,
                                 284.2, 409.9, 543.1, 696.7, 870.2, 1070.8,
                                 1303.0, 1559.0, 1839.0, 2145.5, 2472.0,
                                 2822.0, 3205.9, 3608.4, 4038.5, 4492.0,
                                 4966.0, 5465.0, 5989.0, 6539.0, 7112.0,
                                 7709.0, 8333.0, 8979.0, 9659.0, 10367.0,
                                 11103.0, 11867.0, 12658.0, 13474.0,
                                 14326.0, 15200.0, 16105.0, 17038.0,
                                 17998.0, 18986.0, 20000.0, 21044.0,
                                 22117.0, 23220.0, 24350.0, 25514.0,
                                 26711.0, 27940.0, 29200.0, 30491.0,
                                 31814.0, 33169.0, 34561.0, 35985.0,
                                 37441.0, 38925.0, 40443.0, 41991.0,
                                 43569.0, 45184.0, 46834.0, 48519.0,
                                 50239.0, 51996.0, 53789.0, 55618.0,
                                 57486.0, 59390.0, 61332.0, 63314.0,
                                 65351.0, 67416.0, 69525.0, 71676.0,
                                 73871.0, 76111.0, 78395.0, 80725.0,
                                 83102.0, 85530.0, 88005.0, 90526.0,
                                 93105.0, 95730.0, 98404.0, 101137.0,
                                 103922.0, 106755.0, 109651.0, 112601.0,
                                 115606.0, 118669.0, 121791.0, 124982.0,
                                 128241.0, 131556.0]),

                  'l3': np.array([-1.0, -1.0, -1.0, -1.0, 3.0, 4.7, 7.2,
                                  17.5, 18.2, 19.9, 21.6, 30.5, 49.2, 72.5,
                                  99.2, 135.0, 162.5, 200.0, 248.4, 294.6,
                                  346.2, 398.7, 453.8, 512.1, 574.1, 638.7,
                                  706.8, 778.1, 852.7, 932.7, 1021.8,
                                  1116.4, 1217.0, 1323.6, 1433.9, 1550.0,
                                  1678.4, 1804.0, 1940.0, 2080.0, 2223.0,
                                  2371.0, 2520.0, 2677.0, 2838.0, 3004.0,
                                  3173.0, 3351.0, 3538.0, 3730.0, 3929.0,
                                  4132.0, 4341.0, 4557.0, 4786.0, 5012.0,
                                  5247.0, 5483.0, 5723.0, 5964.0, 6208.0,
                                  6459.0, 6716.0, 6977.0, 7243.0, 7514.0,
                                  7790.0, 8071.0, 8358.0, 8648.0, 8944.0,
                                  9244.0, 9561.0, 9881.0, 10207.0, 10535.0,
                                  10871.0, 11215.0, 11564.0, 11919.0,
                                  12284.0, 12658.0, 13035.0, 13419.0,
                                  13814.0, 14214.0, 14619.0, 15031.0,
                                  15444.0, 15871.0, 16300.0, 16733.0,
                                  17166.0, 17610.0, 18057.0, 18510.0,
                                  18970.0, 19435.0]),

                  'l2': np.array([-1.0, -1.0, -1.0, -1.0, 3.0, 4.7, 7.2,
                                  17.5, 18.2, 19.9, 21.7, 30.4, 49.6, 72.9,
                                  99.8, 136.0, 163.6, 202.0, 250.6, 297.3,
                                  349.7, 403.6, 460.2, 519.8, 583.8, 649.9,
                                  719.9, 793.2, 870.0, 952.3, 1044.9,
                                  1143.2, 1248.1, 1359.1, 1474.3, 1596.0,
                                  1730.9, 1864.0, 2007.0, 2156.0, 2307.0,
                                  2465.0, 2625.0, 2793.0, 2967.0, 3146.0,
                                  3330.0, 3524.0, 3727.0, 3938.0, 4156.0,
                                  4380.0, 4612.0, 4852.0, 5107.0, 5359.0,
                                  5624.0, 5891.0, 6164.0, 6440.0, 6722.0,
                                  7013.0, 7312.0, 7617.0, 7930.0, 8252.0,
                                  8581.0, 8918.0, 9264.0, 9617.0, 9978.0,
                                  10349.0, 10739.0, 11136.0, 11544.0,
                                  11959.0, 12385.0, 12824.0, 13273.0,
                                  13734.0, 14209.0, 14698.0, 15200.0,
                                  15711.0, 16244.0, 16785.0, 17337.0,
                                  17907.0, 18484.0, 19083.0, 19693.0,
                                  20314.0, 20948.0, 21600.0, 22266.0,
                                  22952.0, 23651.0, 24371.0]),


                  'l1': np.array([-1.0, -1.0, -1.0, 5.3, 8.0, 12.6, 18.0,
                                  37.3, 41.6, 45.0, 48.5, 63.5, 88.6,
                                  117.8, 149.7, 189.0, 230.9, 270.0, 326.3,
                                  378.6, 438.4, 498.0, 560.9, 626.7, 696.0,
                                  769.1, 844.6, 925.1, 1008.6, 1096.7,
                                  1196.2, 1299.0, 1414.6, 1527.0, 1652.0,
                                  1782.0, 1921.0, 2065.0, 2216.0, 2373.0,
                                  2532.0, 2698.0, 2866.0, 3043.0, 3224.0,
                                  3412.0, 3604.0, 3806.0, 4018.0, 4238.0,
                                  4465.0, 4698.0, 4939.0, 5188.0, 5453.0,
                                  5714.0, 5989.0, 6266.0, 6548.0, 6835.0,
                                  7126.0, 7428.0, 7737.0, 8052.0, 8376.0,
                                  8708.0, 9046.0, 9394.0, 9751.0, 10116.0,
                                  10486.0, 10870.0, 11271.0, 11682.0,
                                  12100.0, 12527.0, 12968.0, 13419.0,
                                  13880.0, 14353.0, 14839.0, 15347.0,
                                  15861.0, 16388.0, 16939.0, 17493.0,
                                  18049.0, 18639.0, 19237.0, 19840.0,
                                  20472.0, 21105.0, 21757.0, 22427.0,
                                  23104.0, 23808.0, 24526.0, 25256.0]),

                  'm5': np.array([-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0,
                                  -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0,
                                  -1.0, -1.0, -1.0, -1.0, -1.0, -1.0,
                                  -1.0,-1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 3.0,
                                  4.0, 5.0, 10.1, 18.7, 29.2, 41.7,
                                  54.6,69.0, 93.8, 112.0, 134.2, 155.8,
                                  178.8, 202.3, 227.9, 253.9, 280.0,
                                  307.2,335.2, 368.3, 405.2, 443.9, 484.9,
                                  528.2, 573.0, 619.3, 676.4, 726.6,780.5,
                                  836.0, 883.8, 928.8, 980.4, 1027.0,
                                  1083.4, 1127.5, 1189.6, 1241.1, 1292.0,
                                  1351.0, 1409.0, 1468.0, 1528.0, 1589.0,
                                  1662.0, 1735.0, 1809.0, 1883.0, 1960.0,
                                  2040.0, 2122.0, 2206.0, 2295.0, 2389.0,
                                  2484.0, 2580.0, 2683.0, 2787.0, 2892.0,
                                  3000.0, 3105.0, 3219.0, 3332.0, 3442.0,
                                  3552.0, 3664.0, 3775.0, 3890.0, 4009.0,
                                  4127.0])}

_xraydb = None

def get_xraydb():
    """return instance of the XrayDB

    Returns:
        XrayDB

    Example:
        >>> import xraydb
        >>> xdb = xraydb.get_xraydb()

    """
    global _xraydb
    if _xraydb is None:
        _xraydb = XrayDB()
    return _xraydb

def f0(ion, q):
    """elastic X-ray scattering factor, f0(q), for an ion.

    Args:
       ion (int or str):  atomic number, atomic symbol or ionic symbol of scatterer

       q  (float, ndarray):  Q value(s)  for scattering

    Returns
       scattering factor for each Q value

    Notes:
       1.  from D. Waasmaier and A. Kirfel, Acta Cryst. A51 p416 (1995) and
           International Tables for Crystallography, Vol. C.
       2.  `ion` can be of the form: 26, `Fe`, `Fe2+`.  For a full list of ions
           use `f0_ions()`
       3. elements supported are from Z = 1 to 98 ('H' to 'Cf')
       4. q = sin(theta) / lambda, where theta=incident angle, lambda=X-ray wavelength

    """
    xdb = get_xraydb()
    return xdb.f0(ion, q)

def f0_ions(element=None):
    """list ion names supported in the f0() calculation from
    Waasmaier and Kirfel.

    Args:
      element (None, int, str):  scatterer

    Returns:
      list of strings for matching ion names

    Notes:
        if element is None, all 211 ions are returned.
    """
    xdb = get_xraydb()
    return xdb.f0_ions(element=element)

def chantler_energies(element, emin=0, emax=1.e9):
    """energies at which Chantler data is tabulated for a particular element.

    Args:
        element (int, str):  atomic number, atomic symbol for element
        emin (float):        lower bound of energies (default=0)
        emax (float):        upper bound of energies (default=1.e9)

    Returns:
        ndarray of energies

    Notes:
        energies are in eV
    """
    xdb = get_xraydb()
    return xdb.chantler_energies(element, emin=emin, emax=emax)


def chantler_data(element, energy, column, **kws):
    """data from Chantler tables.

    Args:
        element (int, str):  atomic number, atomic symbol for element
        energy (float or ndarray):   energy or array of energies
        column (str): data to return, one of 'f1', 'f2', 'mu_photo',
                     'mu_incoh', 'mu_total'

    Returns:
        value or ndarray of values
    """
    xdb = get_xraydb()
    return xdb._from_chantler(element, energy, column=column, **kws)


def f1_chantler(element, energy, **kws):
    """real part of anomalous x-ray scattering factor for an element and
    energy or array of energies.   Data is from the Chantler tables.

    Args:
        element (int, str):  atomic number, atomic symbol for element
        energy (float or ndarray):   energy or array of energies

    Returns:
        float value or ndarray

    Notes:
        1. Values returned are in units of electrons

    """
    xdb = get_xraydb()
    return xdb.f1_chantler(element, energy, **kws)


def f2_chantler(element, energy):
    """imaginary part of anomalous x-ray scattering factor for an element and
    energy or array of energies.   Data is from the Chantler tables.

    Args:
        element (int, str):  atomic number, atomic symbol for element
        energy (float or ndarray):   energy or array of energies

    Returns:
        float value or ndarray

    Notes:
        1. Values returned are in units of electrons

    """
    xdb = get_xraydb()
    return xdb.f2_chantler(element, energy)


def mu_chantler(element, energy, incoh=False, photo=False):
    """X-ray mass attenuation coeficient, mu/rho, for an element and
    energy or array of energies.   Data is from the Chantler tables.

    Args:
        element (int, str):  atomic number, atomic symbol for element
        energy (float or ndarray):   energy or array of energies
        incoh (bool): whether to return only the incoherent contribution [False]
        photo (bool): whether to return only the photo-electric contribution [False]

    Returns:
        float value or ndarray

    Notes:
        1. Values returned are in units of cm^2/gr
        2. The default is to return total attenuation coefficient.
    """
    xdb = get_xraydb()
    return xdb.mu_chantler(element, energy, incoh=incoh, photo=photo)

def mu_elam(element, energy, kind='total'):
    """X-ray mass attenuation coefficient, mu/rho, for an element and
    energy or array of energies.  Data is from the Elam tables.

    Args:
        element (int, str):  atomic number, atomic symbol for element
        energy (float or ndarray):   energy or array of energies
        kind (str):  type of cross-section to use, one of ('total',
                     'photo', 'coh', 'incoh') ['total']

    Returns:
        float value or ndarray

    Notes:
        1. Values returned are in units of cm^2/gr
        2. The default is to return total attenuation coefficient.

    """
    xdb = get_xraydb()
    return xdb.mu_elam(element, energy, kind=kind)


def coherent_cross_section_elam(element, energy):
    """coherent scaattering cross-section for an element and
    energy or array of energies.  Data is from the Elam tables.

    Args:
        element (int, str):  atomic number, atomic symbol for element
        energy (float or ndarray):   energy or array of energies

    Returns:
        float value or ndarray

    Notes:
        1. Values returned are in units of cm^2/gr
    """
    xdb = get_xraydb()
    return xdb.coherent_cross_section_elam(element, energy)


def incoherent_cross_section_elam(element, energy):
    """incoherent scaattering cross-section for an element and
    energy or array of energies.  Data is from the Elam tables.

    Args:
        element (int, str):  atomic number, atomic symbol for element
        energy (float or ndarray):   energy or array of energies

    Returns:
        float value or ndarray

    Notes:
        1. Values returned are in units of cm^2/gr
    """
    xdb = get_xraydb()
    return xdb.incoherent_cross_section_elam(element, energy)


def atomic_number(element):
    """z for element name

    Args:
        element (str):  atomic symbol

    Returns:
        atomic number
    """
    xdb = get_xraydb()
    return int(xdb._elem_data(element).Z)


def atomic_symbol(z):
    """atomic symbol for atomic number

    Args:
        z (int):  atomic number

    Returns:
        atomic symbol
    """
    xdb = get_xraydb()
    return xdb._elem_data(z).symbol


def atomic_mass(element):
    """molar mass for an element

    Args:
        element (int, str):  atomic number, atomic symbol for element

    Return:
        atomic mass, in AMU
    """
    xdb = get_xraydb()
    if isinstance(element, int):
        element = atomic_symbol(element)
    return xdb._elem_data(element).mass


def atomic_density(element):
    """density (gr/cm^3) for common for of an element

    Args:
        element (int, str):  atomic number, atomic symbol for element

    Return:
        density in gm/cm^3

    """
    xdb = get_xraydb()
    if isinstance(element, int):
        element = atomic_symbol(element)
    return xdb._elem_data(element).density


def xray_edges(element):
    """get dictionary of x-ray absorption edges:
         energy(in eV),
         fluorescence yield, and
         jump ratio for an element.

    Args:
        element (int, str):  atomic number, atomic symbol for element

    Return:
        dictionary of XrayEdge named tuples.

    Notes:
        1. The dictionary will have keys of edge (iupac symbol)
           and values containing an XrayEdge namedtuple containing
           (energy, fluorescence_yield, edge_jump)
    """
    xdb = get_xraydb()
    return xdb.xray_edges(element)


def xray_edge(element, edge, energy_only=False):
    """get x-ray absorption edge data for an element:
    (energy(in eV), fluorescence yield, jump ratio)

    Args:
        element (int, str):  atomic number, atomic symbol for element
        edge (str): iupac symbol of X-ray edge
        energy_only (bool): whether to return only the energy [False]

    Returns:
         XrayEdge namedtuple containing (energy,
         fluorescence_yield, edge_jump) or float of energy
    """
    xdb = get_xraydb()
    out = xdb.xray_edge(element, edge)
    if energy_only:
        out = out[0]
    return out


def xray_lines(element, initial_level=None, excitation_energy=None):
    """get dictionary of X-ray emission lines of an element

    Args:
        element (int, str):  atomic number, atomic symbol for element
        initial_level (None or str): iupac symbol of initial level
        excitation_energy (None or float): exciation energy

    Returns:
        dict of X-ray lines with keys of siegbahn notation and values of
        XrayLine tuples of (energy, intensity, initial level, final level)


    Notes:
        1. excitation energy will supercede initial_level, as it means
           'all intial levels with below this energy

    Exaample:
        >>> for name, line in xraydb.xray_lines('Mn', 'K').items():
        ...     print(name, line)
        ...
        Ka3 XrayLine(energy=5769.9, intensity=0.000265963, initial_level='K', final_level='L1')
        Ka2 XrayLine(energy=5889.1, intensity=0.293941, initial_level='K', final_level='L2')
        Ka1 XrayLine(energy=5900.3, intensity=0.58134, initial_level='K', final_level='L3')
        Kb3 XrayLine(energy=6491.8, intensity=0.042234, initial_level='K', final_level='M2')
        Kb1 XrayLine(energy=6491.8, intensity=0.0815329, initial_level='K', final_level='M3')
        Kb5 XrayLine(energy=6537.0, intensity=0.000685981, initial_level='K', final_level='M4,5')

    """
    xdb = get_xraydb()
    return xdb.xray_lines(element, initial_level=initial_level,
                          excitation_energy=excitation_energy)


def xray_line(element, line):
    """get data for an  x-ray emission line of an element, given
    the siegbahn notation for the like (Ka1, Lb1, etc).

    Returns:
         energy (in eV), intensity, initial_level, final_level

    Args:
        element (int, str):  atomic number, atomic symbol for element
        line (str):  siegbahn notation for emission line

    Returns:
        an XrayLine namedtuple with (energy, intensity, intial_level, final_level)

    Notes:
       1. if line is not a specifictransition but a generic name like
       'Ka', 'Kb', 'La', 'Lb', 'Lg', without number,  the weighted average for this
       family of lines is returned.

    """
    xdb = get_xraydb()
    lines = xdb.xray_lines(element)

    family = line.lower()
    if family == 'k': family = 'ka'
    if family == 'l': family = 'la'
    if family in ('ka', 'kb', 'la', 'lb', 'lg'):
        scale = 1.e-99
        value = 0.0
        linit, lfinal =  None, None
        for key, val in lines.items():
            if key.lower().startswith(family):
                value += val[0]*val[1]
                scale += val[1]
                if linit is None:
                    linit = val[2]
                if lfinal is None:
                    lfinal = val[3][0]
        return XrayLine(value/scale, scale, linit, lfinal)
    else:
        return lines.get(line.title(), None)


def fluor_yield(element, edge, line, energy):
    """fluorescence yield for an X-ray emission line or family of lines.

    Args:
        element (int, str):  atomic number, atomic symbol for element
        edge (str): iupac symbol of X-ray edge
        line (str): siegbahn notation for emission line
        energy (float): incident X-ray energy

    Returns:
        fluorescence yield, weighted average fluorescence energy, net_probability


    Examples:
        >>> xraydb.fluor_yield('Fe', 'K', 'Ka', 8000)
        0.350985, 6400.752419799043, 0.874576096

        >>> xraydb.fluor_yield('Fe', 'K', 'Ka', 6800)
        0.0, 6400.752419799043, 0.874576096

        >>> xraydb.fluor_yield('Ag', 'L3', 'La', 6000)
        0.052, 2982.129655446868, 0.861899000000000

    See Also:
         `xray_lines` which gives the full set of emission lines ('Ka1', 'Kb3',
         etc) and probabilities for each of these.

    """
    e0, fyield, jump = xray_edge(element, edge)
    trans  = xray_lines(element, initial_level=edge)

    lines = []
    net_ener, net_prob = 0., 0.
    for name, vals in trans.items():
        en, prob = vals[0], vals[1]
        if name.startswith(line):
            lines.append([name, en, prob])

    for name, en, prob in lines:
        if name.startswith(line):
            net_ener += en*prob
            net_prob += prob
    if net_prob <= 0:
        net_prob = 1
    net_ener = net_ener / net_prob
    if energy < e0:
        fyield = 0
    return fyield, net_ener, net_prob


def ck_probability(element, initial, final, total=True):
    """transition probability for an element, initial, and final levels.

    Args:
        element (int, str):  atomic number, atomic symbol for element
        initial (str):  iupac symbol for initial level
        final (str):  iupac symbol for final level
        total (bool): whether to include transitions via possible
                      intermediate levels [True]

    Returns:
        transition probability, or 0 if transition is not allowed.
    """
    xdb = get_xraydb()
    return xdb.ck_probability(element, initial, final, total=total)


def core_width(element, edge=None):
    """returns core hole width for an element and edge

    Args:
        element (int or str): element
        edge (None or str):  edge to consider

    Returns:
        core width or list of core widths

    Notes:
       1. if edge is None, values are return for all edges
       2. Data from Krause and Oliver (1979) and  Keski-Rahkonen and Krause (1974)

    """
    xdb = get_xraydb()
    return xdb.corehole_width(element, edge=edge)

def ionization_potential(gas):
    """return effective ionization potential for a gas, as appropriate for
    ionization chambers in the linear regime (not 'proportional counter' regime)

    Args:
        gas (string):  name of gas

    Returns:
        ionization potential in eV

    Notes:
       Data from G. F. Knoll, Radiation Detection and Measurement, Table 5-1, and
       from ICRU Report 31, 1979.  Supported gas names and effective potentials:

           ==================== ================
            gas names            potential (eV)
           -------------------- ----------------
            hydrogen, H           36.5
            helium, He            41.3
            nitrogren, N, N2      34.8
            oxygen, O, O2         30.8
            neon, Ne              35.4
            argon, Ar             26.4
            krypton, Kr           24.4
            xenon, Xe             22.1
            air                   33.8
            methane, CH4          27.3
            carbondioxide, CO2    33.0
           ==================== ================

       If the gas is not recognized the default value of 32.0 eV will be returned.

    """
    xdb = get_xraydb()
    try:
        return xdb.ionization_potential(gas)
    except:
        return 32.0


def guess_edge(energy, edges=['K', 'L3', 'L2', 'L1', 'M5']):
    """guess an element and edge based on energy (in eV)

    Args:
        energy (float) : approximate edge energy (in eV)
        edges (None or list of strings) : edges to consider

    Returns:
        a tuple of (atomic symbol, edge) for best guess

    Notes:
        by default, the list of edges is ['K', 'L3', 'L2', 'L1', 'M5']

    """
    xdb = get_xraydb()
    ret = []
    min_diff = 1e9

    for edge in edges:
        ename =  edge.lower()
        # if not already in _edge_energies, look it up and save it now

        if ename not in _edge_energies:
            energies = [-1000]*150
            maxz = 0
            for row in xdb.tables['xray_levels'].select().execute().fetchall():
                ir, elem, edgename, en, eyield, xjump = row
                iz = xdb.atomic_number(elem)
                maxz = max(iz, maxz)
                if ename == edgename.lower():
                    energies[iz] = en
            _edge_energies[ename] = np.array(energies[:maxz])

        energies = _edge_energies[ename]
        iz = int(index_nearest(energies, energy))
        diff = energy - energies[iz]
        if diff < 0: # prefer positive errors
            diff = -2.0*diff
        if iz < 10 or iz > 92: # penalize extreme elements
            diff = 2.0*diff
        if edge == 'K': # prefer K edge
            diff = 0.25*diff
        elif edge in ('L1', 'M5'): # penalize L1 and M5 edges
            diff = 2.0*diff
        if diff < min_diff:
            min_diff = diff
        ret.append((edge, iz, diff))

    for edge, iz, diff in ret:
        if abs(diff - min_diff) < 2:
            return (atomic_symbol(iz), edge)
    return (None, None)


class Scatterer:
    """Scattering Element

    lamb=PLANCK_HC /(eV0/1000.)*1e-11    # in cm, 1e-8cm = 1 Angstrom
    Xsection=2* R_ELECTRON_CM *lamb*f2/BARN    # in Barns/atom
    """
    def __init__(self, symbol, energy=10000):
        # atomic symbol and incident x-ray energy (eV)
        self.symbol = symbol
        self.number = atomic_number(symbol)
        self.mass   = atomic_mass(symbol)
        self.f1     = self.number + f1_chantler(symbol, energy)
        self.f2     = f2_chantler(symbol, energy)
        self.mu_photo = chantler_data(symbol, energy, 'mu_photo')
        self.mu_total = chantler_data(symbol, energy, 'mu_total')

def xray_delta_beta(material, density, energy):
    """anomalous components of the index of refraction for a material,
    using the tabulated scattering components from Chantler.

    Args:
       material:   chemical formula  ('Fe2O3', 'CaMg(CO3)2', 'La1.9Sr0.1CuO4')
       density:    material density in g/cm^3
       energy:     x-ray energy in eV

    Returns:
      (delta, beta, atlen)

    where
      delta :  real part of index of refraction
      beta  :  imag part of index of refraction
      atlen :  attenuation length in cm

    These are the anomalous scattering components of the index of refraction:

    n = 1 - delta - i*beta = 1 - lambda**2 * r0/(2*pi) Sum_j (n_j * fj)

    Adapted from code by Yong Choi

    """

    lamb_cm = 1.e-8 * PLANCK_HC / energy # lambda in cm
    elements = []

    for symbol, number in chemparse(material).items():
        elements.append((number, Scatterer(symbol, energy)))

    total_mass, delta, beta_photo, beta_total = 0, 0, 0, 0
    for (number, scat) in elements:
        weight      = density*number*AVOGADRO
        delta      += weight * scat.f1
        beta_photo += weight * scat.f2
        beta_total += weight * scat.f2*(scat.mu_total/scat.mu_photo)
        total_mass += number * scat.mass

    scale = lamb_cm * lamb_cm * R_ELECTRON_CM / (2*np.pi*total_mass)
    delta  *= scale
    beta_photo *= scale
    beta_total *= scale
    if isinstance(beta_total, np.ndarray):
        beta_total[np.where(beta_total<1.e-99)] = 1.e-99
    else:
        beta_total = max(beta_total, 1.e-19)
    return delta, beta_photo, lamb_cm/(4*np.pi*beta_total)

def mirror_reflectivity(formula, theta, energy, density=None,
                        roughness=0.0, polarization='s'):
    """mirror reflectivity for a thick, singl-layer mirror.

    Args:
       formula (string):           material name or formula ('Si', 'Rh', 'silicon')
       theta (float or nd-array):  mirror angle in radians
       energy (float or nd-array): X-ray energy in eV
       density (float or None):    material density in g/cm^3
       roughness (float):          mirror roughness in Angstroms
       polarization ('s' or 'p'):  mirror orientation relative to X-ray polarization

    Returns:
       mirror reflectivity values

    Notes:
       1. only one of theta or energy can be an nd-array
       2. density can be `None` for known materials
       3. polarization of 's' puts the X-ray polarization along the mirror
          surface, 'p' puts it normal to the mirror surface. For
          horizontally polarized X-ray beams from storage rings, 's' will
          usually mean 'vertically deflecting' and 'p' will usually mean
          'horizontally deflecting'.
    """
    from .materials import get_material
    if density is None:
        formula, density = get_material(formula)

    delta, beta, _ = xray_delta_beta(formula, density, energy)
    n = 1 - delta - 1j*beta

    # kiz is k in air/vacuum,  with n = 1.
    # ktz is k in mirror material, with n < 1.
    # Note: kiz and ktz should have a factor of (2*pi/lambda)
    # but this will cancel in the calculation of r_amp, so we drop it here.
    kiz = np.sin(theta)
    ktz = np.sqrt(n**2 - np.cos(theta)**2)

    # polarization correction will be tiny for small angles
    if polarization == 'p':
        ktz = ktz / n

    r_amp = (kiz - ktz)/(kiz + ktz)
    if roughness > 1.e-12:
        r_amp = r_amp * np.exp(-2*(roughness**2*kiz*ktz))
    return (r_amp*r_amp.conjugate()).real


def ionchamber_fluxes(gas='nitrogen', volts=1.0, length=100.0,
                      energy=10000.0, sensitivity=1.e-6,
                      sensitivity_units='A/V'):
    
    """return ion chamber fluxes for a gas or mixture of gases, ion chamber
    length, X-ray energy, recorded voltage and current amplifier sensitivity.

    Args:
        gas (string or dict):  name or formula of fill gas (see note 1) ['nitrogen']
        volts (float):  measured voltage output of current amplifier  [1.0]
        length (float): active length of ion chamber in mm [100]
        energy (float): X-ray energy in eV [10000]
        sensitivity (float): current amplifier sensitivity [1.e-6]
        sensitivity_units (string): units of current amplifier sensitivity
                                    (see note 2 for options) ['A/V']

    Returns:
        named tuple IonchamberFluxes with fields

            `photo`       flux absorbed by photo-electric effect in Hz,
            
            `incident`    flux of beam incident on ion chamber in Hz,
            
            `transmitted` flux of beam output of ion chamber in Hz 

    Notes:
       1. The gas argument can either be a string for the name of chemical
          formula for the gas, or dictionary with keys that are gas names or
          formulas and values that are the relative fraction for mixes gases.

          The gas formula is used in two ways:
             a) to get the photo- and total- absorption coefficient, and
             b) to get the effective ionization potential for the gas.

          The effective ionization potentials are known for a handful of
          gases (see `ionization_potential` function), all ranging between
          20 and 45 eV. For unknown gases the value of 32.0 eV will be
          used.

       2. The `sensitivity` and `sensitivity_units` arguments have some overlap
          to specify the sensitivity or gain of the current amplifier.
          Generally, the units in `A/V`, but you can add a common SI prefix of
 
          'p', 'pico', 'n', 'nano', '\u03bc', 'u', 'micro', 'm', 'milli'
          
          so that, for example
             ionchamber_fluxes(..., sensitivity=1.e-6)
          and 
             ionchamber_fluxes(..., sensitivity=1, sensitivity_units='uA/V')

          will both give a sensitivity of 1 microAmp / Volt . 
               
    Examples:
        >>> ionchamber_fluxes(gas='helium', volts=1.25, length=200.0,
                              energy=10000.0, sensitivity=1.e-9)
        IonChamberFluxes(photo=16110895.3, incident=15452608024.6, transmitted=15316549138.8)

        >>> ionchamber_fluxes(gas='nitrogen', volts=1.25, length=200.0,
                              energy=10000.0, sensitivity=1.e-9)
        IonChamberFluxes(photo=13575282.2, incident=23102328.0, transmitted=8759458.7)

        >>> ionchamber_fluxes(gas={'nitrogen':0.5, 'helium': 0.5}, volts=1.25,
                              length=200.0, energy=10000.0, sensitivity=1.e-9)
        IonChamberFluxes(photo=14843088.8, incident=7737855176.4, transmitted=7662654298.8)

    
    """
    from .materials import material_mu

    fin = fout = fphoto = 0.0

    units = sensitivity_units.replace('Volts', 'V').replace('Volt', 'V')
    units = units.replace('Amperes', 'A').replace('Ampere', 'A')
    units = units.replace('Amps', 'A').replace('Amp', 'A')    
    units = units.replace('A/V', '')
    sensitivity *= SI_PREFIXES.get(units, 1)

    if isinstance(gas, str):
        gas = {gas: 1.0}
    
    gas_total = 0.0
    gas_comps = []
    for gname, frac in gas.items():
        ionpot = ionization_potential(gname)
        if gname == 'N2': gname = 'nitrogen'
        if gname == 'O2': gname = 'oxygen'
        gas_total += frac
        gas_comps.append((gname, frac, ionpot))


    # note on Photo v Total attenuation:
    # the current is from the photo-electric cross-section, so that
    #   flux_photo = flux_in * [1 - exp(-t*mu_photo)]
    # while total attenuation means
    #   flux_out = flux_in * exp(-t*mu_total)

    for gas, frac, ionpot in gas_comps:
        mu_photo = material_mu(gas, energy=energy, kind='photo')
        mu_total = material_mu(gas, energy=energy, kind='total')

        flux_photo = volts * sensitivity * ionpot / (2 * QCHARGE * energy)
        flux_photo *= (frac/gas_total)
        flux_in    = flux_photo / (1.0 - np.exp(-length*mu_photo))
        flux_out   = flux_in * np.exp(-length*mu_total)

        fphoto += flux_photo
        fin    += flux_in 
        fout   += flux_out

    return fluxes(photo=fphoto, incident=fin,transmitted=fout)

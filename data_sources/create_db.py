'''
This script creates an SQLite3 database of fundamental X-ray fluorescence
parameters as compiled by W.T. Elam, B.D. Ravel and J.R. Sieber, published in
Radiation Physics and Chemistry, 63 (2), 121 (2002). The database is published
by NIST at http://www.cstl.nist.gov/acd/839.01/xrfdownload.html
'''

import io
import json
import os
import time
import sqlite3
from collections import namedtuple

def add_Version(dest, append=True):
    """add Version Information"""
    if os.path.exists(dest) and not append:
        raise IOError('File "%s" already exists -- cannot add Version')

    conn = sqlite3.connect(dest)
    c = conn.cursor()
    c.execute('''create table Version (id integer primary key, tag text, date text, notes text)''')

    source = 'Version.dat'
    version_lines = []
    if os.path.exists(source):
        with io.open(source, mode='r', encoding='ascii') as f:
            version_lines = f.readlines()
    rowid = 0
    for line in version_lines:
        if not line.startswith('#') and len(line)> 3:
            _tag, _date, _notes = [l.strip() for l in line.split('//', 2)]
            rowid += 1
            c.execute('insert into Version values (?,?,?,?)',
                      (rowid, _tag, _date, _notes))

    conn.commit()
    c.close()


def add_elementaldata(dest):
    source = 'elemental_data.txt'
    if not os.path.isfile(source):
        raise IOError('File "%s" does not exist' % source)

    conn = sqlite3.connect(dest)
    c = conn.cursor()
    c.execute('''create table elements (atomic_number integer primary key,
        element text, molar_mass real, density real)
        ''')
    with io.open(source, encoding='ascii') as f:
        for line in f.readlines():
            if line.startswith('#'):
                continue
            num, sym, mw, rho = line[:-1].split()
            c.execute('insert into elements values (?,?,?,?)', (num, sym, mw, rho))
    conn.commit()
    c.close()

def add_ionization_potentials(dest):
    source = 'ion_chamber_potentials.txt'
    if not os.path.isfile(source):
        raise IOError('File "%s" does not exist' % source)

    conn = sqlite3.connect(dest)
    c = conn.cursor()
    c.execute('create table ionization_potentials (gas text,  potential real)')
    with io.open(source, encoding='ascii') as f:
        for line in f.readlines():
            if line.startswith('#'):
                continue

            line = line[:-1].strip()
            if len(line)  > 2:
                words = line.split()
                potential = words.pop()
                gas = ' '.join(words)
                c.execute('insert into ionization_potentials values (?,?)', (gas, potential))
    conn.commit()
    c.close()

def add_compton_energies(dest):
    """add energies for Compton scattering as a function on incident X-ray energy:
    Energy                : energy of incident X-ray
    Compton_xray_90deg    : energy of X-ray scattered at theta=90
    Compton_xray_mean     : mean energy of Compton-scattered X-ray
    Compton_electron_mean : mean energy of Compton-scattered electron
    """
    source = 'Compton_energies.txt'
    if not os.path.isfile(source):
        raise IOError('File "%s" does not exist' % source)

    conn = sqlite3.connect(dest)
    c = conn.cursor()
    c.execute('create table Compton_energies (incident text, xray_90deg text, xray_mean text, electron_mean text)')
    e, cx90, cxmean, cemean = [], [], [], []
    with io.open(source, encoding='ascii') as f:
        for line in f.readlines():
            if line.startswith('#'):
                continue

            line = line[:-1].strip()
            if len(line)  > 2:
                words = line.split()
                e.append(float(words[0]))
                cx90.append(float(words[1]))
                cxmean.append(float(words[2]))
                cemean.append(float(words[3]))

    c.execute('insert into compton_energies values (?,?,?,?)', (json.dumps(e),
                                                                json.dumps(cx90),
                                                                json.dumps(cxmean),
                                                                json.dumps(cemean)))
    conn.commit()
    c.close()

def add_corehole_data(dest, append=True):
    """add core-widths from Keski-Rahkonen and Krause. Data from
    Atomic Data and Nuclear Data Tables, Vol 14, Number 2, 1974 and
    from  Krause and Oliver, J. Phys. Chem. Ref. Data 8,329 (1979)

    """
    kk_source = 'keskirahkonen_krause.dat'
    ko_source = 'krause_oliver1979.dat'
    if os.path.exists(dest) and not append:
        raise IOError('File "%s" already exists -- cannot add core hole data')

    conn = sqlite3.connect(dest)
    c = conn.cursor()
    c.execute(
        '''create table KeskiRahkonen_Krause (id integer primary key,
        atomic_number integer, element text, edge text, width float)''')
    c.execute(
        '''create table Krause_Oliver (id integer primary key,
        atomic_number integer, element text, edge text, width float)''')
    c.execute(
        '''create table corelevel_widths (id integer primary key,
        atomic_number integer, element text, edge text, width float)''')

    # Keski-Rahkonen and Krause data:
    f = open(kk_source)
    lines = f.readlines()
    id = 0
    for line in lines:
        if line.startswith('#'):
            continue
        atno, elem, edge, width = line[:-1].split()
        id +=1
        atno, width = int(atno), float(width)
        c.execute('insert into KeskiRahkonen_Krause values (?,?,?,?,?)',
                      (id, atno, elem, edge, width))
        c.execute('insert into corelevel_widths values (?,?,?,?,?)',
                      (id, atno, elem, edge, width))

    # Krause and Oliver data
    f = open(ko_source)
    lines = f.readlines()
    id = 0
    for line in lines:
        if line.startswith('#'):
            continue
        words = line[:-1].strip().split()
        atno, elem, kwid, l1wid, l2wid, l3wid = words[:6]
        id +=1
        atno = int(atno)
        c.execute('insert into Krause_Oliver values (?,?,?,?,?)',
                      (id, atno, elem, 'K', float(kwid)))
        id +=1
        c.execute('insert into Krause_Oliver values (?,?,?,?,?)',
                      (id, atno, elem, 'L1', float(l1wid)))
        id +=1
        c.execute('insert into Krause_Oliver values (?,?,?,?,?)',
                      (id, atno, elem, 'L2', float(l2wid)))
        id +=1
        c.execute('insert into Krause_Oliver values (?,?,?,?,?)',
                      (id, atno, elem, 'L3', float(l3wid)))

        c.execute('update corelevel_widths set width=? where atomic_number=? and edge=?',
                      (float(kwid), atno, 'K'))
        c.execute('update corelevel_widths set width=? where atomic_number=? and edge=?',
                      (float(l1wid), atno, 'L1'))
        c.execute('update corelevel_widths set width=? where atomic_number=? and edge=?',
                      (float(l2wid), atno, 'L2'))
        c.execute('update corelevel_widths set width=? where atomic_number=? and edge=?',
                      (float(l3wid), atno, 'L3'))

    conn.commit()
    c.close()

def add_Krause_Oliver(dest, append=True):
    """add core-widths from Krause and Oliver,
    J. Phys. Chem. Ref. Data 8,329 (1979)
    """
    source = 'krause_oliver1979.dat'
    if os.path.exists(dest) and not append:
        raise IOError('File "%s" already exists -- cannot add core hole data')

    conn = sqlite3.connect(dest)
    c = conn.cursor()
    c.execute(
        '''create table Krause_Oliver (id integer primary key,
        atomic_number integer, element text, edge text, width float)''')


    conn.commit()
    c.close()


def add_Waasmaier(dest, append=True):
    """add f0 data from Waasmaier and Kirfel"""
    source = 'waasmaeir_kirfel.dat'

    if os.path.exists(dest) and not append:
        raise IOError('File "%s" already exists -- cannot add f0 data')

    conn = sqlite3.connect(dest)
    c = conn.cursor()
    c.execute(
        '''create table Waasmaier (id integer primary key,
        atomic_number integer, element text, ion text,
        offset real, scale text, exponents text)
        ''')

    f = open(source)
    lines = f.readlines()
    if 'Elastic Photon-Atom Scatt' not in lines[1]:
        raise RuntimeError('Source file not recognized for f0_WaasKirf data')

    strip_ion = str.maketrans('0123456789+-', ' '*12)
    id = 0
    while lines:
        line = lines.pop(0)
        if line.startswith('#S '):
            id += 1
            #print [s for s in line[3:].split()]
            zstr, ion = [s.strip() for s in line[3:].split()]
            atno = int(zstr)
            for i in range(3):
                line = lines.pop(0)
            words = [float(w.strip()) for w in line.split()]
            off   = words[5]
            scale = json.dumps(words[:5])
            expon = json.dumps(words[6:])

            elem = ion.translate(strip_ion).strip()
            for suffix in (('va', 'val')):
                if elem.endswith(suffix):
                    elem = elem[:-len(suffix)]

            c.execute('insert into Waasmaier values (?,?,?,?,?,?,?)',
                      (id, atno, elem, ion, off, scale, expon))

    conn.commit()
    c.close()

def add_Chantler(dest, append=True, table='Chantler', subdir='fine', suffix='.dat'):
    """add f' / f'', mu data from Chantler"""
    dirname = os.path.join('chantler', subdir)

    if os.path.exists(dest) and not append:
        raise IOError('File "%s" already exists -- cannot add f0 data')

    conn = sqlite3.connect(dest)
    c = conn.cursor()
    c.execute(
        '''create table %s (id integer primary key,
        element text, sigma_mu real, mue_f2 real, density real,
        corr_henke float, corr_cl35 float, corr_nucl float,
        energy text, f1 text, f2 text, mu_photo text,
        mu_incoh text, mu_total text)
        ''' % table)

    args = '(%s)' % ','.join(['?']*14)

    nelem = 92
    for z in range(1, nelem+1):
        fname = os.path.join(dirname, '%2.2i.dat' % z)
        lines = open(fname, 'r').readlines()

        # line 1: take symbol and density only
        words = lines[0][1:-1].split()
        words.pop()
        density = float(words.pop())
        elem = words[0].replace(':','')

        # line 2: take sigma_mu
        words = lines[1][1:-1].split()
        sigma_mu = float(words.pop())

        # line 3: take mue_f2
        words = lines[2][1:-1].split()
        mue_f2 = float(words.pop())

        en, f1, f2, mu_photo, mu_incoh, mu_total = [], [], [], [], [], []
        corr_henke, corr_cl35, corr_nucl = 0, 0, 0
        for line in lines:
            if line.startswith('#'):
                if 'Relativistic' in line or 'Nuclear Thomson' in line:
                    line = line[1:-1].replace('#', ' ').strip()
                    label, val = line.split('=')
                    val = val.replace(',', '').replace('e/atom', '')
                    if 'Relativistic' in line:
                        corr_henke, corr_cl35 = [float(x) for x in val.split()]
                    else:
                        corr_nucl = float(val)
                continue

            words = [float(w) for w in line[:-1].split()]
            en.append(1000.0*words[0])
            f1.append(words[1]  - z + corr_cl35 + corr_nucl)
            f2.append(words[2])
            mu_photo.append(words[3])
            mu_incoh.append(words[4])
            mu_total.append(words[3]+words[4])

        query = 'insert into %s values %%s' % table

        c.execute(query % args,
                  (z, elem, sigma_mu, mue_f2, density,
                   corr_henke, corr_cl35, corr_nucl,
                   json.dumps(en), json.dumps(f1), json.dumps(f2),
                   json.dumps(mu_photo), json.dumps(mu_incoh),
                   json.dumps(mu_total)))

    conn.commit()
    c.close()


def add_Elam(dest, overwrite=False, silent=False):
    source = 'elam.dat'
    if not os.path.isfile(source):
        if silent:
            return
        raise IOError('File "%s" does not exist' % source)
    if os.path.isfile(dest) and overwrite:
        os.remove(dest)
    if os.path.exists(dest):
        if silent:
            return
        raise IOError('File "%s" already exists. Use "-f" to overwrite' % dest)

    with io.open(source, encoding='ascii') as f:
        lines = f.readlines()
        if 'Elam, Ravel, Sieber' not in lines[0]:
            raise RuntimeError('Source file not recognized')
        while lines[0].startswith('/'):
            lines.pop(0)

    conn = sqlite3.connect(dest)
    c = conn.cursor()

    current_edge_id = 0
    c.execute(
        '''create table xray_levels (id integer primary key, element text,
        iupac_symbol text, absorption_edge real, fluorescence_yield real,
        jump_ratio real)
        '''
        )
    current_line_id = 0
    c.execute(
        '''create table xray_transitions (id integer primary key, element text,
        iupac_symbol text, siegbahn_symbol text, initial_level text,
        final_level text, emission_energy real, intensity real)
        '''
        )
    current_ck_id = 0
    c.execute(
        '''create table Coster_Kronig (id integer primary key, element text,
        initial_level text, final_level text,
        transition_probability real, total_transition_probability real)
        '''
        )
    current_photo_id = 0
    c.execute(
        '''create table photoabsorption (id integer primary key, element text,
        log_energy text, log_photoabsorption text,
        log_photoabsorption_spline text)
        '''
        )
    current_scatter_id = 0
    c.execute(
        '''create table scattering (id integer primary key, element text,
        log_energy text,
        log_coherent_scatter text, log_coherent_scatter_spline text,
        log_incoherent_scatter text, log_incoherent_scatter_spline text)
        '''
        )

    while lines:
        line = lines.pop(0)
        if line.startswith('Element'):
            sym, num, mw, rho = line.split()[1:]
            current_element = sym
        elif line.startswith('Edge'):
            current_edge_id += 1
            label, energy, yield_, jump = line.split()[1:]
            el = current_element
            c.execute(
                'insert into xray_levels values (?,?,?,?,?,?)',
                (current_edge_id, el, label, energy, yield_, jump)
                )
            current_edge = label
        elif line.startswith('  Lines'):
            while True:
                if lines[0].startswith('    '):
                    current_line_id += 1
                    line = lines.pop(0)
                    iupac, siegbahn, energy, intensity = line.split()
                    start, end = iupac.split('-')
                    el = current_element
                    c.execute(
                        'insert into xray_transitions values (?,?,?,?,?,?,?,?)',
                        (current_line_id, el, iupac, siegbahn, start, end,
                        energy, intensity)
                        )
                else:
                    break
        elif line.startswith('  CK '):
            temp = line.split()[1:]
            ck = []
            while temp:
                (i,j), temp = temp[:2], temp[2:]
                ck.append((i,j))
            if lines[0].startswith('  CKtotal'):
                temp = lines.pop(0).split()[1:]
                ck_total = []
                while temp:
                    (i,j), temp = temp[:2], temp[2:]
                    ck_total.append((i,j))
            else:
                ck_total = ck
            for i, j in zip(ck, ck_total):
                current_ck_id += 1
                (so, p), tp = i[:], j[1]
                c.execute(
                    '''insert into Coster_Kronig
                    values (?,?,?,?,?,?)''',
                    (current_ck_id, current_element, current_edge, so, p, tp)
                    )
        elif line.startswith('Photo'):
            current_photo_id += 1
            energy = []
            photo = []
            spline = []
            while lines[0].startswith('    '):
                temp = [float(i) for i in lines.pop(0).split()]
                energy.append(temp[0])
                photo.append(temp[1])
                spline.append(temp[2])
            c.execute(
                'insert into photoabsorption values (?,?,?,?,?)',
                (current_photo_id, current_element, json.dumps(energy),
                json.dumps(photo), json.dumps(spline))
                )
        elif line.startswith('Scatter'):
            current_scatter_id += 1
            energy = []
            cs = []
            css = []
            ics = []
            icss = []
            while lines[0].startswith('    '):
                temp = [float(i) for i in lines.pop(0).split()]
                energy.append(temp[0])
                cs.append(temp[1])
                css.append(temp[2])
                ics.append(temp[3])
                icss.append(temp[4])
            c.execute(
                'insert into scattering values (?,?,?,?,?,?,?)',
                (current_scatter_id, current_element, json.dumps(energy),
                json.dumps(cs), json.dumps(css), json.dumps(ics),
                json.dumps(icss))
                )

    conn.commit()
    c.close()

_EADL_doc = """
The 1997 release of the Evaluated Atomic Data Library (EADL97)

This module parses the EADL.DAT file that can be downloaded from:

http://www-nds.iaea.org/epdl97/libsall.htm

EADL contains atomic relaxation information for use in particle transport
analysis for atomic number Z = 1-100 and for each subshell.

The original units are in cm and MeV.

The specific data are:

- Subshell data

    a) number of electrons
    b) binding and kinetic energy (MeV)
    c) average radius (cm)
    d) radiative and non-radiative level widths (MeV)
    e) average number of released electrons and x-rays
    f) average energy of released electrons and x-rays (MeV)
    g) average energy to the residual atom, i.e., local deposition (MeV)

- Transition probability data

    a) radiation transition probabilities
    b) non-radiative transition probabilities

The data are organized in blocks with headers.

The first line of the header:

Columns    Format   Definition
1-3         I3      Z  - atomic number
4-6         I3      A  - mass number (in all cases=0 for elemental data)
8-9         I2      Yi - incident particle designator (7 is photon)
11-12       I2      Yo - outgoing particle designator (0, no particle
                                                       7, photon
                                                       8, positron
                                                       9, electron)
14-24       E11.4   AW - atomic mass (amu)

26-31       I6      Date of evaluation (YYMMDD)

The second line of the header:

Columns    Format   Definition
1-2         I2      C  - reaction descriptor
                                  = 71, coherent scattering
                                  = 72, incoherent scattering
                                  = 73, photoelectric effect
                                  = 74, pair production
                                  = 75, triplet production
                                  = 91, subshell parameters
                                  = 92, transition probabilities
                                  = 93, whole atom parameters

3-5         I2      I  - reaction property:
                                  =   0, integrated cross section
                                  =  10, avg. energy of Yo
                                  =  11, avg. energy to the residual atom
                                  = 912, number of electrons
                                  = 913, binding energy
                                  = 914, kinetic energy
                                  = 915, average radius
                                  = 921, radiative level width
                                  = 922, non-radiative level width
                                  = 931, radiative transition probability
                                  = 932, non-radiative transition probability
                                  = 933, particles per initial vacancy
                                  = 934, energy of particles per initial vacancy
                                  = 935, average energy to the residual atom, i.e.
                                         local deposition, per initial vacancy
                                  --- moved to EPDL97 ---
                                  = 941, form factor
                                  = 942, scattering function
                                  = 943, imaginary anomalous scatt. factor
                                  = 944, real anomalous scatt. factor

6-8         I3      S  - reaction modifier:
                                  =  0 no X1 field data required
                                  = 91 X1 field data required

22-32       #11.4   X1 - subshell designator
                                      0 if S is 0
                                      if S is 91, subshell designator


                 Summary of the EADL Data Base
--------------------------------------------------------------------------
Yi    C    S    X1    Yo   I          Data Types
--------------------------------------------------------------------------
                     Subshell parameters
--------------------------------------------------------------------------
0    91    0    0.    0    912        number of electrons
0    91    0    0.    0    913        binding energy
0    91    0    0.    0    914        kinetic energy
0    91    0    0.    0    915        average radius
0    91    0    0.    0    921        radiative level width
0    91    0    0.    0    921        non-radiative level width
--------------------------------------------------------------------------
                     Transititon probabilities
--------------------------------------------------------------------------
0    92    0    0.    0    935        average energy to the residual atom
0    92    0    0.  7 or 9 933        average number of particles per
                                      initial vacancy
0    92    0    0.  7 or 9 934        average energy of particles per
                                      initial vacancy
0    92   91    *     0    931        radiative transition probability
0    92   91    *     0    932        non-radiative transition probability
---------------------------------------------------------------------------
Yi    C    S    X1    Yo   I          Data Types
--------------------------------------------------------------------------

* -> Subshell designator

Data sorted in ascending order Z -> C -> S -> X1 -> Yo -> I
"""


def parse_EADL(fname):
    '''Parse the EADL data file

    Data source:

    http://www-nds.iaea.org/epdl97/libsall.htm

    Both returned dictionaries share the same keys (which are a subset of
    the header data.

    The values in the key are ``['Z', 'C', 'S', 'X1', 'Yo', 'I']``

      Z  : atomic number
      C  : {91, 92} <-> {subshell, transition}
      S  : if section depends on shell
      X1 : shell if S
      Yo : particle out {7, 9, 0} <-> {photon, electron, none}
      I  : property key
      Yi : incoming particle {0, 7} <-> {none, photon}

    Parameters
    ----------
    fname : str

    Returns
    -------
    headers : dict
        All relevant header information with human-readable aliases.

    data : dict
        Lists of namedtuple instances for this sub-table


    ''' + _EADL_doc
    SHELL_MAP = {1: 'K (1s1/2)',
                 2: 'L (2)',
                 3: 'L1 (2s1/2)',
                 4: 'L23 (2p)',
                 5: 'L2 (2p1/2)',
                 6: 'L3 (2p3/2)',
                 7: 'M (3)',
                 8: 'M1 (3s1/2)',
                 9: 'M23 (3p)',
                 10: 'M2 (3p1/2)',
                 11: 'M3 (3p3/2)',
                 12: 'M45 (3d)',
                 13: 'M4 (3d3/2)',
                 14: 'M5 (3d5/2)',
                 15: 'N (4)',
                 16: 'N1 (4s1/2)',
                 17: 'N23 (4p)',
                 18: 'N2 (4p1/2)',
                 19: 'N3 (4p3/2)',
                 20: 'N45 (4d)',
                 21: 'N4 (4d3/2)',
                 22: 'N5 (4d5/2)',
                 23: 'N67 (4f)',
                 24: 'N6 (4f5/2)',
                 25: 'N7 (4f7/2)',
                 26: 'O (5)',
                 27: 'O1 (5s1/2)',
                 28: 'O23 (5p)',
                 29: 'O2 (5p1/2)',
                 30: 'O3 (5p3/2)',
                 31: 'O45 (5d)',
                 32: 'O4 (5d3/2)',
                 33: 'O5 (5d5/2)',
                 34: 'O67 (5f)',
                 35: 'O6 (5f5/2)',
                 36: 'O7 (5f7/2)',
                 37: 'O89 (5g)',
                 38: 'O8 (5g7/2)',
                 39: 'O9 (5g9/2)',
                 40: 'P (6)',
                 41: 'P1 (6s1/2)',
                 42: 'P23 (6p)',
                 43: 'P2 (6p1/2)',
                 44: 'P3 (6p3/2)',
                 45: 'P45 (6d)',
                 46: 'P4 (6d3/2)',
                 47: 'P5 (6d5/2)',
                 48: 'P67 (6f)',
                 49: 'P6 (6f5/2)',
                 50: 'P7 (6f7/2)',
                 51: 'P89 (6g)',
                 52: 'P8 (6g7/2)',
                 53: 'P9 (6g9/2)',
                 54: 'P1011 (6h)',
                 55: 'P10 (6h9/2)',
                 56: 'P11 (6h11/2)',
                 57: 'Q (7)',
                 58: 'Q1 (7s1/2)',
                 59: 'Q23 (7p)',
                 60: 'Q2 (7p1/2)',
                 61: 'Q3 (7p3/2)'}

    Elements = ['H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne',
                'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca',
                'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn',
                'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb', 'Sr', 'Y', 'Zr',
                'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In',
                'Sn', 'Sb', 'Te', 'I', 'Xe', 'Cs', 'Ba', 'La', 'Ce', 'Pr',
                'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er',
                'Tm', 'Yb', 'Lu', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt',
                'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr',
                'Ra', 'Ac', 'Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk',
                'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr', 'Rf', 'Db', 'Sg',
                'Bh', 'Hs', 'Mt']

    KeyTuple = namedtuple('KeyTuple', ['Z', 'C', 'S', 'X1', 'Yo', 'I', 'Yi'])

    def make_dataline_key(inp_dict):
        return KeyTuple(*tuple(inp_dict[k] for k in KeyTuple._fields))

    reaction_proprety_map = {
        0: 'cross_section',
        10: 'secondary_particle_energy',
        11: 'atom_energy_transfer',
        912: 'number_of_electrons',
        913: 'binding_energy',
        914: 'kinetic_energy',
        915: 'average_radius',
        921: 'radiative_level_width',
        922: 'non-radiative_level_width',
        931: 'radiative_transition_probability',
        932: 'non-radiative_transition_probability',
        933: 'particles_per_initial_vacancy',
        934: 'energy_of_particles_per_initial_vacancy',
        935: 'average_energy_to_the_residual_atom',
        941: 'form_factor',
        942: 'scattering_function',
        943: 'imaginary_anomalous_scattering_factor',
        944: 'real_anomalous_scattering_factor',
    }
    particle_map = {7: 'photon', 0: 'none', 9: 'electron', 8: 'positron'}
    reaction_code_map = {91: 'subshell', 92: 'transition',
                         71: 'coherent scattering',
                         72: 'incoherent scattering',
                         73: 'photoelectric effect',
                         74: 'pair production',
                         75: 'triplet production',
                         93: 'whole atom parameters'}
    interpolation_map = {0: 'linear in x and y',
                         2: 'linear in x and y',
                         3: 'logarithmic in x, linear in y',
                         4: 'linear in x, logarithmic in y',
                         5: 'logarithmic in x and y'}

    def _proc_shell_int(header, row):
        klass = reaction_proprety_classes[header['I']]
        i, N = map(int, row)
        return klass(SHELL_MAP[i], i, N)

    def _proc_shell_float(header, row):
        klass = reaction_proprety_classes[header['I']]
        i, f = row
        i = int(i)
        return klass(SHELL_MAP[i], i, f)

    def _proc_radiative_transfer(header, row):
        klass = reaction_proprety_classes[header['I']]
        i = int(header['X1'])
        j, fr, Er = row
        j = int(j)
        return klass(SHELL_MAP[i], i, SHELL_MAP[j], j, fr, Er)

    def _proc_nonradiative_transfer(header, row):
        klass = reaction_proprety_classes[header['I']]
        i = int(header['X1'])
        j, k, fnr, Enr = row
        j = int(j)
        k = int(k)
        return klass(SHELL_MAP[i], i,
                     SHELL_MAP[j], j,
                     SHELL_MAP[k], k,
                     fnr, Enr)

    def _proc_float_float(header, row):
        klass = reaction_proprety_classes[header['I']]
        return klass(*row)

    reaction_proprety_classes = {
        0: namedtuple('IntegratedCrossSection',
                      ('E_incident', 'cross_section')),
        10: namedtuple('AverageEneregySecondary',
                       ('E_incident', 'E_secondary')),
        11: namedtuple('AverageEnergyResidual', ('E_incident', 'E_residual')),
        912: namedtuple('NumberOfElectrons', ('shell', 'shell_code', 'N')),
        913: namedtuple('BindingEnergy', ('shell', 'shell_code', 'E_be')),
        914: namedtuple('KeneticEnergy', ('shell', 'shell_code', 'E_ke')),
        915: namedtuple('AverageRadius', ('shell', 'shell_code', 'r_mean')),
        921: namedtuple('RadiativeLevelWidth',
                        ('shell', 'shell_code', 'gamma_r')),
        922: namedtuple('NonRadiativeLevelWidth',
                        ('shell', 'shell_code', 'gamma_nr')),
        931: namedtuple('RadiativeTransitionProbability',
                        ('primary_shell', 'primary_shell_code',
                         'secondary_shell', 'secondary_shell_code',
                         'transition_probability', 'E')),
        932: namedtuple('NonRadiativeTransitionProbability',
                        ('primary_shell', 'primary_shell_code',
                         'secondary_shell', 'secondary_shell_code',
                         'tertiary_shell', 'tertiary_shell_code',
                         'transition_probability', 'E')),
        933: namedtuple('ParticlesPerInitVacency',
                        ('shell', 'shell_code', 'N_p')),
        934: namedtuple('EnergePerInitVacency',
                        ('shell', 'shell_code', 'E_p')),
        935: namedtuple('AverageEofRisdualAtom',
                        ('shell', 'shell_code', 'E_mean')),
        941: namedtuple('FormFactor', ('x', 'F')),
        942: namedtuple('ScatteringFunction', ('x', 'S')),
        943: namedtuple('ImAnaomalousScatteringFactor', ('E_incident', 'Im')),
        944: namedtuple('ReAnaomalousScatteringFactor', ('E_incident', 'Re')),
        }

    reaction_property_funcs = {
        0: _proc_float_float,
        10: _proc_float_float,
        11: _proc_float_float,
        912: _proc_shell_int,
        913: _proc_shell_float,
        914: _proc_shell_float,
        915: _proc_shell_float,
        921: _proc_shell_float,
        922: _proc_shell_float,
        931: _proc_radiative_transfer,
        932: _proc_nonradiative_transfer,
        933: _proc_shell_float,
        934: _proc_shell_float,
        935: _proc_shell_float,
        941: _proc_float_float,
        942: _proc_float_float,
        943: _proc_float_float,
        944: _proc_float_float,
        }

    BREAK_TOKEN = ' ' * 71 + '1'

    def _fixed_width_float(val):
        split = 8 if val[8] in {'+', '-'} else 9
        base = float(val[:split])
        exp = val[split:].replace(' ', '')
        if exp:
            exp = int(exp)
        else:
            exp = 0
        return base * 10 ** exp

    in_section = False
    expect_second_header_line = False
    ret_header = {}
    ret_data = {}
    current_key = None
    cur_header = None
    with open(fname, 'r') as fin:

        for ln in fin:
            ln = ln.rstrip('\n\r')
            if expect_second_header_line:
                cur_header['C'] = C = int(ln[0:2])
                cur_header['I'] = I = int(ln[2:5])
                cur_header['S'] = S = int(ln[5:8])
                cur_header['X1'] = X1 = int(_fixed_width_float(ln[21:32]))
                cur_header['reaction_code'] = reaction_code_map[C]
                cur_header['reaction_property'] = reaction_proprety_map[I]
                cur_header['reaction_property_code'] = I
                if S == 91:
                    cur_header['subshell_code'] = X1
                    if X1 != 0:
                        cur_header['subshell'] = SHELL_MAP[X1]
                    else:
                        cur_header['subshell'] = 'none'
                elif S == 0 and X1 == 0:
                    cur_header['subshell_code'] = 0
                    cur_header['subshell'] = 'none'
                else:
                    raise ValueError('Inconsistent Data X1 = {!r}, '
                                     'S = {!r}'.forma(X1, S))

                expect_second_header_line = False
                key = make_dataline_key(cur_header)
                ret_header[key] = cur_header
                ret_data[key] = []
                current_key = key
                in_section = True
            elif not in_section:
                # read the first line
                expect_second_header_line = True

                cur_header = dict()
                cur_header['Z'] = Z = int(ln[0:3])
                cur_header['A'] = A = int(ln[3:6])
                cur_header['Yi'] = Yi = int(ln[7:9])
                cur_header['Yo'] = Yo = int(ln[10:12])
                cur_header['Aw'] = Aw = _fixed_width_float(ln[13:24])
                Iflag = ln[31]
                if Iflag == ' ':
                    Iflag = 0
                else:
                    Iflag = int(Iflag)
                cur_header['Iflag'] = Iflag

                cur_header['element'] = Elements[Z-1]
                cur_header['atomic_number'] = Z
                cur_header['mass_number'] = A
                cur_header['atomic_mass'] = Aw
                cur_header['incoming_particle'] = particle_map[Yi]
                cur_header['incoming_particle_value'] = Yi
                cur_header['outgoing_particle'] = particle_map[Yo]
                cur_header['outgoing_particle_value'] = Yo
                cur_header['interpolation'] = interpolation_map[Iflag]
            elif ln == BREAK_TOKEN:
                in_section = False
            else:
                # get function to process rows of this type
                proc_func = reaction_property_funcs.get(
                    cur_header['I'], lambda h, row: list(row))
                # parse the fixed with data to floats
                row = [_fixed_width_float(ln[j*11:(j+1)*11])
                       for j in range(len(ln) // 11)]
                # generate final result representation
                ret_data[current_key].append(proc_func(cur_header, row))
        return ret_header, ret_data

if __name__ == '__main__':
    try:
        import argparse
    except ImportError:
        raise RuntimeError(
            'argparse module not found.\n'
            'Install argparse or update to python-2.7 or >=python-3.2.'
            )
    parser = argparse.ArgumentParser(
        description='export the Elam, Waasmaier, Chantler data to an SQLite database "dest"'
        )
    dest = 'xraydb.sqlite'
    parser.add_argument('-f', '--force', action='store_true')
    parser.add_argument('-s', '--silent', action='store_true')
    args = parser.parse_args()

    add_Elam(dest, overwrite=args.force, silent=args.silent)
    add_Waasmaier(dest, append=True)
    add_elementaldata(dest)
    add_ionization_potentials(dest)
    add_compton_energies(dest)
    add_corehole_data(dest, append=True)
    add_Chantler(dest, table='Chantler',        subdir='fine',   append=True)
    add_Version(dest)

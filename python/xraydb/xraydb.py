#!/usr/bin/env python
"""
SQLAlchemy wrapping of x-ray database for data from
     Elam et al, Chantler et al, Waasmaier and Kirfel

Main Class for full Database:  xrayDB
"""

import os
import json
from collections import namedtuple
import numpy as np
from scipy.interpolate import UnivariateSpline
from packaging.version import parse as version_parse

import sqlalchemy
from sqlalchemy.orm import sessionmaker

from .utils import elam_spline, as_ndarray
from .version import __version__

XrayEdge = namedtuple('XrayEdge', ('energy', 'fyield', 'jump_ratio'))
XrayLine = namedtuple('XrayLine', ('energy', 'intensity', 'initial_level',
                                   'final_level'))
ElementData = namedtuple('ElementData', ('Z', 'symbol', 'name', 'mass', 'density'))
ComptonEnergies = namedtuple('ComptonEnergies', ('incident', 'xray_90deg', 'xray_mean', 'electron_mean'))



def make_engine(dbname):
    "create engine for sqlite connection, perhaps trying a few sqlachemy variants"
    return sqlalchemy.create_engine(f'sqlite:///{dbname}')

def isxrayDB(dbname):
    """whether a file is a valid XrayDB database

    Args:
        dbname (string): name of XrayDB file

    Returns:
        bool: is file a valid XrayDB

    Notes:
      1. must be a sqlite db file, with tables named 'elements',
        'photoabsorption', 'scattering', 'xray_levels', 'Coster_Kronig',
        'Chantler', 'Waasmaier', and 'KeskiRahkonen_Krause'
    """
    _tables = ('Chantler', 'Waasmaier', 'Coster_Kronig',
               'KeskiRahkonen_Krause', 'xray_levels', 'elements',
               'photoabsorption', 'scattering')
    result = False
    try:
        engine = make_engine(dbname)
        meta = sqlalchemy.MetaData()
        meta.reflect(engine)
        result = all([t in meta.tables for t in _tables])
    except:
        pass
    return result


class XrayDB():
    """
    Database of Atomic and X-ray Data

    This XrayDB object gives methods to access the Atomic and
    X-ray data in th SQLite3 database xraydb.sqlite.

    Much of the data in this database comes from the compilation
    of Elam, Ravel, and Sieber, with additional data from Chantler,
    and other sources. See the documention and bibliography for
    a complete listing.
    """

    def __init__(self, dbname='xraydb.sqlite', read_only=True):
        "connect to an existing database"
        if not os.path.exists(dbname):
            parent, _ = os.path.split(__file__)
            dbname = os.path.join(parent, dbname)
            if not os.path.exists(dbname):
                raise IOError("Database '%s' not found!" % dbname)

        if not isxrayDB(dbname):
            raise ValueError("'%s' is not a valid X-ray Database file!" % dbname)
        self._cache = {}
        self.dbname = os.path.abspath(dbname)
        self.engine = make_engine(dbname)
        self.conn = self.engine.connect()
        kwargs = {}
        if read_only:
            kwargs = {'autoflush': True, 'autocommit': False}

            def readonly_flush(*args, **kwargs):
                return

            self.session = sessionmaker(self.engine, **kwargs)()
            self.session.flush = readonly_flush
        else:
            self.session = sessionmaker(bind=self.engine, **kwargs)()

        self.metadata = sqlalchemy.MetaData()
        self.metadata.reflect(self.engine)
        self.tables = self.metadata.tables

        elems = self.get_cache('elements')
        self.__atomic_symbols = [e.element for e in elems]
        self.__atomic_names = [e.name for e in elems]

    def close(self):
        "close session"
        self.session.flush()
        self.session.close()

    def query(self, *args, **kws):
        "generic query"
        return self.session.query(*args, **kws)

    def get_cache(self, tablename, column=None, value=None):
        """for some tables, we will just cache all the data"""
        if column is None:
            if tablename in self._cache:
                rows = self._cache[tablename]
            else:
                q = self.tables[tablename].select()
                rows = self.session.execute(q).fetchall()
                self._cache[tablename] = rows
                # print("cached ", tablename)
        else:
            if tablename in self._cache:
                data = self._cache[tablename]
            else:
                data = self._cache[tablename] = {}

            key = f"{column:s}_{repr(value)}"
            if key not in data:
                tab = self.tables[tablename]
                col = getattr(tab.c, column, None)
                if col is None:
                    raise ValueError(f"now column {column} for table {tablename}")
                data[key] = self.query(tab).filter(col==value).all()
                # print("cached ", tablename, key)
            if key in data:
                rows = data[key]
        return rows


    def get_version(self, long=False, with_history=False):
        """
        return sqlite3 database and python library version numbers

        Parameters:
            long (bool): show timestamp and notes of latest version [False]
            with_history (bool): show complete version history [False]

        Returns:
            string: version information
        """
        out = []
        rows = self.get_cache('Version')
        if not with_history:
            rows = rows[-1:]
        if long or with_history:
            for row in rows:
                out.append("XrayDB Version: %s [%s] '%s'" % (row.tag,
                                                             row.date,
                                                             row.notes))
            out.append("Python Version: %s" % __version__)
            out = "\n".join(out)
        else:
            out = "XrayDB Version: %s, Python Version: %s" % (rows[0].tag,
                                                              __version__)
        return out

    def f0_ions(self, element=None):
        """
        return list of ion names supported for the .f0() function.


        Parameters:
            element (string, int, pr None):  atomic number, symbol, or ionic symbol
                    of scattering element.

        Returns:
            list:  if element is None, all 211 ions are returned.
                   if element is not None, the ions for that element are returned

        Example:
            >>> xdb = XrayDB()
            >>> xdb.f0_ions('Fe')
            ['Fe', 'Fe2+', 'Fe3+']

        Notes:
            Z values from 1 to 98 (and symbols 'H' to 'Cf') are supported.

        References:
            Waasmaier and Kirfel
        """
        rows = self.get_cache('Waasmaier')
        if element is not None:
            rows = [r for r in rows if r.element==element]
        return [str(r.ion) for r in rows]

    def f0(self, ion, q):
        """
        return f0(q) -- elastic X-ray scattering factor from Waasmaier and Kirfel

        Parameters:
            ion (string, int, or None):  atomic number, symbol or ionic symbol
                  of scattering element.
            q (float, list, ndarray): value(s) of q for scattering factors

        Returns:
            ndarray: elastic scattering factors


        Example:
            >>> xdb = XrayDB()
            >>> xdb.f0('Fe', range(10))
            array([ 25.994603  ,   6.55945765,   3.21048827,   1.65112769,
                     1.21133507,   1.0035555 ,   0.81012185,   0.61900285,
                     0.43883403,   0.27673021])

        Notes:
            q = sin(theta) / lambda, where theta = incident angle,
            and lambda = X-ray wavelength

            Z values from 1 to 98 (and symbols 'H' to 'Cf') are supported.
            The list of ionic symbols can be read with the function .f0_ions()

        References:
            Waasmaier and Kirfel
        """
        f0_rows = self.get_cache('Waasmaier')
        row = [None]
        if isinstance(ion, int):
            rows = [r for r in f0_rows if ion == r.atomic_number]
            if len(rows) == 0:
                raise ValueError(f'No ion {ion} from Waasmaier table')
        else:
            rows = [r for r in f0_rows if ion.title() == r.ion]
            if len(rows) == 0:
                raise ValueError(f'No ion {ion} from Waasmaier table')
        row = rows[0]
        q = as_ndarray(q)
        f0 = row.offset
        for s, e in zip(json.loads(row.scale), json.loads(row.exponents)):
            f0 += s * np.exp(-e*q*q)
        return f0

    def _from_chantler(self, element, energy, column='f1', smoothing=0):
        """
        return energy-dependent data from Chantler table

        Parameters:
            element (string or int): atomic number or symbol.
            eneregy (float or ndarray):
        columns: f1, f2, mu_photo, mu_incoh, mu_total

        Notes:
           this function is meant for internal use.
        """
        elem = self.symbol(element)
        energy = as_ndarray(energy)
        emin, emax = min(energy), max(energy)

        row = self.get_cache('Chantler', column='element', value=elem)[0]

        te = np.array(json.loads(row.energy))
        nemin = max(0, -3 + max(np.where(te <= emin)[0]))
        nemax = min(len(te), 3 + max(np.where(te <= emax)[0]))

        te = te[nemin:nemax+1]
        if column == 'mu':
            column = 'mu_total'
        ty = np.array(json.loads(getattr(row, column)))[nemin:nemax+1]
        ty[np.where(abs(ty) < 1.e-99)] =  1.e-99
        if column == 'f1':
            out = UnivariateSpline(te, ty, s=smoothing)(energy)
        else:
            out = np.exp(np.interp(np.log(energy),
                                   np.log(te),
                                   np.log(ty)))
        if isinstance(out, np.ndarray) and len(out) == 1:
            out = out[0]
        return out

    def chantler_energies(self, element, emin=0, emax=1.e9):
        """
        return array of energies (in eV) at which data is
        tabulated in the Chantler tables for a particular element.

        Parameters:
            element (string or int): atomic number or symbol
            emin (float): minimum energy (in eV) [0]
            emax (float): maximum energy (in eV) [1.e9]

        Returns:
            ndarray: energies

        References:
            Chantler

        Notes:
            returns 2 energies below emin and above emax to better
            enable interpolation
        """
        ctab = self.tables['Chantler']
        elem = self.symbol(element)
        row = self.query(ctab).filter(ctab.c.element == elem).one()
        te = np.array(json.loads(row.energy))

        if emin <= min(te):
            nemin = 0
        else:
            nemin = max(0, -1 + max(np.where(te <= emin)[0]))
        if emax > max(te):
            nemax = len(te)
        else:
            nemax = min(len(te), 2 + max(np.where(te <= emax)[0]))
        return te[nemin:nemax+1]

    def f1_chantler(self, element, energy, **kws):
        """
        returns f1 -- real part of anomalous X-ray scattering factor
        for selected input energy (or energies) in eV.

        Parameters:
            element (string or int): atomic number or symbol
            energy (float or ndarray): energies (in eV).

        Returns:
            ndarray: real part of anomalous scattering factor

        References:
            Chantler
        """
        return self._from_chantler(element, energy, column='f1', **kws)

    def f2_chantler(self, element, energy, **kws):
        """
        returns f2 -- imaginary part of anomalous X-ray scattering factor
        for selected input energy (or energies) in eV.

        Parameters:
            element (string or int): atomic number or symbol
            energy (float or ndarray): energies (in eV).

        Returns:
            ndarray: imaginary part of anomalous scattering factor

        References:
            Chantler
        """
        return self._from_chantler(element, energy, column='f2', **kws)

    def mu_chantler(self, element, energy, incoh=False, photo=False):
        """
        returns X-ray mass attenuation coefficient, mu/rho in cm^2/gr
        for selected input energy (or energies) in eV.
        default is to return total attenuation coefficient.

        Parameters:
            element (string or int): atomic number or symbol
            energy (float or ndarray): energies (in eV).
            photo (bool): return only the photo-electric contribution [False]
            incoh (bool): return only the incoherent contribution [False]

        Returns:
            ndarray: mass attenuation coefficient in cm^2/gr

        References:
            Chantler
        """
        col = 'mu_total'
        if photo:
            col = 'mu_photo'
        elif incoh:
            col = 'mu_incoh'
        return self._from_chantler(element, energy, column=col)

    def compton_energies(self, incident_energy):
        """
        return tuple of Compton energies for an incident energy
        """
        row = self.get_cache('Compton_energies')[0]
        _en   = json.loads(row.incident)
        _xe90 = json.loads(row.xray_90deg)
        _xave = json.loads(row.xray_mean)
        _eave = json.loads(row.electron_mean)

        xray_90deg = np.interp(incident_energy, _en, _xe90)
        xray_mean = np.interp(incident_energy, _en, _xave)
        electron_mean = np.interp(incident_energy, _en, _eave)

        return ComptonEnergies(incident_energy, xray_90deg, xray_mean, electron_mean)

    def _elem_data(self, element):
        "return data from elements table: internal use"

        rows = self.get_cache('elements')
        if isinstance(element, int):
            row = [r for r in rows if r.atomic_number == element][0]
        else:
            if element.title() in self.__atomic_symbols:
                row = [r for r in rows if r.element == element.title()][0]
            elif element.lower() in self.__atomic_names:
                row = [r for r in rows if r.name == element.lower()][0]
            else:
                raise ValueError("unknown element '%s'" % repr(element))
        return ElementData(int(row.atomic_number),
                           row.element.title(), row.name,
                           row.molar_mass, row.density)

    def atomic_number(self, element):
        """
        return element's atomic number

        Parameters:
            element (string or int): atomic number or symbol

        Returns:
            integer: atomic number
        """
        return self._elem_data(element).Z

    def symbol(self, element):
        """
        return element symbol

        Parameters:
            element (string or int): atomic number or symbol

        Returns:
            string: element symbol
        """
        return self._elem_data(element).symbol

    def atomic_name(self, element):
        """
        return element's name (English)

        Parameters:
            element (string or int): atomic number or symbol

        Returns:
            string: element name
        """
        return self._elem_data(element).name

    def molar_mass(self, element):
        """
        return molar mass of element

        Parameters:
            element (string or int): atomic number or symbol

        Returns:
            float: molar mass of element in amu
        """
        return self._elem_data(element).mass

    def density(self, element):
        """
        return density of pure element

        Parameters:
            element (string or int): atomic number or symbol

        Returns:
            float: density of element in gr/cm^3
        """
        return self._elem_data(element).density

    def xray_edges(self, element):
        """
        returns dictionary of X-ray absorption edge energy (in eV),
        fluorescence yield, and jump ratio for an element.

        Parameters:
            element (string or int): atomic number or symbol

        Returns:
            dictionary:  keys of edge (iupac symbol), and values of
                         XrayEdge namedtuple of (energy, fyield, edge_jump)

        References:
           Elam, Ravel, and Sieber.
        """
        elem = self.symbol(element)
        ltab = self.tables['xray_levels']
        out = {}
        for r in self.query(ltab).filter(ltab.c.element == elem).all():
            out[str(r.iupac_symbol)] = XrayEdge(r.absorption_edge,
                                                r.fluorescence_yield,
                                                r.jump_ratio)
        return out

    def xray_edge(self, element, edge):
        """
        returns XrayEdge for an element and edge

        Parameters:
            element (string or int): atomic number or symbol
            edge (string):  X-ray edge

        Returns:
            XrayEdge:  namedtuple of (energy, fyield, edge_jump)

        Example:
            >>> xdb = XrayDB()
            >>> xdb.xray_edge('Co', 'K')
            XrayEdge(edge=7709.0, fyield=0.381903, jump_ratio=7.796)

        References:
           Elam, Ravel, and Sieber.
        """
        return self.xray_edges(element).get(edge.title(), None)

    def xray_lines(self, element, initial_level=None, excitation_energy=None):
        """
        returns dictionary of X-ray emission lines of an element, with

        Parameters:
            initial_level (string or list/tuple of string):  initial level(s) to
                 limit output.
            excitation_energy (float): energy of excitation, limit output those
                 excited by X-rays of this energy (in eV).

        Returns:
            dictionary: keys of lines (Siegbahn symbol), values of Xray Lines

        Notes:
            if both excitation_energy and initial_level are given, excitation_level
            will limit output

        Example:
            >>> xdb = XrayDB()
            >>> for key, val in xdb.xray_lines('Ga', 'K').items():
            >>>      print(key, val)
            'Ka3', XrayLine(energy=9068.0, intensity=0.000326203,
                            initial_level=u'K', final_level=u'L1')
            'Ka2', XrayLine(energy=9223.8, intensity=0.294438,
                            initial_level=u'K', final_level=u'L2')
            'Ka1', XrayLine(energy=9250.6, intensity=0.57501,
                            initial_level=u'K', final_level=u'L3')
            'Kb3', XrayLine(energy=10263.5, intensity=0.0441511,
                            initial_level=u'K', final_level=u'M2')
            'Kb1', XrayLine(energy=10267.0, intensity=0.0852337,
                            initial_level=u'K', final_level=u'M3')
            'Kb5', XrayLine(energy=10348.3, intensity=0.000841354,
                            initial_level=u'K', final_level=u'M4,5')

        References:
           Elam, Ravel, and Sieber.
        """
        elem = self.symbol(element)
        ttab = self.tables['xray_transitions']
        row = self.query(ttab).filter(ttab.c.element == elem)
        if excitation_energy is not None:
            initial_level = []
            for ilevel, dat in self.xray_edges(elem).items():
                if dat[0] < excitation_energy:
                    initial_level.append(ilevel.title())

        if initial_level is not None:
            if isinstance(initial_level, (list, tuple)):
                row = row.filter(ttab.c.initial_level.in_(initial_level))
            else:
                row = row.filter(ttab.c.initial_level == initial_level.title())
        out = {}
        for r in row.all():
            out[str(r.siegbahn_symbol)] = XrayLine(r.emission_energy, r.intensity,
                                                   r.initial_level, r.final_level)
        return out

    def xray_line_strengths(self, element, excitation_energy=None):
        """
        return the absolute line strength in cm^2/gr for all available lines

        Parameters:
            element (string or int): Atomic symbol or number for element
            excitation_energy (float): incident energy, in eV

        Returns:
            dictionary: elemental line with fluorescence cross section in cm2/gr.

        References:
           Elam, Ravel, and Sieber.
        """
        out = {}
        lines = self.xray_lines(element, excitation_energy=excitation_energy)
        for label, eline in lines.items():
            edge = self.xray_edge(element, eline.initial_level)
            if edge is None and ',' in eline.initial_level:
                ilevel, _ = eline.initial_level.split(',')
                edge = self.xray_edge(element, ilevel)
            if edge is not None:
                mu = self.mu_elam(element, [edge.energy*(0.999),
                                            edge.energy*(1.001)], kind='photo')
                out[label] = (mu[1]-mu[0]) * eline.intensity * edge.fyield
        return out

    def ck_probability(self, element, initial, final, total=True):
        """
        return Coster-Kronig transition probability for an element and
        initial/final levels

        Parameters:
            element (string or int): Atomic symbol or number for element
            initial (string):  initial level
            final (string):  final level
            total (bool): whether to return total or partial probability

        Returns:
            float: transition probability

        Example:
            >>> xdb = XrayDB()
            >>> xdb.ck_probability('Cu', 'L1', 'L3', total=True)
            0.681

        References:
           Elam, Ravel, and Sieber.
        """
        elem = self.symbol(element)
        ctab = self.tables['Coster_Kronig']

        row = self.query(ctab).filter(ctab.c.element == elem)
        row = row.filter(ctab.c.initial_level == initial.title())
        row = row.filter(ctab.c.final_level == final.title()).all()
        out = 0.0
        if len(row) > 0:
            row = row[0]
            out = row.transition_probability
            if total:
                out = row.total_transition_probability
        return out

    def corehole_width(self, element, edge=None, use_keski=False):
        """
        returns core hole width for an element and edge

        Parameters:
            element (string, integer): atomic number or symbol for element
            edge (string or None): edge for hole, return all if None
            use_keski (bool) : force use of KeskiRahkonen and Krause table for all data.

        Returns:
            a dict of ``{edge: core_hole_width}`` if the edge is not specified
            or a float with the core hole width for a specified edge.

        Notes:
            Uses Krause and Oliver where data is available (K, L lines Z > 10)
            Uses Keski-Rahkonen and Krause otherwise
            Values are in eV.

        References:
            Krause and Oliver, 1979
            Keski-Rahkonen and Krause, 1974

        """
        version_qy = self.tables['Version'].select().order_by('date')
        version_id = self.session.execute(version_qy).fetchall()[-1].id

        ctab = self.tables['corelevel_widths']
        if version_id < 4 or use_keski:
            ctab = self.tables['KeskiRahkonen_Krause']

        rows = self.query(ctab).filter(ctab.c.element == self.symbol(element))
        if edge is not None:
            rows = rows.filter(ctab.c.edge == edge.title())

        result = {r.edge: r.width for r in rows.all()}
        if edge is not None:
            result = result[edge]
        return result


    def cross_section_elam(self, element, energies, kind='photo'):
        """
        returns Elam Cross Section values for an element and energies

        Parameters:
            element (string or int):  atomic number or symbol for element
            energies (float or ndarray): energies (in eV) to calculate cross-sections
            kind (string):  one of 'photo', 'coh', and 'incoh' for photo-absorption,
                  coherent scattering, and incoherent scattering cross sections,
                  respectively. Default is 'photo'.

        Returns:
            ndarray of scattering data

        References:
            Elam, Ravel, and Sieber.
        """
        elem = self.symbol(element)
        kind = kind.lower()
        if kind not in ('coh', 'incoh', 'photo'):
            raise ValueError('unknown cross section kind=%s' % kind)

        tablename = 'photoabsorption' if kind == 'photo' else 'scattering'

        row = self.get_cache(tablename, column='element', value=elem)[0]

        tab_lne = np.array(json.loads(row.log_energy))
        if kind.startswith('coh'):
            tab_val = np.array(json.loads(row.log_coherent_scatter))
            tab_spl = np.array(json.loads(row.log_coherent_scatter_spline))
        elif kind.startswith('incoh'):
            tab_val = np.array(json.loads(row.log_incoherent_scatter))
            tab_spl = np.array(json.loads(row.log_incoherent_scatter_spline))
        else:
            tab_val = np.array(json.loads(row.log_photoabsorption))
            tab_spl = np.array(json.loads(row.log_photoabsorption_spline))

        en = 1.0*as_ndarray(energies)
        emin_tab = 10*int(0.102*np.exp(tab_lne[0]))
        en[np.where(en < emin_tab)] = emin_tab
        out = np.exp(elam_spline(tab_lne, tab_val, tab_spl, np.log(en)))

        if isinstance(energies, (int, float)):
            return out[0]

        return out

    def mu_elam(self, element, energies, kind='total'):
        """
        returns attenuation cross section for an element at energies (in eV)

        Parameters:
            element (string or int):  atomic number or symbol for element
            energies (float or ndarray): energies (in eV) to calculate cross-sections
            kind (string):  one of 'photo' or 'total' for photo-electric or
                  total attenuation, respectively.  Default is 'total'.

        Returns:
           ndarray of scattering values in units of cm^2/gr

        References:
            Elam, Ravel, and Sieber.
        """
        calc = self.cross_section_elam
        kind = kind.lower()
        if kind.startswith('tot'):
            xsec = calc(element, energies, kind='photo')
            xsec += calc(element, energies, kind='coh')
            xsec += calc(element, energies, kind='incoh')
        elif kind.startswith('photo'):
            xsec = calc(element, energies, kind='photo')
        elif kind.lower().startswith('coh'):
            xsec = calc(element, energies, kind='coh')
        elif kind.lower().startswith('incoh'):
            xsec = calc(element, energies, kind='incoh')
        else:
            raise ValueError('unknown cross section kind=%s' % kind)
        return xsec

    def coherent_cross_section_elam(self, element, energies):
        """returns coherenet scattering crossrxr section for an element
        at energies (in eV)

        returns values in units of cm^2 / gr

        arguments
        ---------
        element:  atomic number, atomic symbol for element
        energies: energies in eV to calculate cross-sections

        Data from Elam, Ravel, and Sieber.
        """
        return self.cross_section_elam(element, energies, kind='coh')

    def incoherent_cross_section_elam(self, element, energies):
        """return incoherenet scattering cross section for an element
        at energies (in eV)

        returns values in units of cm^2 / gr

        arguments
        ---------
        element:  atomic number, atomic symbol for element
        energies: energies in eV to calculate cross-sections

        Data from Elam, Ravel, and Sieber.
        """
        return self.cross_section_elam(element, energies, kind='incoh')

    def ionization_potential(self, gas):
        """return effective ionization potential for a gas,
        as appropriate for ionization chambers in the linear
        regime (not in the 'proportional counter' regime)

        returns values in units of eV

        argument
        ---------
        gas (string):  name of gas

        notes
        -----
        Data from G. F. Knoll, Radiation Detection and Measurement, Table 5-1.
        """
        itab = self.tables['ionization_potentials']
        out = self.query(itab).filter(itab.c.gas == gas).all()
        if len(out) != 1:
            raise ValueError('unknown gas for ionization potential: %s' % gas)
        return float(out[0].potential)

import os
import numpy as np
from .chemparser import chemparse
from .xray import mu_elam, atomic_mass
from .utils import get_homedir

_materials = None

def get_user_materialsfile():
    """return name for user-specific materials.dat file
    With $HOME being the users home directory, this will be
    $HOME/.config/xraydb/materials.dat
    """
    return os.path.join(get_homedir(), '.config', 'xraydb', 'materials.dat')

def _read_materials_db():
    """return _materials dictionary, creating it if needed"""
    global _materials
    if _materials is None:
        # initialize materials table
        _materials = {}

        def read_materialsfile(fname):
            with open(fname, 'r') as fh:
                lines = fh.readlines()
            for line in lines:
                line = line.strip()
                if len(line) > 2 and not line.startswith('#'):
                    try:
                        name, f, den = [i.strip() for i in line.split('|')]
                        name = name.lower()
                        _materials[name] = (f.replace(' ', ''), float(den))
                    except:
                        pass

        # first, read from standard list
        local_dir, _ = os.path.split(__file__)
        fname = os.path.join(local_dir, 'materials.dat')
        if os.path.exists(fname):
            read_materialsfile(fname)

        # next, read from users materials file
        fname = get_user_materialsfile()
        if os.path.exists(fname):
            read_materialsfile(fname)
    return _materials

def material_mu(name, energy, density=None, kind='total'):
    """X-ray attenuation length (in 1/cm) for a material by name or formula

    Args:
        name (str): chemical formul or name of material from materials list.
        energy (float or ndarray):   energy or array of energies in eV
        density (None or float):  material density (gr/cm^3).
        kind (str):  'photo' or 'total'for whether to
                  return photo-absorption or total cross-section ['total']
    Returns:
        absorption length in 1/cm

    Notes:
        1.  material names are not case sensitive,
            chemical compounds are case sensitive.
        2.  mu_elam() is used for mu calculation.
        3.  if density is None and material is known, that density will be used.


    Examples:
        >>> material_mu('H2O', 10000.0)
        5.32986401658495
    """
    global _materials
    if _materials is None:
        _materials = _read_materials_db()
    formula = None
    _density  = None
    mater = _materials.get(name.lower(), None)
    if mater is not None:
        formula, _density = mater
    else:
        for key, val in _materials.items():
            if name.lower() == val[0].lower(): # match formula
                formula, _density = val
                break
    # default to using passed in name as a formula
    if formula is None:
        formula = name
    if density is None:
        density = _density
    if density is None:
        raise Warning('material_mu(): must give density for unknown materials')

    mass_tot, mu = 0.0, 0.0
    for elem, frac in chemparse(formula).items():
        mass  = frac * atomic_mass(elem)
        mu   += mass * mu_elam(elem, energy, kind=kind)
        mass_tot += mass
    return density*mu/mass_tot


def material_mu_components(name, energy, density=None, kind='total'):
    """material_mu_components: absorption coefficient (in 1/cm) for a compound

    Args:
        name (str): chemical formul or name of material from materials list.
        energy (float or ndarray):   energy or array of energies in eV
        density (None or float):  material density (gr/cm^3).
        kind (str):  'photo' or 'total'for whether to
                  return photo-absorption or total cross-section ['total']

    Returns:
        dict for constructing mu per element,
        with elements 'mass' (total mass), 'density', and
       'elements' (list of atomic symbols for elements in material).
        For each element, there will be an item (atomic symbol as key)
        with tuple of (stoichiometric fraction, atomic mass, mu)

    Examples:
        >>> xraydb.material_mu('quartz', 10000)
        50.36774553547068
        >>> xraydb.material_mu_components('quartz', 10000)
        {'mass': 60.0843, 'density': 2.65, 'elements': ['Si', 'O'],
        'Si': (1, 28.0855, 33.87943243018506), 'O': (2.0, 15.9994, 5.952824815297084)}
     """
    global _materials
    if _materials is None:
        _materials = _read_materials_db()
    mater = _materials.get(name.lower(), None)
    if mater is None:
        formula = name
        if density is None:
            raise Warning('material_mu(): must give density for unknown materials')
    else:
        formula, density = mater


    out = {'mass': 0.0, 'density': density, 'elements':[]}
    for atom, frac in chemparse(formula).items():
        mass  = atomic_mass(atom)
        mu    = mu_elam(atom, energy, kind=kind)
        out['mass'] += frac*mass
        out[atom] = (frac, mass, mu)
        out['elements'].append(atom)
    return out

def get_material(name):
    """look up material name

    Args:
        name (str): name of material

    Returns:
        chemical formula, denisty of material

    Examples:
        >>> xraydb.get_material('kapton')
        ('C22H10N2O5', 1.43)

    """
    global _materials
    if _materials is None:
        _materials = _read_materials_db()

    return _materials.get(name.lower(), None)


def add_material(name, formula, density):
    """add a material to the users local material database

    Args:
        name (str): name of material
        formula (str): chemical formula
        density (float: density

    Returns:
        None

    Notes:
        the data will be saved to $HOME/.config/xraydb/materials.dat
        in the users home directory, and wiill be useful in subsequent sessions.

    Examples:
        >>> xraydb.add_material('becopper', 'Cu0.98e0.02', 8.3)

    """
    global _materials
    if _materials is not None:
        _materials = _read_materials_db()
    formula = formula.replace(' ', '')
    _materials[name.lower()] = (formula, float(density))

    fname = get_user_materialsfile()

    if os.path.exists(fname):
        fh = open(fname, 'r')
        text = fh.readlines()
        fh.close()
    else:
        parent, _ = os.path.split(fname)
        if not os.path.exists(parent):
            try:
                os.makedirs(parent)
            except FileExistsError:
                pass
        text = ['# user-specific database of materials\n',
                '# name, formula, density\n']

    text.append(" %s | %s | %g\n" % (name, formula, density))

    with open(fname, 'w') as fh:
        fh.write(''.join(text))

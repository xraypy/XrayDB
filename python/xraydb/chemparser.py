#!/usr/bin/env python
#
# Chemical Formula Parser:
#
#  returns dictionary of total atomic composition
#  supports floats for complex stoichiometries
#
#    >>>> from xraydb import chemparse
#    >>> chemparse('H2O')
#    {'H': 2.0, 'O': 0}
#    >>> chempars('Mn(SO4)2(H2O)7)')
#    {'H': 14.0, 'S': 2.0, 'Mn': 1, 'O': 15.0}
#    >>> chemparse('Zn1.e-5Fe3O4')
#    {'Zn': 1e-05, 'Fe': 3.0, 'O': 4.0}
#
# based (heavily) on chemical formula parser from Tim Peters
# modified (simplified to not compute molecular weights here,
# extended to support floating point, made into Parser class)
#   Matt Newville  Univ Chicago  Jan-2013
#

from re import compile as re_compile
class Element:
    def __init__(self, symbol):
        self.sym = symbol

    def add(self, weight, result):
        result[self.sym] = result.get(self.sym, 0) + weight

LEXER = re_compile(r"[A-Z][a-z]*|[0-9]+\.?[0-9]*([eE][-+]?[0-9]+)?|[()]|<EOS>").match
NAME, NUM, LPAREN, RPAREN, EOS = range(5)
BADSYM = "'{:s}' is not an element symbol"

ELEMENTS = {}
for sym in ('Ac', 'Ag', 'Al', 'Am', 'Ar', 'As', 'At', 'Au', 'B', 'Ba', 'Be',
       'Bi', 'Bk', 'Br', 'C', 'Ca', 'Cd', 'Ce', 'Cf', 'Cl', 'Cm', 'Co',
       'Cr', 'Cs', 'Cu', 'Dy', 'Er', 'Es', 'Eu', 'F', 'Fe', 'Fm', 'Fr',
       'Ga', 'Gd', 'Ge', 'H', 'He', 'Hf', 'Hg', 'Ho', 'I', 'In', 'Ir', 'K',
       'Kr', 'La', 'Li', 'Lr', 'Lu', 'Md', 'Mg', 'Mn', 'Mo', 'N', 'Na',
       'Nb', 'Nd', 'Ne', 'Ni', 'No', 'Np', 'O', 'Os', 'P', 'Pa', 'Pb',
       'Pd', 'Pm', 'Po', 'Pr', 'Pt', 'Pu', 'Ra', 'Rb', 'Re', 'Rh', 'Rn',
       'Ru', 'S', 'Sb', 'Sc', 'Se', 'Si', 'Sm', 'Sn', 'Sr', 'Ta', 'Tb',
       'Tc', 'Te', 'Th', 'Ti', 'Tl', 'Tm', 'U', 'Unh', 'Unp', 'Unq', 'Uns',
       'V', 'W', 'Xe', 'Y', 'Yb', 'Zn', 'Zr'):
    ELEMENTS[sym]  = Element(sym)

class ElementSequence:
    def __init__(self, *seq):
        self.seq = list(seq)
        self.count = 1

    def append(self, thing):
        self.seq.append(thing)

    def set_count(self, n):
        self.count = n

    def __len__(self):
        return len(self.seq)

    def add(self, weight, result):
        totalweight = weight * self.count
        for thing in self.seq:
            thing.add(totalweight, result)

class Tokenizer:
    def __init__(self, input):
        self.input = input + "<EOS>"
        self.i = 0
        self.ttype = None
        self.tvalue = None

    def gettoken(self):
        self.lasti = self.i
        m = LEXER(self.input, self.i)
        if m is None:
            self.error("unrecognized element or number")
        self.i = m.end()
        self.tvalue = m.group()
        if self.tvalue == "(":
            self.ttype = LPAREN
        elif self.tvalue == ")":
            self.ttype = RPAREN
        elif self.tvalue == "<EOS>":
            self.ttype = EOS
        elif "0" <= self.tvalue[0] <= "9":
            self.ttype = NUM
            self.tvalue = float(self.tvalue)
        else:
            self.ttype = NAME

    def error(self, msg):
        emsg = msg + ":\n"
        emsg = emsg + self.input[:-5] + "\n"  # strip <EOS>
        emsg = emsg + " " * self.lasti + "^\n"
        raise ValueError(emsg)

class ChemFormulaParser(object):
    def __init__(self, formula=None):
        self.formula = formula

    def parse(self, formula=None):
        if formula is not None:
            self.formula = formula
        self.tok = Tokenizer(formula)
        self.tok.gettoken()
        seq = self.parse_sequence()
        if self.tok.ttype != EOS:
            self.tok.error("expected end of input")

        out = {}
        seq.add(1, out)
        return out

    def parse_sequence(self):
        seq = ElementSequence()
        while self.tok.ttype in (LPAREN, NAME):
            # parenthesized expression or straight name
            if self.tok.ttype == LPAREN:
                self.tok.gettoken()
                thisseq = self.parse_sequence()
                if self.tok.ttype != RPAREN:
                    self.tok.error("expected right paren")
                self.tok.gettoken()
            else:
                assert self.tok.ttype == NAME
                if self.tok.tvalue in ELEMENTS:
                    thisseq = ElementSequence(ELEMENTS[self.tok.tvalue])
                else:
                    self.tok.error(BADSYM.format(self.tok.tvalue))
                self.tok.gettoken()
            # followed by optional count
            if self.tok.ttype == NUM:
                thisseq.set_count(self.tok.tvalue)
                self.tok.gettoken()
            seq.append(thisseq)
            if len(seq) == 0:
                self.tok.error("empty sequence")
        return seq

def chemparse(formula):
    '''parse a chemical formula to a dictionary of elemental abundances

    Args:
        formula (str): chemical formula

    Returns:
        dict of element symbol and abundance.

    Examples:
        >>> from xraydb import chemparse
        >>> chemparse('Mn(SO4)2(H2O)7)')
        {'H': 14.0, 'S': 2.0, 'Mn': 1, 'O': 15.0}

        >>> chemparse('Zn1.e-5Fe3O4')
        {'Zn': 1e-05, 'Fe': 3.0, 'O': 4.0}

        >>> chemparse('CO')
        {'C': 1, 'O': 1}
        >>> chemparse('Co')
        {'Co': 1}

        >>> chemparse('co')
        ValueError: unrecognized element or number:
        co
    '''
    return ChemFormulaParser().parse(formula)

def validate_formula(formula):
    '''return whether a chemical formula is valid and
    can be parsed to a dictionary with chemparse()

    Args:
        formula (str): chemical formula

    Returns:
        bool (True or False) for whether chemparse() will succeed

    Examples:
        >>> from xraydb import validate_formula
        >>> validate_formula('Mn(SO4)2(H2O)7)')
        True

        >>> validate_formula('Mn(SO4)2(H2O7')
        False

        >>> validate_formula('Z')
        False

    '''
    try:
        t = chemparse(formula)
        return len(t) > 0
    except:
        return False

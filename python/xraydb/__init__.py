"""Python interface to XrayDB:

   X-ray Reference Data for the Elements

   last update: 30-August-2019
   License: Public Domain
   Author:  Matthew Newville <newville@cars.uchicago.edu>
            Center for Advanced Radiation Sources,
            The University of Chicago
"""
from .xraydb import XrayDB

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

#!/usr/bin/env python
import os
import sys
import shutil
from setuptools import setup
import versioneer

dbfile = 'xraydb.sqlite'
matfile = 'materials.dat'

dest_dbfile = os.path.join('xraydb', dbfile)
src_dbfile = os.path.join('..', dbfile)
if (not os.path.exists(dest_dbfile) and
    os.path.exists(src_dbfile)):
    shutil.copy(src_dbfile, dest_dbfile)

desc="X-ray Reference Data for the Elements using SQLite"

setup(name = 'xraydb',
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      author='Matthew Newville',
      author_email='newville@cars.uchicago.edu',
      url='http://github.com/xraypy/XrayDB',
      download_url='http://github.com/xrapy/XrayDB',
      license='public domain',
      description=desc,
      long_description=desc,
      platforms=('Windows', 'Linux', 'Mac OS X'),
      classifiers=['Intended Audience :: Science/Research',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Scientific/Engineering'],
      install_requires=('sqlalchemy', 'numpy', 'scipy'),
      package_dir={'xraydb': 'xraydb'},
      packages=['xraydb'],
      package_data={'xraydb': [dbfile, matfile]})

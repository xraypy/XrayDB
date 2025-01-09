[![DOI](https://zenodo.org/badge/205441660.svg)](https://zenodo.org/badge/latestdoi/205441660)


## XrayDB

X-ray Reference Data in SQLite library, including a Python interface.

The repository contains useful data about the intereactions of X-rays with
matter.  It packages these different data sources into a single sqlite3
database which can, in principle, be used by a very large number of
computer programming languages and environments.

The data and code here are placed in the Public Domain.

## Web interface

Web interfaces using XrayDB to display X-ray properties of the elements can be
found at

   https://xraydb.seescience.org/
   https://xraydb.xrayabsorption.org/

The code for this web interface is at https://github.com/xraypy/xrayweb

## Periodic Tables

Poster-sized Periodic Tables of X-ray energies built with XrayDB can be
downloaded from https://xraypy.github.io/XrayDB/periodictable.html

## About X-ray DB

The X-ray Scattering data from the Elam Tables was modified from code
originally written by Darren S. Dale.

Refined values for anomalous scattering factors have been provided directly
by Christopher T. Chantler.

The project has mostly been supported and maintained by Matt Newville.
Suggestions and conributions are most welcome.

Some history:
-------------

This project has moved around a bit.  Originally part of Larch
(https://xraypy.github.io/xraylarch/), and then
part of Scikit-Beam (https://github.com/scikit-beam/scikit-beam), the
XrayDB now has a permanent home here at (https://github.com/xraypy/XrayDB).

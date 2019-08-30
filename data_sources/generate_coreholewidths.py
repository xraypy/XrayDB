#!/usrb/bin/env python
"""writes Corehole_Widths.dat containing core hole wdith in eV
for element up to Z = 98 and K, L, M, and N edges.

Calculation uses data from O. Keski-Rahkonen and M. O. Krause,
Atomic Data and Nuclear Data Tables 14, #2, pages 139-146 (1974)

This uses the data (interpolated by hand from the graphs in the
above paper), and the calculation scheme from subroutine setgam
from Feff8.
"""

import numpy as np
from xraydb import xrayDB
xdb = xrayDB()

dat = {'K':  np.array([[0.99, 10.0, 20.0, 40.0, 50.0, 60.0, 80.0, 95.1],
                       [0.02,  0.28, 0.75, 4.8, 10.5, 21.0, 60.0, 105.0]]),
       'L1': np.array([[0.99, 18.0, 22.0, 35.0, 50.0, 52.0, 75.0, 95.1],
                       [0.07,  3.9,  3.8,  7.0, 6.0, 3.7, 8.0, 19.0]]),
       'L2': np.array([[0.99, 17.0, 28.0, 31.0, 45.0, 60.0, 80.0, 95.1],
                       [0.001, 0.12, 1.4,  0.8, 2.6, 4.1, 6.3, 10.5]]),
       'L3': np.array([[0.99, 17.0, 28.0, 31.0, 45.0, 60.0, 80.0, 95.1],
                       [0.001, 0.12, 0.55, 0.7, 2.1, 3.5, 5.4,  9.0]]),
       'M1': np.array([[0.99, 20.0, 28.0, 30.0, 36.0, 53.0, 80.0, 95.1],
                       [0.001, 1.0,  2.9,  2.2, 5.5, 10.0, 22.0, 22.0]]),
       'M2': np.array([[0.99, 20.0, 22.0, 30.0, 40.0, 68.0, 80.0, 95.1],
                       [0.001, 0.001, 0.5,  2.0, 2.6, 11.0, 15.0, 16.0]]),
       'M3': np.array([[0.99, 20.0, 22.0, 30.0, 40.0, 68.0, 80.0, 95.1],
                       [0.001, 0.001, 0.5,  2.0, 2.6, 11.0, 10.0, 10.0]]),
       'M4': np.array([[0.99, 36.0, 40.0, 48.0, 58.0, 76.0, 79.0, 95.1],
                       [0.0006, 0.09, 0.07, 0.48, 1.0, 4.0, 2.7,  4.7]]),
       'M5': np.array([[0.99, 36.0, 40.0, 48.0, 58.0, 76.0, 79.0, 95.1],
                       [0.0006, 0.09, 0.07, 0.48, 0.87, 2.2, 2.5,  4.3]]),
       'N1': np.array([[0.99, 30.0, 40.0, 47.0, 50.0, 63.0, 80.0, 95.1],
                       [0.001, 0.001, 6.2,  7.0, 3.2, 12.0, 16.0, 13.0]]),
       'N2': np.array([[0.99, 40.0, 42.0, 49.0, 54.0, 70.0, 87.0, 95.1],
                       [0.001, 0.001, 1.9, 16.0, 2.7, 13.0, 13.0,  8.0]]),
       'N3': np.array([[0.99, 40.0, 42.0, 49.0, 54.0, 70.0, 87.0, 95.1],
                       [0.001, 0.001, 1.9, 16.0, 2.7, 13.0, 13.0,  8.0]]),
       'N4': np.array([[0.99, 40.0, 50.0, 55.0, 60.0, 70.0, 81.0, 95.1],
                       [0.001, 0.001, 0.15, 0.1, 0.8, 8.0, 8.0,  5.0]]),
       'N5': np.array([[0.99, 40.0, 50.0, 55.0, 60.0, 70.0, 81.0, 95.1],
                       [0.001, 0.001, 0.15, 0.1, 0.8, 8.0, 8.0,  5.0]]),
       'N6': np.array([[0.99, 71.0, 73.0, 79.0, 86.0, 90.0, 95.0, 100.0],
                       [0.001, 0.001, 0.05, 0.22, 0.1, 0.16, 0.5,  0.9]]),
       'N7': np.array([[0.99, 71.0, 73.0, 79.0, 86.0, 90.0, 95.0, 100.0],
                       [0.001, 0.001, 0.05, 0.22, 0.1, 0.16, 0.5,  0.9]])
       }

buff = ['# core width data from Keski-Rahknonen and Krause (1974)\n',
        '# Z  Symbol  Edge  Core Width(eV)\n']
fmt   = " %2i    %2s    %2s      %.4f\n"
for z in range(1, 99):
    for edge in sorted(xdb.xray_edges(z).keys()):
        width = 0.1
        if edge in dat:
            width = 10**(np.interp(z, dat[edge][0], np.log10(dat[edge][1])))
        buff.append(fmt % (z, xdb.symbol(z), edge, width))

fout = open('keskirahkonen_krause.dat', 'w')
fout.write(''.join(buff))
fout.close()

## Notes:
## Feff8 uses the calc below.
##      gamh => dat[edge][1]
##      zh => dat[edge][0]
##      terp() with 4th argument = 1 does linear interpolation
##
#       zz = iz
#       if (ihole .le. 16)  then
#          do 10  i = 1, 8
#             gamkp(i) = log10 (gamh(i,ihole))
#             zk(i) = zh(i,ihole)
#    10    continue
#          call terp (zk, gamkp, 8, 1, zz, gamach)
#       else
# c     include data from the tables later.
# c     Now gamach=0.1eV for any O-hole for any element.
#          gamach = -1.0
#       endif
#
# c     Change from log10 (gamma) to gamma
#       gamach = 10.0 ** gamach


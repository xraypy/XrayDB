#!/usr/bin/env python
# XrayDB example script python/examples/mu_components_C.py
#
# plot components of X-ray mass attenuation for C 
#
import numpy as np
import matplotlib.pyplot as plt
from xraydb import mu_elam 

energy = np.arange(500, 120000, 10)  # energy in eV
      
elem = 'C'
mu_total = mu_elam(elem, energy, kind='total')
mu_photo = mu_elam(elem, energy, kind='photo')
mu_incoh = mu_elam(elem, energy, kind='incoh')
mu_coher = mu_elam(elem, energy, kind='coh')

plt.title('X-ray mass attenuation for %s' % elem)
plt.plot(energy, mu_total, linewidth=2, label='Total')
plt.plot(energy, mu_photo, linewidth=2, label='Photo-electric')
plt.plot(energy, mu_incoh, linewidth=2, label='Incoherent')
plt.plot(energy, mu_coher, linewidth=2, label='Coherent')

plt.xlabel('Energy (eV)')
plt.ylabel(r'$\mu/\rho \rm\, (cm^2/gr)$')
plt.legend()
plt.yscale('log')
plt.show()

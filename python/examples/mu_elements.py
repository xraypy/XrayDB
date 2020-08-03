#!/usr/bin/env python
# XrayDB example script python/examples/mu_elements.py
#
# plot X-ray mass attenuation for selected elements
#
import numpy as np
import matplotlib.pyplot as plt
import wxmplot.interactive as wi
from xraydb import mu_elam , atomic_symbol

energy = np.arange(500, 120000, 10)  # energy in eV
      
for elem in ('C', 'Cu', 'Au'):
    mu = mu_elam(elem, energy)
    plt.plot(energy, mu, label=elem, linewidth=2)
 
plt.title('X-ray mass attenuation')
plt.xlabel('Energy (eV)')
plt.ylabel(r'$\mu/\rho \rm\, (cm^2/gr)$')
plt.legend()
plt.yscale('log')
plt.xscale('log')
plt.show()

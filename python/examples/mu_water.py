#!/usr/bin/env python
# XrayDB example script    python/examples/mu_water.py
#
# calculate the fraction of X-rays transmitted through 1 mm of water
#
import numpy as np
import matplotlib.pyplot as plt

from xraydb import material_mu

energy = np.linspace(1000, 41000, 201)

mu = material_mu('H2O', energy)

# mu is returned in 1/cm
trans = np.exp(-0.1 * mu)

plt.plot(energy, trans, label='transmitted')
plt.plot(energy, 1-trans, label='attenuated')
plt.title('X-ray absorption by 1 mm of water')
plt.xlabel('Energy (eV)')
plt.ylabel('Transmitted / Attenuated fraction')
plt.legend()
plt.show()

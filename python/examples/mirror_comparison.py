import numpy as np
from xraydb import mirror_reflectivity
import matplotlib.pyplot as plt

energy = np.linspace(1000, 51000, 501)

r_si = mirror_reflectivity('Si', 0.002, energy)
r_ni = mirror_reflectivity('Ni', 0.002, energy)
r_rh = mirror_reflectivity('Rh', 0.002, energy)
r_pt = mirror_reflectivity('Pt', 0.002, energy)

plt.plot(energy, r_si, label='Si')
plt.plot(energy, r_ni, label='Ni')
plt.plot(energy, r_rh, label='Rh')
plt.plot(energy, r_pt, label='Pt')

plt.title('X-ray reflectivity at $\\theta=2 \mathrm{mrad}$')
plt.xlabel('Energy (eV)')
plt.ylabel('Reflectivity')
plt.legend()
plt.show()

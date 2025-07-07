import numpy as np
from xraydb import (coated_reflectivity, mirror_reflectivity)
import matplotlib.pyplot as plt

coating = 'Rh'
coating_thick = 300
substrate = 'Si'
theta = 0.004
energy = np.linspace(10000, 30000, 500)
binder = 'Cr'
binder_thick = 30

r = coated_reflectivity(coating, coating_thick, substrate, theta, energy, binder=binder, binder_thick=binder_thick)
r_Rh = mirror_reflectivity('Rh', theta, energy)

plt.plot(energy/1000, r, label='Rh coated')
plt.plot(energy/1000, r_Rh, label='Rh bulk')
plt.title(f'{coating_thick//10} nm {coating}/{binder} coated {substrate} mirror ' + 'at $\\theta$ = ' + f'{theta*1000:.0f} mrad')
plt.xlabel('Energy (keV)')
plt.ylabel('Reflectivity')
plt.yscale('log')
plt.legend()
plt.show()
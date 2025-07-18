import numpy as np
from xraydb import (coated_reflectivity, mirror_reflectivity)
import matplotlib.pyplot as plt

coating = 'Rh'
coating_thick = 300
substrate = 'Si'
theta = 0.004
energy = np.linspace(10000, 35000, 500)
binder = 'Cr'
binder_thick = 30

refl_coat = coated_reflectivity(coating, coating_thick, substrate, theta, energy, binder=binder, binder_thick=binder_thick)
refl_rhod = mirror_reflectivity('Rh', theta, energy)

title = f'$\\rm {coating_thick} \\AA \\> {coating}/{binder_thick} \\AA \\> {binder} \\> coated \\> {substrate} \\> mirror \\> \\theta\\, =\\, {theta*1000:.0f} mrad $'
plt.plot(energy, refl_coat, label='Rh coated')
plt.plot(energy, refl_rhod, label='Rh bulk')
plt.title(title)
plt.xlabel('Energy (eV)')
plt.ylabel('Reflectivity')
plt.yscale('log')
plt.legend()
plt.show()

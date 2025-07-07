import numpy as np
from xraydb import multilayer_reflectivity
import matplotlib.pyplot as plt

stackup = ['Si', 'W']
N = 50
thickness = [27, 18] # angstroms
substrate = 'SiO2'
theta = 0.01
energy = np.linspace(500, 20000, 5000)

r = multilayer_reflectivity(
    stackup, thickness, substrate, theta, energy, n_periods=N)
plt.plot(energy/1000, r)
plt.title('$40 \\times [\mathrm{27\ \AA\ Si, 18\ \AA\ W}]$ ' \
          'multilayer at $\\theta$ = ' + f'{theta*1000:.0f} mrad')
plt.xlabel('Energy (keV)')
plt.ylabel('Reflectivity')
plt.show()
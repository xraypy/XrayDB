import numpy as np
from xraydb import multilayer_reflectivity
import matplotlib.pyplot as plt
from xraydb.utils import PLANCK_HC

energy = PLANCK_HC / 11

stackup = ['W', 'Si']
N = 50
period = 32
Gamma = 0.34
thickness = [period * Gamma, period * (1 - Gamma)]
substrate = 'SiO2'
theta = np.linspace(0, 0.5, 250)

r = multilayer_reflectivity(
    stackup, thickness, 'B4C', theta, energy, n_periods=N)
plt.plot(theta*1000, r)
plt.title('X-ray reflectivity at $E=1127 \mathrm{eV}$')
plt.xlabel('$\\theta \mathrm{ (mrad)}$')
plt.ylabel('Reflectivity')
plt.legend()
plt.show()


# coated mirror testing

# stackup = ['Rh', 'Cr']
# thickness = [500, 50]
# substrate = 'Si'
# theta = np.linspace(0, 0.5, 250)
# energy = 1000
# r = multilayer_reflectivity(
#     stackup, thickness, substrate, theta, energy, n_periods=1)

# plt.plot(np.rad2deg(theta), r)
# plt.title('X-ray reflectivity at $E=1000 \mathrm{eV}$')
# plt.xlabel('$\\theta \mathrm{ (mrad)}$')
# plt.ylabel('Reflectivity')
# plt.show()
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
theta = np.linspace(0, 0.5, 250)

r = multilayer_reflectivity(
    stackup, theta, energy, substrate='B4C', thickness=thickness, n_periods=N
)
plt.plot(theta*1000, r)
plt.title('X-ray reflectivity at $E=1127 \mathrm{eV}$')
plt.xlabel('$\\theta \mathrm{ (mrad)}$')
plt.ylabel('Reflectivity')
plt.legend()
plt.show()

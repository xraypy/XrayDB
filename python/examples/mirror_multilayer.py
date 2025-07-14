import numpy as np
from xraydb import multilayer_reflectivity
import matplotlib.pyplot as plt

# 40 layers of [27Ang Si, 18Ang W]
materials = ['Si', 'W']
thicknesses = [27, 18] # angstroms
n_periods = 40
substrate = 'SiO2'
theta = 0.01
energy = np.linspace(500, 20000, 5000)

reflect = multilayer_reflectivity(materials, thicknesses, substrate,
                                  theta, energy, n_periods=n_periods)

plt.plot(energy, reflect)
plt.title(f'40 x [27\u212B Si, 18\u212B W] multilayer at \u03B8 = {theta*1000:.0f} mrad')
plt.xlabel('Energy (eV)')
plt.ylabel('Reflectivity')
plt.show()

import numpy as np
from xraydb import coated_reflectivity 
import matplotlib.pyplot as plt

# coating = 'Rh'
# coating_thick = 500
# substrate = 'SiO2'
# theta = np.linspace(0, 0.5, 250)
# energy = 1000
# binder = 'Cr'
# binder_thick = 50
# r = coated_reflectivity(coating, coating_thick, substrate, theta, energy, 
#                         binder=binder, binder_thick=binder_thick)

RhCrSi_r = np.array([1.000000e+00, 7.776340e-01, 5.477470e-01, 2.409720e-01, 5.100943e-02,
                    1.580261e-02, 6.627787e-03, 3.180575e-03, 1.703938e-03, 1.107435e-03,
                    7.098140e-04, 5.086654e-04, 4.295797e-04, 2.072734e-04, 1.592465e-04,
                    1.707207e-04, 1.133023e-04, 8.167967e-05, 5.430874e-05, 8.805342e-05,
                    2.725561e-05, 4.779536e-05, 3.314265e-05, 2.371928e-05, 2.565458e-05,
                    2.122170e-05])

coating = 'Rh'
coating_thick = 500
substrate = 'Si'
theta = np.linspace(0, 0.5, 26)
energy = 1000
binder = 'Cr'
binder_thick = 50
r = coated_reflectivity(coating, coating_thick, substrate, theta, energy, binder=binder, binder_thick=binder_thick)
from numpy.testing import assert_allclose
# assert_allclose(r, RhCrSi_r, rtol=0.005)
plt.plot(theta*1000, r, label='xraydb')
plt.plot(theta*1000, RhCrSi_r, label='Henke')
plt.title(f'X-ray reflectivity at E = {energy} eV')
plt.xlabel('$\\theta \mathrm{\ (mrad)}$')
plt.ylabel('Reflectivity')
plt.show()
print("Average % error: ", np.mean((r - RhCrSi_r)/r))
assert_allclose(r, RhCrSi_r, rtol=0.005)



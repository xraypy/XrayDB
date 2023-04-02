#!/usr/bin/env python
import time
import numpy as np
from scipy.constants import physical_constants
from scipy.integrate import quad

from lmfit.printfuncs import gformat

note = """# this will calculate the following energies related to Compton scattering for
# X-ray energies ranging from 10 to 1,000,000 eV
#
# Energy                : energy of incident X-ray
# Compton_xray_90deg    : energy of X-ray scattered at theta=90
# Compton_xray_mean     : mean energy of Compton-scattered X-ray
# Compton_electron_mean : mean energy of Compton-scattered electron
#
# note that Compton_xray_90deg = energy - energy / (1 + energy / (mc**2))
#
# the mean values are found by integrating the angular dependence
# with the Klein-Nishina distribution of scattering cross-section."""


# r_e ~ 2.8 fm     : classical electron radius
# mc2 ~ 511000 eV  : electron mass energy
r_e = physical_constants['classical electron radius'][0]*1.e6
mc2 = physical_constants['electron mass energy equivalent in MeV'][0]*1.e6

def KleinNishina(theta, energy):
    "Klein-Nishina distribution"
    gamma =  energy / mc2
    cfact = 1.0/(1 + gamma*(1 - np.cos(theta)))
    return (r_e*cfact)**2 * (cfact + 1.0/cfact - np.sin(theta)**2)

def ElectronEnergyKleinNishina(theta, energy):
    "Compton_electron energy * Klein-Nishina distribution"
    gamma =  energy / mc2
    cfact = 1.0/(1 + gamma*(1 - np.cos(theta)))
    return energy*(1-cfact) * (r_e*cfact)**2 * (cfact + 1.0/cfact - np.sin(theta)**2)

theta = np.arange(0, 1, 0.0001)*np.pi

out = ["# results for mean Compton Electron Energy",
       "# all values are energies in eV"]

out.extend(note.split('\n'))
out.extend(["#------------------------------------------",
            "#   Energy   Compton_Xray_90deg Compton_Xray_mean Compton_Electron_mean"])

esteps = (10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 22, 24, 25,
          26, 28, 30, 33, 35, 38, 40, 43, 45, 48, 50, 55, 60, 65,
          70, 75, 80, 85, 90, 95, 100)
n = 0
for scale in range(5):
    for estep in esteps:
        if estep == 10 and scale > 0:
            continue
        energy = 10.0**(scale)*estep
        cxray_90deg = energy / (1 + energy/mc2)
        celec_mean = (quad(ElectronEnergyKleinNishina, 0, 2*np.pi, energy)[0]
                      / quad(KleinNishina, 0, 2*np.pi, energy)[0])
        s = (f"{energy:10.1f}   {gformat(cxray_90deg, 12)}       {gformat(energy-celec_mean, 12)}      {gformat(celec_mean, 12)}")
        out.append(s)
        n  += 1

out.append('')

with open('Compton_energies.txt', 'w') as fh:
    fh.write('\n'.join(out))

time.sleep(0.01)
print('done')

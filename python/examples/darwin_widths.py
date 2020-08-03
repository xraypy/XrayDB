import numpy as np
from xraydb import darwin_width
import matplotlib.pyplot as plt
from matplotlib.ticker import (AutoLocator, AutoMinorLocator)

dw_si111 = darwin_width(10000, 'Si', (1, 1, 1))
dw_si333 = darwin_width(10000, 'Si', (1, 1, 1), m=3)

fmt_string = "Darwin Width for {:s} at {:.0f} keV: {:.2f} microrad, {:.2f} eV"
print(fmt_string.format('Si(111)', 10, dw_si111.theta_fwhm*1e6,
                        dw_si111.energy_fwhm))

print(fmt_string.format('Si(333)', 10, dw_si333.theta_fwhm*1e6,
                        dw_si333.energy_fwhm))


dtheta  = dw_si111.dtheta*1e6
denergy = dw_si111.denergy[::-1]

#  slightly advanced matplotlib hackery:
fig, ax = plt.subplots(constrained_layout=True)


ax.plot(dtheta, dw_si111.intensity, label='Si(111)', linewidth=2)
ax.plot(dw_si333.dtheta*1e6, dw_si333.intensity, label='Si(333)', linewidth=2)

ax.set_title('X-ray diffraction intensity at 10keV')
ax.set_xlabel('Angle ($ \mu \mathrm{rad}$)')
ax.set_ylabel('Reflectivity')
ax.legend()

def foreward(x): return np.interp(x, dtheta, denergy)
def backward(x): return np.interp(x, denergy, dtheta)

axtop = ax.secondary_xaxis('top', functions=(foreward, backward))
axtop.set_xlabel('Energy (eV)')

plt.show()

import numpy as np
from xraydb import darwin_width
import matplotlib.pyplot as plt

dw_si111 = darwin_width(10000, 'Si', (1, 1, 1))
dw_si333 = darwin_width(30000, 'Si', (3, 3, 3))

fmt_string = "Darwin Width for {:s} at {:.0f} keV: {:5.2f} microrad, {:5.2f} eV"
print(fmt_string.format('Si(111)', 10,
                        dw_si111.theta_width*1e6,
                        dw_si111.energy_width))


print(fmt_string.format('Si(333)', 30,
                        dw_si333.theta_width*1e6,
                        dw_si333.energy_width))

dtheta  = dw_si111.dtheta*1e6
denergy = dw_si111.denergy[::-1]

#  slightly advanced matplotlib hackery:
fig, ax = plt.subplots(constrained_layout=True)


ax.plot(dtheta, dw_si111.intensity, label='$I$, Si(111)', linewidth=2)
ax.plot(dtheta, dw_si111.intensity**2, label='$I^2$, Si(111)', linewidth=2)
ax.plot(dw_si333.dtheta*1e6, dw_si333.intensity**2, label='$I^2$ Si(333) 30 keV', linewidth=2)


ax.set_title('X-ray diffraction intensity at 10keV')
ax.set_xlabel('Angle - $\\theta_B$ ($ \mu \mathrm{rad}$)')
ax.set_ylabel('Reflectivity')
ax.legend()

plt.show()

import numpy as np
from xraydb import darwin_width
import matplotlib.pyplot as plt

dw_si111 = darwin_width(10000, 'Si', (1, 1, 1))

dtheta  = dw_si111.dtheta*1e6

fig, ax = plt.subplots(constrained_layout=True)

ax.plot(dtheta, dw_si111.intensity, label='$I$, 1 crystal', linewidth=2)
ax.plot(dtheta, dw_si111.rocking_curve, label='Rocking Curve', linewidth=2)


ax.set_title('X-ray Rocking Curve at 10keV, Si(111)')
ax.set_xlabel('Angle - $\\theta_B$ ($ \\mu \mathrm{rad}$)')
ax.set_ylabel('Reflectivity')
ax.legend()

plt.show()

import numpy as np
from xraydb import darwin_width
import matplotlib.pyplot as plt



dw_si111 = darwin_width(10000, 'Si', (1, 1, 1))
dw_si220 = darwin_width(10000, 'Si', (2, 2, 0))
dw_si311 = darwin_width(10000, 'Si', (3, 3, 1))
dw_si333a = darwin_width(10000, 'Si', (3, 3, 3))
dw_si333b = darwin_width(10000, 'Si', (1, 1, 1), m=3)

plt.plot(dw_si111.dtheta*1e6, dw_si111.intensity, label='Si(111)')
# plt.plot(dw_si220.dtheta*1e6, dw_si220.intensity, label='Si(220)')
# plt.plot(dw_si311.dtheta*1e6, dw_si311.intensity, label='Si(311)')
plt.plot(dw_si333b.dtheta*1e6, dw_si333b.intensity, label='Si(333)')
print(dw_si111.theta, dw_si333a.theta, dw_si333b.theta)
plt.title('X-ray diffraction intensity at 10keV')
plt.xlabel('Angle ($ \mu \mathrm{rad}$)')
plt.ylabel('Reflectivity')
plt.legend()
plt.show()

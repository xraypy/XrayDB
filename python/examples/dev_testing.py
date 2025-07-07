from xraydb import (multilayer_reflectivity, coated_reflectivity)
import numpy as np
from numpy.testing import assert_allclose
import matplotlib.pyplot as plt
import xrt.backends.raycing.materials as rm
from xraydb import get_material

def test_multilayer_reflectivity():
    thickness = [27, 18]
    n_periods = 40

    mSi = rm.Material('Si', rho=2.329, table='Chantler')
    mW = rm.Material('W', rho=19.25, table='Chantler')
    mL = rm.Multilayer(mSi, thickness[0], mW, thickness[1], n_periods, mSi)
    theta = np.linspace(0, 0.5, 21) 
    # print(theta*180/np.pi)
    E = 1000
    # print(get_material('Si'))
    
    # Data from henke.lbl.gov/
    WSi_r = np.array([1.0, 0.753174, 0.186214, 0.0224796, 0.009611952, 0.01369169, 0.117561, 0.002706273, 0.0007443512, 0.0004953227, 
                      0.0005217905, 0.002400966, 0.0001348259, 6.357297e-06, 2.817841e-06, 4.196663e-06, 1.501378e-05, 0.0006133853, 
                      0.0001087077, 1.91107e-05, 3.025002e-05])

    r = multilayer_reflectivity(['Si', 'W'], thickness, 'Si', theta, E, n_periods) 
    rs, rp = mL.get_amplitude(E, np.sin(theta))[0:2]
    print("Average % error between xraydb and xrt: ", np.mean((r - abs(rs)**2)/r))
    print("Average % error between xraydb and LBL: ", np.mean((r - WSi_r)/r))
    print("Average % error between xrt and LBL: ", np.mean((abs(rs)**2 - WSi_r)/abs(rs)**2))
    plt.figure()
    plt.plot(theta * 1000, r, label='xraydb')
    plt.plot(theta * 1000, abs(rs)**2, label='xrt')
    plt.plot(theta * 1000, WSi_r, label='LBL')
    plt.ylabel('Reflectivity')
    plt.xlabel('$\\theta \mathrm{\ (mrad)}$')
    plt.legend()
    plt.show()
    assert_allclose(r,abs(rs)**2, rtol=0.005)
test_multilayer_reflectivity()

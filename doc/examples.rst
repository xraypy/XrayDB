
.. _example_calcs:

Example Calculations of X-ray properties of materials
=========================================================

.. _XrayDB Web App (beta!):  https://millenia.cars.aps.anl.gov/xraydb

.. module:: xraydb
   :noindex:

Here, a few detailed examples of using the `xraydb.sqlite` to calculate the
X-ray properties of materials are shown.  These all use the functions in
the python `xraydb` module, which is describe in more detail in the next
chapter, :ref:`python_api`.  The examples will explore some aspects of
X-ray physics, but will not give a complete tutorial on the concepts here.
For reference see :cite:`AlsNielson_McMorrow2011` for example.  Some of
these calculations are also available at  `XrayDB Web App (beta!)`_.


X-ray attenuation by elements
-----------------------------------------------

The XrayDB database tabulates values of the X-ray mass attenuation
coefficient, :math:`\mu/\rho`, for each element.  In most of the X-ray
regime used in materials characterization (say, up to 150 keV), the
photo-electric effect is the main process that causes X-ray attenuation.
When the photo-electric process is dominant, the values for
:math:`\mu/\rho` depends strongly on *Z* of the atom and on X-ray energy
*E*.  In addition to these strong dependencies, sharp increases --
so-called absorption edges -- with be see at energies of bound core
electron levels of atoms.  To illustrate these characteristics, the
following script will plot :math:`\mu/\rho` for selected elements:

.. literalinclude:: ../python/examples/mu_elements.py

.. _fig_mu_depth:

.. figure::  _images/mu_elements.png
    :target: _images/mu_elements.png
    :width: 75%
    :align: center

    X-ray mass attenuation coefficient for C, Cu, and Au.

As you can see in Figure from this figure, the attenuation drops very
strongly with :math:`E` -- approximately as :math:`E^3`. :math:`\mu` also
depends strongly with *Z*, though the sharp absorption edges make this more
complicated.

You can also observe that at relatively high energies for relatively low-Z
elements (such as C above about 20 keV) that the attenuation levels off.
This is because the coherent (Rayleigh) and incoherent (Compton) scattering
processes dominate, so that the photo-electric absorption is no longer the
dominant X-ray scattering process.  This can be illustrated by plotting the
different components of :math:`\mu/\rho` for C, as with the following script:

.. literalinclude:: ../python/examples/mu_components_C.py

which will generate the following plot:

.. _fig_mu_components_C:

.. figure::  _images/mu_components_C.png
    :target: _images/mu_components_C.png
    :width: 75%
    :align: center

    X-ray scattering and attenuation factors for C.

Note that above 20 keV, the photo-electric absorption and incoherent
Compton contributions are about equal, and that the Compton scattering
dominates above 50 keV.  As shown above, the photo-electric scattering will
be much higher for heavier elements. The Rayleigh and Compton scattering
have a much weaker dependence on *Z*, so that the photo-electric process
dominates to higher energies.  Replacing 'C' with 'Fe' in the script above
will generate the following plot:

.. _fig_mu_components_Fe:

.. figure::  _images/mu_components_Fe.png
    :target: _images/mu_components_Fe.png
    :width: 75%
    :align: center

    X-ray scattering and attenuation factors for Fe.

which shows that the Compton scattering reaching about 0.1 to 0.25
:math:`\rm cm^2/gr` for Fe, about the same value as it was for C, while the
photo-electric cross-section dominates past 100 keV.

:math:`\mu` calculations for materials
------------------------------------------

While one can use the above values for :math:`\mu/\rho` to calculate the
attenuation of X-rays by multi-element materials, the :func:`material_mu`
function is available to do the more convenient calculation of the X-ray
absorption coefficient :math:`\mu` in units of 1/cm for a material and
energy value and density (which are known for several common materials).
This gives the length for which X-ray intensity is reduced by a factor of
*e*, and so can be used to calculate the fraction of the X-rays transmitted
through a material of known thickness, as :math:`\exp(-t\mu)` for a
material of thickness *t*.  As a first example, we calculate the the
fraction of X-ray transmitted through 1 mm of the water as a function of
X-ray energy:

.. literalinclude:: ../python/examples/mu_water.py

.. _fig_mu_water:

.. figure::  _images/mu_water.png
    :target: _images/mu_water.png
    :width: 75%
    :align: center

    Fraction of X-rays absorbed and transmitted by water


replacing::

    mu = material_mu('H2O', energy)

with::

    mu = material_mu('CaCO3', energy, density=2.71)

would generate the following plot

.. _fig_mu_calcite:

.. figure::  _images/mu_calcite.png
    :target: _images/mu_calcite.png
    :width: 75%
    :align: center

    Fraction of X-rays absorbed and transmitted by calcite


For many X-ray experiments, selecting the size of a material size so that
its thickness is approximately 1 to 2 absorption length is convenient so
that X-ray scattering and emission can be observed strongly, with neither
all primary and scattered X-rays being absorbed by the material itself, but
also not simply passing through the material without any interaction.  For
example, one can simply do::

  >>> from xraydb import material_mu
  >>> mu_20kev = xraydb.material_mu('CaCO3', 20000, density=2.71)
  >>> print("CaCO3 1/e depth at 20keV = {:.3f} mm".format(10/mu_20kev))
  CaCO3 1/e depth at 20keV = 0.648 mm



X-ray flux calculations for ionization chambers and photodiodes
---------------------------------------------------------------------

Gas-filled ionization chambers are widely used as X-ray detectors. They are
simple to use, inexpensive, and can be highly linear in estimating the
photon flux over many orders of magnitude.  X-rays entering a chamber
filled with an inert gas (typically He, N2, or one of the noble gases, or a
mixture of these) will be partially absorbed by the gas, with the strong
energy dependence shown above.  By adjustng the composition of the gas,
nearly any fraction of the incident X-ray beam can be absorbed at a
particular X-ray energy, making these ideal detectors to sample the
intensity of an X-ray beam incident on a sample, while attenuating only a
fraction of the beam.

Some of the X-rays in the gas will be absorbed by the photo-electric effect
which will *ionize* the gas, generating free electrons and energetic ions.  Te
first ionization event will generate an electron-ion pair with the energy of
the X-ray minus the binding energy of the core electron. The high-energy
electron and ion pair will further ionize other gas molecules.  With an
electric potential (typically on the order of 1 kV /cm) across the plates of
the chamber, a current can be measured that is proportional to the X-ray
energy and fluence of the X-rays.

In addition to the photo-electric absorption, X-rays can be attenuated by gas
molecules in an ion chamber by incoherent (Compton) or coherent (Rayleigh)
scattering processes.  The coherent scattering will not generate any electrons
in the gas, but will elastically scatter X-rays out of the main beam.
Incoherent scattering will generate some current, though not all (and
typically only a small portion) of the incident X-ray energy is given to an
electron to generate a current.  Compton scattering gives a distribution of
energies to the scattered electron depending on the angle of scattering.  The
median energy of electrons generated by Compton scattering X-rays of energy
:math:`E` at 90 degrees will be

.. math::
    E_c_median = E / (1 + m_ec^2 / E)

For X-rays of 10 keV, :math:`E_c_median` is about 192 eV. For 20 keV X-rays,
it will be 750 eV, and for 50 keV X-rays, it will be 4.5 keV.  Because the
angular distribution of Compton scattering is not uniform, these median values
over-estimate the amount of energy transferred to the scattered electron a
small amount that increases with energy.  The mean energy of the
Compton-scattered electron can be found by integrating the Klein-Nishina
distribution. Since these values depend only on the incident X-ray energy,
these calculations have been done and the values tabulated in the
`Compton_energies` table in the XrayDB sqlite database.


Although the energy transferred to the electron by Compton scattering is much
less than by the photo-electric process the contribution can be important.
This is especially true for low-Z gas molecules such as He and N2 at
relatively high energies (10 keV and above) for which incoherent scattering
becomes much more important than photo-electric absorption, as shown above
for C. That is, for accurate estimates of fluxes from ion chamber currents at
energies about 20 keV or so, the contribution from Compton scattering should
be included.  For photo-diodes (typically made of Si), the Compton scattering
cross-section exceeds the photo-electric cross-section about 56 keV.


The process of converting the X-ray generated current into X-ray fluence
involves several steps. The energy from a single X-ray-generated
electron is converted into a number of electron-ion pairs given by the
*effective ionization potential* of the gas.  These are reasonably
well-known values (see :cite:`Knoll2010`) that are all between 20 and 40
eV, given in the :ref:`Table of Effective Ionization Potentials
<xray_ionpot_table>`.

.. index:: Table of Effective Ionization Potentials
.. _xray_ionpot_table:

   Table of Effective Ionization Potentials. Many of these are taken from
   :cite:`Knoll2010`, while others appear to come from International Commission
   on Radiation Units & Measurement, Report 31, 1979.  The names given are
   those supported by the functions :func:`ionization_potential` and
   :func:`ionchamber_fluxes`.

           +----------------------+----------------+
           | gas/materia name(s)  | potential (eV) |
           +======================+================+
           | hydrogen, H          |   36.5         |
           +----------------------+----------------+
           | helium, He           |   41.3         |
           +----------------------+----------------+
           | nitrogen, N, N2      |   34.8         |
           +----------------------+----------------+
           | oxygen, O, O2        |   30.8         |
           +----------------------+----------------+
           | neon, Ne             |   35.4         |
           +----------------------+----------------+
           | argon, Ar            |   26.4         |
           +----------------------+----------------+
           | krypton, Kr          |   24.4         |
           +----------------------+----------------+
           | xenon, Xe            |   22.1         |
           +----------------------+----------------+
           | air                  |   33.8         |
           +----------------------+----------------+
           | methane, CH4         |   27.3         |
           +----------------------+----------------+
           | carbondioxide, CO2   |   33.0         |
           +----------------------+----------------+
           | silicon, Si          |    3.68        |
           +----------------------+----------------+
           | germanium, Ge        |    2.97        |
           +----------------------+----------------+

From this table, we can see that the absorption (by photo-electric effect)
of 1 X-ray of energy 10 keV will eventually generate about 300 electron-ion
pairs.  That is not much current, but if :math:`10^8 \,\rm Hz` X-rays are
absorbed per second, then the current generated will be around 5 nA.  Of
course, the thickness of the gas or more precisely the length of gas under
ionizing potential will have an impact on how much current is generated.
The photo-current will then be amplified and converted to a voltage using a
current amplifier, and that voltage will then recorded by a number of
possible means.  Note that while the ion chamber itself will be linear over
many orders of magnitude of X-ray flux (provided the potential between the
plates is high enough - typically in the 1 kV/cm range), a current
amplifier at a particular setting of sensitivity will be linear only over a
couple orders of magnitude (typically between output voltage of 0.05 to 5
V).  Because of this, the sensitivity of the current amplifier used with an
ion chamber needs careful attention.

A photo-diode works in much the same way as an ionization chamber.  X-rays
incident on the diode (typically Si or Ge) will be absorbed and generate a
photo-current that can be collected.  Typically PIN diodes are used, and
with a small reverse bias voltage.  Because the electrons do not need to
escape the material but generate a current transported in the
semiconductor, the effective ionization potential is much lower - a few
times the semiconductor band gap instead of a few time the lowest
core-level ionization potential.  The current generated per X-ray will be
larger than for an ion chamber, but still amplified with a current
amplifier in the same way as is used for an ion chamber.  Generally, diodes
are thick enough that they absorb all incident X-rays.


The function :func:`ionchamber_fluxes` will help generate X-ray fluxes
associated with an ion chamber and help handle all of these subtle issues,
using the following inputs:

  * `gas`: the gas, or mixture of gases used or 'Si' or 'Ge' for diodes.
  * `length`: the length of the ion chamber, in cm.
  * `energy`: the X-ray energy, in eV.
  * `volts`: the output voltage of the current amplifier
  * `sensitivity` and `sensitivity_units`: the sensitivity or gain of the
    amplifier used to convert the photo-current to the recorded voltage.

The default `sensitivity_units` is 'A/V' but can be set to any of the
common SI prefixes such as 'p', 'pico', 'n', 'nano', :math:`\mu`,
(unicode '03bc'), 'u', 'micro', 'm', or 'milli', so that::


    >>> fluxes = ionchamber_fluxes('N2', volts=1, energy=10000, length=10,
                                   sensitivity=1.e-9)
    >>> fluxes = ionchamber_fluxes('N2', volts=1, energy=10000, length=10,
                                   sensitivity=1, sensitivity_units='nA/V')

will give the same results.

The output from  :func:`ionchamber_fluxes` is a named tuple with 4 fields:

  * `photo`  -  the flux absorbed by the photo-electric effect, in Hz.
  * `incoherent`  -  the flux scattered by the Compton effects, in Hz.
  * `incident` - the flux incident on the ion chamber, in Hz.
  * `transmitted` - the flux beam leaving the ion chamber, in Hz.

As described above, the current in the ion chamber or photo-diode is generated
by electrons and ions produced by both the photo-electric and incoherent or
Compton scattering.  The photo-electric cross-section will dominate for heavy
elements and relatively low X-ray energies, but does not necessarily dominate
at high X-ray energies. The photo-electric cross-section with the incident
X-ray energy and the incoherent cross-section with the ***mean***
Compton-scattering energy, using the calculated and tabulated mean energies of
the Compton-scattered electrons are used to estimate the incident flux from
the photo-current. The total attenuation cross-section, including the coherent
cross-sections, is used to calculate the transmitted flu from the incident
flux.

As an example calculation of ion chamber currents::

   >>> fl = ionchamber_fluxes(gas='nitrogen', volts=1.25, energy=18000,
                                  length=10.0, sensitivity=1.e-6)
   >>> print(f"Incident= {fl.incident:g} Hz, Transmitted flux= {fl.transmitted:g} Hz")
   Incident= 2.2358e+12 Hz, Transmitted flux= 2.214e+12 Hz

It is not uncommon for an ion chamber to be filled with a mixture of 2 or
more gases so as to better control the fraction of X-rays absorbed in a
chamber of fixed length. This can be specified by passing in a dictionary
of gas name and fractional density, as with::

   >>> fl = ionchamber_fluxes(gas={'Kr':0.5, 'Ar': 0.5}, volts=1.25,
                              energy=18000, length=10,
                              sensitivity=1, sensitivity_units='microA/V')
   >>> print(f"Incident= {fl.incident:g} Hz, Transmitted flux= {fl.transmitted:g} Hz")
   Incident= 1.43737e+10 Hz, Transmitted flux= 3.28986e+09 Hz

Finally, the pressure of the gas is sometimes adjusted to alter the
fraction of the beam absorbed.  The calculations here all use the densities
at STP, but changes in gas density will be exactly linear to changing the
length of the ion chamber.


X-ray mirror reflectivities
-------------------------------------------

At very shallow angles of incidence X-rays can be reflected by total
external reflection from a material. The reflectivity can be very high
at relatively low energies and shallow angles, but drops off dramatically
with increasing energy, increasing angle, and decreasing electron density.
Still, this reflectivity is one of the few ways to steer X-ray beams and so
is widely used in synchrotron radiation sources.

The reflectivity can be calculated with the :func:`mirror_reflectivity`
function which takes X-ray energy, incident angle, and mirror material as
arguments.

An example script, comparing the energy-dependence of the reflectivity for
a few common mirror materials is given as

.. literalinclude:: ../python/examples/mirror_comparison.py


.. _fig_mirrors:

.. figure::  _images/mirrors.png
    :target: _images/mirrors.png
    :width: 75%
    :align: center

    X-ray mirror reflectivity at :math:`\theta = 2\mathrm{mrad}` for
    selected mirror surfaces and coatings used for mirrors.



Darwin widths of monochromator crystals
-------------------------------------------

Bragg's law describes X-ray diffraction from crystals as

.. math::
    m \lambda = 2 d \sin(\theta)

where :math:`\lambda` is the X-ray wavelength, :math:`d` the d-spacing of
the crystal lattice plane, :math:`\theta` the incident angle, and :math:`m`
the order of the reflection.  For imperfect crystals, in which the lattice
planes are not stacked perfectly over extended distances, the angular width
of any particular reflection is dominated by the spread in d-spacing and
the mosaicity inherent in the crystal.  For perfect crystals, however, the
angular width of a reflection is dominated by the fact that effectively all
of the X-rays will scatter from the lattice well before any attenuation of
the X-ray beam occurs. This *dynamical* diffraction gives a small but
finite offset from the Bragg angle, and gives a broadened angular width to
reflection.  This is usually called the Darwin width (named for
Charles G. Darwin, grandson of the more famous Charles R. Darwin).  In
addition, the refraction and in particular the absorption effects that give
anomalous scattering (as calculated with :func:`xray_delta_beta`) make the
"rocking curve" of reflected intensity as a function of angle an asymmetric
shape.

All of these effects are included in the :func:`darwin_width` function,
which follows very closely the description from chapter 6.4 in
:cite:`AlsNielson_McMorrow2011`.  The function takes inputs of

  * `energy`: the X-ray energy, in eV.
  * `crystal`: the atomic symbol for the crystal: 'Si', 'Ge', or 'C'. ['Si']
  * `hkl`: a tuple with (h, k, l) of the reflection used. [(1, 1, 1)]
  * `a`: lattice constant [`None` - use nominal value for crystal]
  * `polarization`: `s`, `p`, or `u` to specify the X-ray polarization relative to the crystal [`s`]
  * `m`: the order of the reflection. [1]
  * `ignore_f1`: whether to ignore `f1`. [False]
  * `ignore_f2`: whether to ignore `f2`. [False]

Polarization of `s` should be used for vertically deflecting monochromators
at most synchrotron sources (which will normally be horizontally
polarized), and `p` should be used for horizontally deflecting
monochromators.  For crystals used to analyzed unpolarized X-ray emission,
use `u`, which will give the average of `s` and `p` polarization.

As with :func:`ionchamber_fluxes`, the output here is complicated enough
that it is put into a named `DarwinWidth` tuple that will contain the
following fields:

   * `theta` - the nominal Bragg angle, in rad
   * `theta_offset` - the offset from the nomimal Bragg angle, in rad.
   * `theta_width` - estimated angular Darwin width, in rad
   * `theta_fwhm` - estimated FWHM of the angular reflectivity curve, in rad
   * `energy_width` - estimated energy Darwin width, in eV
   * `energy_fwhm` - estimated FWHM energy reflectivity curve, in eV
   * `zeta` -  nd-array of :math:`\zeta = \Delta\lambda/\lambda`.
   * `dtheta`  - nd-array of angles around from Bragg angle, in rad
   * `denergy` -  nd-array of energies around from Bragg energy, in eV
   * `intensity` - nd-array of reflected intensity at `zeta` values.

Here, `dtheta` will be given by :math:`\Delta\theta = \zeta \tan(\theta)`,
and `denergy` will be given by :math:`\Delta{E} = \zeta E`.  All of the
nd-arrays will be the same size, so that plots of reflectivity can be
readily made.  An example usage, printing the predicted energy and angular
widths and plotting the intensity profile or "rocking curve" is

.. literalinclude:: ../python/examples/darwin_widths.py

which will print out values of::

  Darwin Width for Si(111) at 10 keV: 26.96 microrad,  1.34 eV
  Darwin Width for Si(333) at 30 keV:  1.81 microrad,  0.27 eV

and generates a plot of

.. _fig_darwin:

.. figure::  _images/darwin_widths.png
    :target: _images/darwin_widths.png
    :width: 75%
    :align: center

    X-ray monochromator diffracted intensities around the Si(111)
    reflection. Here, :math:`i` represents the intensity of a single
    reflection, and :math:`i^2` the intensity from 2 bounces, as for a
    double-crystal monochromator.  The intensity and angular offset of the
    third harmonic is also shown.


Note that the values reported for `theta_fwhm` and `energy_fwhm` will be
about 6% larger than the reported values for `theta_width` and
`energy_width`.  The `width` values closely follow the region of the curve
where the reflectivity ignoring absorption would be 1 - the flat top of the
curve.  Since a double-crystal monochromator will suppress the tails of the
reflectivity, this smaller value is the one typically reported as "the
Darwin width", though some sources will report this smaller value as "FWHM".

import logging

# pylint: disable=no-name-in-module
from osp.core import CMCL
from osp.wrappers.simcmclkinetics import KineticsSession
from osp.wrappers.simcmclkinetics import EATEngine


# This examples aims to run the EAT_GPF use case by hard-coding
# the input CUDS objects and passing them to the KineticsSession class
# for execution.
#
# Replicated the inputs.json of the use case; note that these values
# (except PSD) were taken from the following kinetics-backend commit:
# 3d19bb48da1033d7f9ef76800aa24e578e260eeb

# Set the level of the logger in OSP Core
logging.getLogger('osp.core').setLevel(logging.ERROR)

# Initialise and set values for the GPF
gpf = CMCL.GPF()
gpf.add(
    CMCL.LENGTH(value=150, unit="mm"),
    CMCL.DIAMETER(value=150, unit="mm"),
    CMCL.CHANNEL_DENSITY(value=200.0, unit="1/inch^2"),
    CMCL.WALL_THICKNESS(value=0.2, unit="mm"),
    CMCL.PERMEABILITY(value=4.0e-13, unit="m^2"),
    CMCL.PORE_DIAMETER(value=1.5e-05, unit="m"),
    CMCL.WALL_POROSITY(value=0.49, unit="-"),
    CMCL.PM_FILTRATION_EFFICIENCY(value=0.0, unit="-"),
    CMCL.PN_FILTRATION_EFFICIENCY(value=0., unit="-"),
    rel=CMCL.HAS_QUANTITATIVE_PROPERTY
)

# Initialise the exhaust
untreated_exhaust = CMCL.UNTREATED_EXHAUST()

# Multi-value as single string (fudge)
particle_psd = CMCL.PARTICLE_SIZE_DISTRIBUTION()
particle_psd.add(CMCL.PARTICLE_NUMBER_DENSITIES(value_string=("1.12E-09, 2.40E-07, 3.29E-05, 2.89E-03, 1.63E-01, \
                                                               5.92E+00, 1.39E+02, 2.11E+03, 2.08E+04, 1.35E+05, 5.83E+05, \
                                                               1.72E+06, 3.64E+06, 6.00E+06, 8.38E+06, 1.04E+07, 1.20E+07, \
                                                               1.36E+07, 1.59E+07, 1.84E+07, 2.06E+07, 2.38E+07, 2.91E+07, \
                                                               3.50E+07, 3.90E+07, 4.15E+07, 4.42E+07, 4.80E+07, 5.39E+07, \
                                                               6.33E+07, 7.51E+07, 8.28E+07, 8.10E+07, 7.04E+07, 5.64E+07, \
                                                               4.26E+07, 3.02E+07, 2.00E+07, 1.30E+07, 8.82E+06, 5.92E+06, \
                                                               3.37E+06, 1.43E+06, 4.27E+05, 8.55E+04, 1.13E+04, 9.69E+02, \
                                                               5.38E+01, 1.92E+00, 4.39E-02, 6.42E-04, 6.01E-06, 3.59E-08, \
                                                               1.37E-10, 3.33E-13, 5.17E-16, 5.12E-19, 3.24E-22, 1.30E-25, \
                                                               3.34E-29, 1.00E-30, 1.00E-30, 1.00E-30, 1.00E-30, 1.00E-30, \
                                                               1.00E-30, 1.00E-30, 1.00E-30, 1.00E-30, 1.00E-30, 1.00E-30, \
                                                               1.00E-30, 1.00E-30, 1.00E-30, 1.00E-30, 1.00E-30, 1.00E-30, \
                                                               1.00E-30, 1.00E-30, 1.00E-30, 1.00E-30, 1.00E-30, 1.00E-30, \
                                                               1.00E-30, 1.00E-30, 1.00E-30, 1.00E-30, 1.00E-30, 1.00E-30, \
                                                               1.00E-30, 1.00E-30, 1.00E-30, 1.00E-30, 1.00E-30, 1.00E-30, \
                                                               1.00E-30, 1.00E-30, 1.00E-30, 1.00E-30"), unit="#/m3"),
        CMCL.PARTICLE_SIZE_CLASSES(value_string=("5.00E-01, 5.24E-01, 5.49E-01, 5.76E-01, 6.03E-01, 6.32E-01, \
                                                 6.63E-01, 6.95E-01, 7.28E-01, 7.63E-01, 8.00E-01, 8.38E-01, 8.79E-01, \
                                                 9.21E-01, 9.65E-01, 1.01E+00, 1.06E+00, 1.11E+00, 1.16E+00, 1.22E+00, \
                                                 1.28E+00, 1.34E+00, 1.41E+00, 1.47E+00, 1.54E+00, 1.62E+00, 1.70E+00, \
                                                 1.78E+00, 1.86E+00, 1.95E+00, 2.05E+00, 2.15E+00, 2.25E+00, 2.36E+00, \
                                                 2.47E+00, 2.59E+00, 2.71E+00, 2.84E+00, 2.98E+00, 3.13E+00, 3.28E+00, \
                                                 3.43E+00, 3.60E+00, 3.77E+00, 3.95E+00, 4.14E+00, 4.34E+00, 4.55E+00, \
                                                 4.77E+00, 5.00E+00, 5.24E+00, 5.49E+00, 5.76E+00, 6.03E+00, 6.32E+00, \
                                                 6.63E+00, 6.95E+00, 7.28E+00, 7.63E+00, 8.00E+00, 8.38E+00, 8.79E+00, \
                                                 9.21E+00, 9.65E+00, 1.01E+01, 1.06E+01, 1.11E+01, 1.16E+01, 1.22E+01, \
                                                 1.28E+01, 1.34E+01, 1.41E+01, 1.47E+01, 1.54E+01, 1.62E+01, 1.70E+01, \
                                                 1.78E+01, 1.86E+01, 1.95E+01, 2.05E+01, 2.15E+01, 2.25E+01, 2.36E+01, \
                                                 2.47E+01, 2.59E+01, 2.71E+01, 2.84E+01, 2.98E+01, 3.13E+01, 3.28E+01, \
                                                 3.43E+01, 3.60E+01, 3.77E+01, 3.95E+01, 4.14E+01, 4.34E+01, 4.55E+01, \
                                                 4.77E+01, 5.00E+01"), unit="nm"),
         rel=CMCL.HAS_QUANTITATIVE_PROPERTY)

untreated_exhaust.add(
    CMCL.MASS_FLOW_RATE(value=72.3745273, unit="kg/h"),
    CMCL.TEMPERATURE(value=719.1521765499999, unit="K"),
    CMCL.PRESSURE(value=97835.26926, unit="Pa"),
    particle_psd,
    rel=CMCL.HAS_QUANTITATIVE_PROPERTY
)

# Initialise the main EAT process
eat_process = CMCL.EAT_PROCESS()
eat_process.add(
    gpf,
    untreated_exhaust,
    rel=CMCL.HAS_PROPER_PARTICIPANT
)

# Construct an applicable engine instance
engine = EATEngine()

# Construct a wrapper and run a new session
with KineticsSession(engine) as session:
    wrapper = CMCL.wrapper(session=session)
    cb_synthesis_w = wrapper.add(eat_process, rel=CMCL.HAS_PART)
    wrapper.session.run()
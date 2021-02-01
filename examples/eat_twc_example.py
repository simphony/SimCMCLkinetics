import logging

# pylint: disable=no-name-in-module
from osp.core import CMCL
from osp.wrappers.simcmclkinetics import KineticsSession
from osp.wrappers.simcmclkinetics import EATEngine


# This examples aims to run the EAT_TWC use case by hard-coding
# the input CUDS objects and passing them to the KineticsSession class
# for execution.
#
# Replicated the inputs.json of the use case; note that these values
# were taken from the following kinetics-backend commit:
# 28e848ac3ac5ce22d63ed4ca11af8273ad1b877f

# Set the level of the logger in OSP Core
logging.getLogger('osp.core').setLevel(logging.ERROR)

# Initialise and set values for the GPF
twc = CMCL.TWC()
twc.add(
    CMCL.LENGTH(value=29, unit="mm"),
    CMCL.DIAMETER(value=22, unit="mm"),
    CMCL.CHANNEL_DENSITY(value=62, unit="1/cm^2"),
    CMCL.WALL_THICKNESS(value=0.165, unit="mm"),
    CMCL.CATALYST_SURFACE_MULT(value=70, unit="-"),
    rel=CMCL.HAS_QUANTITATIVE_PROPERTY
)

# Initialise the exhaust
untreated_exhaust = CMCL.UNTREATED_EXHAUST()
untreated_exhaust.add(
    CMCL.MASS_FLOW_RATE(value=0.0004403, unit="kg/s"),
    CMCL.TEMPERATURE(value=600, unit="K"),
    CMCL.PRESSURE(value=1, unit="bar"),
    rel=CMCL.HAS_QUANTITATIVE_PROPERTY
)

# Composition
composition = CMCL.INLET_GAS(unit="mole fraction")
composition.add(
    CMCL.C3H6_FRACTION(value=0.000450, unit="-"),
    CMCL.CO_FRACTION(value=0.014200, unit="-"),
    CMCL.NO_FRACTION(value=0.001000, unit="-"),
    CMCL.NO2_FRACTION(value=0.969, unit="-"),
    CMCL.O2_FRACTION(value=0.0077, unit="-"),
    CMCL.N2_FRACTION(value=0.97665, unit="-"),
    CMCL.H2O_FRACTION(value=0.0, unit="-"),
    CMCL.CO2_FRACTION(value=0.0, unit="-"),
    rel=CMCL.HAS_QUANTITATIVE_PROPERTY
)

untreated_exhaust.add(
    composition,
    rel=CMCL.HAS_PART
)

# Add the names of output quantities we want to get back
outputs = CMCL.OUTPUTS()
outputs.add(
    CMCL.OUT_NO_OUT(),
    CMCL.OUT_CO_OUT(),
    CMCL.OUT_C3H6_OUT(),
    rel=CMCL.HAS_PART)

# Initialise the main EAT process
eat_process = CMCL.EAT_PROCESS()
eat_process.add(
    twc,
    untreated_exhaust,
    rel=CMCL.HAS_PROPER_PARTICIPANT
)

# Add outputs
eat_process.add(outputs, rel=CMCL.HAS_PART)

# Construct an applicable engine instance
engine = EATEngine()

# Construct a wrapper and run a new session
with KineticsSession(engine) as session:
    wrapper = CMCL.wrapper(session=session)
    cb_synthesis_w = wrapper.add(eat_process, rel=CMCL.HAS_PART)
    wrapper.session.run()
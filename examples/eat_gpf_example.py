#
# This examples aims to run the EAT_GPF use case by hard-coding
# the input CUDS objects and passing them to the SimCMCLkineticsSession class
# for execution.
#

# Import CUDS objects generated from CMCL ontology
# pylint: disable=no-name-in-module
from osp.core import CMCL

# Import the session wrapper
from osp.wrappers.simcmclkinetics import SimCMCLkineticsSession

# Replicate the inputs.json of the use case; note that these values
# were taken from the following kinetics-backend commit:
# 28e848ac3ac5ce22d63ed4ca11af8273ad1b877f

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
    rel=CMCL.HAS_QUANTITATIVE_PROPERTY
)

# Multi-value as single string (fudge)
# NOTE - Looks like initialising this as a proper python multi-line
# string introduces additional line breaks (which would break the JSON),
# so you're getting a wide string.
psd_value = "0.0 \n 0.0 \n 0.0 \n 0.0 \n 0.0 \n 717336335.4961826 \n 1136584354.379982 \n 924227815.950944 \n 845311534.7779906 \n 356410402.48458695 \n 85584073.91376975 \n 987972758.5775461 \n 709085997.0099192 \n 266943816.34198743 \n 4915598091.457544 \n 7297012929.206079 \n 2787390572.980519 \n 148122061.65184438 \n 0.0 \n 0.0"

# Initialise the exhaust
untreated_exhaust = CMCL.UNTREATED_EXHAUST()

untreated_exhaust.add(
    CMCL.MASS_FLOW_RATE(value=72.3745273, unit="kg/h"),
    CMCL.TEMPERATURE(value=719.1521765499999, unit="K"),
    CMCL.PRESSURE(value=97835.26926, unit="Pa"),
    CMCL.PSD(value=psd_value, unit="#/kg"),
    rel=CMCL.HAS_QUANTITATIVE_PROPERTY
)

# Composition
composition = CMCL.INLET_GAS(unit="mole fraction")
composition.add(
    CMCL.O2_FRACTION(value=0.0077, unit="-"),
    CMCL.N2_FRACTION(value=0.97665, unit="-"),
    rel=CMCL.HAS_QUANTITATIVE_PROPERTY
)

untreated_exhaust.add(
    composition,
    rel=CMCL.HAS_PART
)

# Add the names of output quantities we want to get back
outputs = CMCL.OUTPUT_CONTAINER()
outputs.add(
    CMCL.OUT_PM_IN(),
    CMCL.OUT_PM_OUT(),
    CMCL.OUT_PN_IN(),
    CMCL.OUT_PN_OUT(),
    rel=CMCL.HAS_PART)

# Initialise the main EAT process
eat_process = CMCL.EAT_PROCESS()
eat_process.add(
    gpf,
    untreated_exhaust,
    rel=CMCL.HAS_PROPER_PARTICIPANT
)

# Add container for future outputs
eat_process.add(outputs, rel=CMCL.HAS_PART)

# Pretty print CUDS data for testing
#pretty_print(eat_process)

# Construct a wrapper and run a new session
with SimCMCLkineticsSession() as session:
    wrapper = CMCL.wrapper(session=session)
    cb_synthesis_w = wrapper.add(eat_process, rel=CMCL.HAS_PART)
    wrapper.session.run()
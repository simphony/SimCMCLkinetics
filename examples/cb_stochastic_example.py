# pylint: disable=no-name-in-module
from osp.core import CMCL
from osp.wrappers.simcmclkinetics import KineticsSession
from osp.wrappers.simcmclkinetics import CarbonBlackEngine

# This examples aims to run the CarbonBlack_StochasticSolver use case by hard-coding
# the input CUDS objects and passing them to the SimCMCLkineticsSession class
# for execution.
# Replicate the inputs.json of the use case; note that these values
# were taken from the following kinetics-backend commit:
# 28e848ac3ac5ce22d63ed4ca11af8273ad1b877f

# Grab the main entities
cb_synthesis = CMCL.CB_SYNTHESIS_PROCESS()
inlet_mixture = CMCL.INLET_GAS(unit="mole fraction")
cb_reactor = CMCL.CB_SYNTHESIS_REACTOR()
heterog_mixture = CMCL.PHASE_HETEROGENEOUS_REACTIVE_MIXTURE()
outputs = CMCL.OUTPUT_CONTAINER()

# Set the physical propeties of the reactor
cb_reactor.add(
    CMCL.LENGTH(value=1.0, unit="m"),
    CMCL.CROSS_SECTION(value=0.000201062, unit="m^2"),
    rel=CMCL.HAS_QUANTITATIVE_PROPERTY)

# Set the properties of the inlet mixture
inlet_mixture.add(
    CMCL.MASS_FLOW_RATE(value=5.82383E-05, unit="kg/s"),
    CMCL.C2H2_FRACTION(value=0.03, unit="-"),
    CMCL.C6H6_FRACTION(value=0.001, unit="-"),
    CMCL.N2_FRACTION(value=0.969, unit="-"),
    rel=CMCL.HAS_QUANTITATIVE_PROPERTY)

# Add physical quantities to the heterogeneous mixture
heterog_mixture.add(
    CMCL.PRESSURE(value=1.0, unit="atm"),
    rel=CMCL.HAS_QUANTITATIVE_PROPERTY)

# Add the names of output quantities we want to get back
outputs.add(
    CMCL.OUT_PART_SIZE_DISTR_Y(),
    CMCL.OUT_PART_SIZE_DISTR_X(),
    CMCL.OUT_PRIM_SIZE_DISTR_Y(),
    CMCL.OUT_PRIM_SIZE_DISTR_X(),
    CMCL.OUT_PART_AVG_FRACT_DIM(),
    rel=CMCL.HAS_PART)

# Add the heterogeneous mixture to the reactor
cb_reactor.add(heterog_mixture, rel=CMCL.HAS_PART)

# Setup the Carbon Black synthesis process
cb_synthesis.add(
    inlet_mixture, 
    cb_reactor, 
    rel=CMCL.HAS_PROPER_PARTICIPANT)

# Add container for future outputs
cb_synthesis.add(outputs, rel=CMCL.HAS_PART)

# Construct an applicable engine instance
engine = CarbonBlackEngine()

# Construct a wrapper and run a new session
with KineticsSession(engine) as session:
    wrapper = CMCL.wrapper(session=session)
    cb_synthesis_w = wrapper.add(cb_synthesis, rel=CMCL.HAS_PART)
    wrapper.session.run()
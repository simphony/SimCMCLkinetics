from osp.core.namespaces import CMCL
from osp.core.cuds import Cuds

def assemble_cb_synthesis() -> Cuds:
    # Grab the main entities
    cb_synthesis = CMCL.CB_SYNTHESIS_PROCESS()
    inlet_mixture = CMCL.INLET_GAS()
    cb_reactor = CMCL.CB_SYNTHESIS_REACTOR()
    heterog_mixture = CMCL.PHASE_HETEROGENEOUS_REACTIVE_MIXTURE()
    cb_powder = CMCL.CARBON_BLACK_POWDER()

    # Set the physical propeties of the reactor
    cb_reactor.add(
        CMCL.LENGTH(value=1.0, unit="m"),
        CMCL.CROSS_SECTION(value=0.000201062, unit="m^2"),
        rel=CMCL.HAS_QUANTITATIVE_PROPERTY)


    # Set the properties of the inlet mixture
    inlet_mixture.add(
        CMCL.MASS_FLOW_RATE(value=5.82383e-05, unit="kg/s"),
        CMCL.C2H2_FRACTION(value=0.03, unit="mole fraction"),
        CMCL.C6H6_FRACTION(value=0.001, unit="mole fraction"),
        CMCL.N2_FRACTION(value=0.969, unit="mole fraction"),
        rel=CMCL.HAS_QUANTITATIVE_PROPERTY)

    # Add physical quantities to the heterogeneous mixture
    heterog_mixture.add(
        CMCL.PRESSURE(value=1.0, unit="atm"),
        rel=CMCL.HAS_QUANTITATIVE_PROPERTY)

    # Add the heterogeneous mixture to the reactor
    cb_reactor.add(heterog_mixture, rel=CMCL.HAS_PART)

    # Setup the Carbon Black synthesis process
    cb_synthesis.add(
        inlet_mixture,
        cb_reactor,
        cb_powder,
        rel=CMCL.HAS_PROPER_PARTICIPANT)

    return cb_synthesis
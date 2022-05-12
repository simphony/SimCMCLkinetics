from osp.core.namespaces import CMCL
from osp.core.cuds import Cuds

def assemble_eat_twc() -> Cuds:
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
    composition = CMCL.INLET_GAS()
    composition.add(
        CMCL.C3H6_FRACTION(value=0.000450, unit="mole fraction"),
        CMCL.CO_FRACTION(value=0.014200, unit="mole fraction"),
        CMCL.NO_FRACTION(value=0.001000, unit="mole fraction"),
        CMCL.NO2_FRACTION(value=0.969, unit="mole fraction"),
        CMCL.O2_FRACTION(value=0.0077, unit="mole fraction"),
        CMCL.N2_FRACTION(value=0.97665, unit="mole fraction"),
        CMCL.H2O_FRACTION(value=0.0, unit="mole fraction"),
        CMCL.CO2_FRACTION(value=0.0, unit="mole fraction"),
        rel=CMCL.HAS_QUANTITATIVE_PROPERTY
    )

    untreated_exhaust.add(
        composition,
        rel=CMCL.HAS_PART
    )

    # Initialise the main EAT process
    eat_process = CMCL.EAT_PROCESS()
    eat_process.add(
        twc,
        untreated_exhaust,
        rel=CMCL.HAS_PROPER_PARTICIPANT
    )
    return eat_process
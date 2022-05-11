from osp.core.namespaces import CMCL
from osp.core.cuds import Cuds
import pytest


@pytest.fixture()
def carbon_black_cuds() -> Cuds:
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


@pytest.fixture()
def eat_gpf_cuds() -> Cuds:
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

    # Initialise the exhaust
    untreated_exhaust = CMCL.UNTREATED_EXHAUST()

    # Multi-value as single string (fudge)
    particle_psd = CMCL.PARTICLE_SIZE_DISTRIBUTION()
    particle_psd.add(CMCL.PARTICLE_NUMBER_DENSITIES(
                value_string=("1.39E+01,2.08E+04,3.64E+06, \
                            8.38E+06,1.20E+07,2.06E+07, \
                            1.30E+06,5.92E+03,8.55E+01"), unit="#/m3"),
            CMCL.PARTICLE_SIZE_CLASSES(
                value_string=("6.63E-01,7.28E-01,8.79E-01, \
                            9.65E-01,1.06E+00,1.28E+00, \
                            2.98E+00,3.28E+00,3.95E+00"), unit="nm"),
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
    return eat_process

@pytest.fixture()
def eat_twc_cuds() -> Cuds:
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
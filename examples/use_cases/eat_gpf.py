from osp.core.namespaces import CMCL
from osp.core.cuds import Cuds

# Initialise and set values for the GPF
def assemble_eat_gpf() -> Cuds:
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
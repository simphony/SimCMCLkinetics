from osp.core import CMCL
from osp.wrappers.simcmclkinetics import SimCMCLkineticsSession
import osp.core.utils.simple_search as search

# Create main entities
cb_synthesis = CMCL.CB_SYNTHESIS()
inlet_mixture = CMCL.INLET_GAS_MIXTURE()
cb_reactor = CMCL.CB_SYNTHESIS_REACTOR()
heterog_mixture = CMCL.PHASE_HETEROGENEOUS_REACTIVE_MIXTURE()

# Set inlet mixutre properties
inlet_mixture.add(CMCL.INLET_MASS_FLOW(value=1.0e-5,unit="kg/s"),
                  CMCL.C2H2_MASS_FRACTION(value=0.01,unit="-"),
                  CMCL.C6H6_MASS_FRACTION(value=0.02,unit="-"),
                  CMCL.N2_MASS_FRACTION(value=0.97,unit="-"),
                  rel=CMCL.HAS_QUANTITATIVE_PROPERTY)

# Set mixutre properties
heterog_mixture.add(CMCL.TEMPERATURE(value=1200.0,unit="K"),
                    CMCL.PRESSURE(value=1.0,unit="atm"),
                    CMCL.PARTICLE_NUMBER_DENSITY(value=0.0,unit="#/m^3"),
                    CMCL.MEAN_PARTICLE_SIZE(value=0.0,unit="nm"),
                    CMCL.PARTICLE_VOLUME_FRACTION(value=0.0,unit="-"),
                    rel=CMCL.HAS_QUANTITATIVE_PROPERTY)

# Set cb_reactor properties
cb_reactor.add(CMCL.LENGTH(value=1.0,unit="m"),
               CMCL.AREA(value=0.005,unit="m^2"),
               rel=CMCL.HAS_QUANTITATIVE_PROPERTY)

cb_reactor.add(heterog_mixture,
               rel=CMCL.HAS_PART)

# Set the cb synthesis process
cb_synthesis.add(inlet_mixture,
                 cb_reactor,
                 rel=CMCL.HAS_PROPER_PARTICIPANT)



# run a session
with SimCMCLkineticsSession() as s:
    w = CMCL.wrapper(session=s)
    cb_synthesis_w = w.add(cb_synthesis, rel=CMCL.HAS_PART)
    w.session.run()
#
#    react_gas_w = cb_reactor_w.get(oclass=CMCL.REACT_GAS)[0]
    gas_species = search.find_cuds_objects_by_oclass(CMCL.C2H2_MASS_FRACTION,cb_synthesis_w,rel=None)[0]
    gas_species.value = 0.04
    w.session.run()
from osp.core import CMCL
from osp.wrappers.simcmclkinetics import SimCMCLkineticsSession
import osp.core.utils.simple_search as search

# set the reacting gas mixture
def set_react_gas(sp_names_list, sp_conc_list, conc_unit):
    react_gas = CMCL.REACT_GAS()
    for sn, sc in zip(sp_names_list, sp_conc_list):
        sp = CMCL.GAS_SPECIES(name=sn)
        sp.add(CMCL.CONCENTRATION(value=sc,unit=conc_unit), rel=CMCL.HAS_PART)
        react_gas.add(sp, rel=CMCL.HAS_PART)
    return react_gas

# create carbon black reactor entity
cb_reactor = CMCL.CB_REACTOR()
react_gas = set_react_gas(["AR", "C6H6", "O2"], [0.8, 0.1, 0.1], "mass fraction")

cb_reactor.add(CMCL.LENGTH(value=2.0,unit="m"),
               CMCL.CROSS_SECT_AREA(value=0.05,unit="m^2"),
               CMCL.TEMPERATURE(value=1200.0,unit="K"),
               CMCL.PRESSURE(value=1,unit="bar"),
               CMCL.FLOWRATE(value=0.005,unit="kg/s"),
               CMCL.CB_PART(),
               react_gas, rel=CMCL.HAS_PART)

# run a session
with SimCMCLkineticsSession() as s:
    w = CMCL.wrapper(session=s)
    cb_reactor_w = w.add(cb_reactor, rel=CMCL.HAS_PART)
    w.session.run()

    react_gas_w = cb_reactor_w.get(oclass=CMCL.REACT_GAS)[0]
    gas_species = search.find_cuds_objects_by_attribute('name','AR',react_gas_w,rel=None)[0]
    gas_species.get(oclass=CMCL.CONCENTRATION)[0].value = 0.3
    w.session.run()
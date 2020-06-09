from osp.core import CMCL
from osp.core.session import SimWrapperSession
from osp.wrappers.simcmclkinetics import SimulationEngine

class SimCMCLkineticsSession(SimWrapperSession):
    """    """
    def __init__(self, engine=None, **kwargs):
        super().__init__(engine or SimulationEngine(), **kwargs)

    def __str__(self):
        return "CMCL kinetics wrapper session"

    # OVERRIDE
    def _apply_added(self, root_obj, buffer):
        for obj in buffer.values():
            if obj.is_a(CMCL.GAS_SPECIES):
                name = obj.name
                conc = obj.get(oclass=CMCL.CONCENTRATION)[0].value
                self._engine.add_gas_species(obj.uid, name, conc)

    # OVERRIDE
    def _apply_updated(self, root_obj, buffer):
        for obj in buffer.values():
            # check if name has been updated
            if obj.is_a(CMCL.CONCENTRATION):
                gas_spec = obj.get(rel=CMCL.IS_PART_OF)[0]
                self._engine.update_gas_species_conc(gas_spec.uid, obj.value)

            elif obj.is_a(CMCL.LENGTH):
                cb_reactor = obj.get(rel=CMCL.IS_PART_OF)[0]
                self._engine.update_length(cb_reactor.uid, obj.value)

            elif obj.is_a(CMCL.CROSS_SECT_AREA):
                cb_reactor = obj.get(rel=CMCL.IS_PART_OF)[0]
                self._engine.update_cross_sect_area(cb_reactor.uid, obj.value)

            elif obj.is_a(CMCL.TEMPERATURE):
                cb_reactor = obj.get(rel=CMCL.IS_PART_OF)[0]
                self._engine.update_temperature(cb_reactor.uid, obj.value)

            elif obj.is_a(CMCL.PRESSURE):
                cb_reactor = obj.get(rel=CMCL.IS_PART_OF)[0]
                self._engine.update_pressure(cb_reactor.uid, obj.value)

    # OVERRIDE
    def _apply_deleted(self, root_obj, buffer):
        """Deletes the deleted cuds from the engine."""
        for cuds_object in buffer.values():
            if cuds_object.is_a(CMCL.GAS_SPECIES):
                self._engine.remove_gas_species(cuds_object.uid)

    # OVERRIDE
    #def _initialise(self, root_obj):
    #    """ if initialisation is needed"""
    #    pass

    # OVERRIDE
    def _load_from_backend(self, uids, expired=None):
        for uid in uids:
            if uid in self._registry:
                yield self._registry.get(uid)
            else:
                yield None

    # OVERRIDE
    def _run(self, root_cuds_object):
        print("here you call the run method in the engine")

            
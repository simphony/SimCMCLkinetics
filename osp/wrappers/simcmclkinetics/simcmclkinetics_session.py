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
        pass

    # OVERRIDE
    def _apply_updated(self, root_obj, buffer):
        for obj in buffer.values():
            # update inlet mixture data
            if obj.is_a(CMCL.C2H2_MASS_FRACTION):
                inlet_mixture = obj.get(rel=CMCL.IS_QUANTITATIVE_PROPERTY)[0]
                self._engine.update_c2h2_massfrac(inlet_mixture.uid, obj.value)

            elif obj.is_a(CMCL.C6H6_MASS_FRACTION):
                inlet_mixture = obj.get(rel=CMCL.IS_QUANTITATIVE_PROPERTY)[0]
                self._engine.update_c6h6_massfrac(inlet_mixture.uid, obj.value)

            elif obj.is_a(CMCL.N2_MASS_FRACTION):
                inlet_mixture = obj.get(rel=CMCL.IS_QUANTITATIVE_PROPERTY)[0]
                self._engine.update_n2_massfrac(inlet_mixture.uid, obj.value)

            elif obj.is_a(CMCL.INLET_MASS_FLOW):
                inlet_mixture = obj.get(rel=CMCL.IS_QUANTITATIVE_PROPERTY)[0]
                self._engine.update_m_flow(inlet_mixture.uid, obj.value)

            # update heterog_mixture data
            elif obj.is_a(CMCL.TEMPERATURE):
                heterog_mixture = obj.get(rel=CMCL.IS_QUANTITATIVE_PROPERTY)[0]
                self._engine.update_temperature(heterog_mixture.uid, obj.value)

            elif obj.is_a(CMCL.PRESSURE):
                heterog_mixture = obj.get(rel=CMCL.IS_QUANTITATIVE_PROPERTY)[0]
                self._engine.update_pressure(heterog_mixture.uid, obj.value)

            elif obj.is_a(CMCL.PARTICLE_NUMBER_DENSITY):
                heterog_mixture = obj.get(rel=CMCL.IS_QUANTITATIVE_PROPERTY)[0]
                self._engine.update_part_num_dens(heterog_mixture.uid, obj.value)

            elif obj.is_a(CMCL.MEAN_PARTICLE_SIZE):
                heterog_mixture = obj.get(rel=CMCL.IS_QUANTITATIVE_PROPERTY)[0]
                self._engine.update_mean_part_size(heterog_mixture.uid, obj.value)

            elif obj.is_a(CMCL.PARTICLE_VOLUME_FRACTION):
                heterog_mixture = obj.get(rel=CMCL.IS_QUANTITATIVE_PROPERTY)[0]
                self._engine.update_part_vol_frac(heterog_mixture.uid, obj.value)

            # update cb reactor data
            elif obj.is_a(CMCL.LENGTH):
                cb_reactor = obj.get(rel=CMCL.IS_QUANTITATIVE_PROPERTY)[0]
                self._engine.update_length(cb_reactor.uid, obj.value)

            elif obj.is_a(CMCL.AREA):
                cb_reactor = obj.get(rel=CMCL.IS_QUANTITATIVE_PROPERTY)[0]
                self._engine.update_area(cb_reactor.uid, obj.value)

    # OVERRIDE
    def _apply_deleted(self, root_obj, buffer):
        """Deletes the deleted cuds from the engine."""
        pass
        #for cuds_object in buffer.values():
        #    if cuds_object.is_a():
        #        self._engine.remove_...(cuds_object.uid)

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

            
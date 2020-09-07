# Import CUDS objects generated from CMCL ontology
from osp.core import CMCL

# Import generic wrapper class from OSP core
from osp.core.session import SimWrapperSession

# Import CMCL SimulationEngine class
from osp.wrappers.simcmclkinetics import SimulationEngine


# Class to represent a single session of the wrapper (i.e. the process handling
# setup, execution, and retrieval of output data).
#
# Subclass of generic wrapper class SimWrapperSession (in OSP Core)
class SimCMCLkineticsSession(SimWrapperSession):
    
    # Initialises parent using a new SimulationEngine instance if none is supplied.
    def __init__(self, engine=None, **kwargs):
        super().__init__(engine or SimulationEngine(), **kwargs)

    # Return string representation
    def __str__(self):
        return "CMCL Kinetics wrapper session"

    # Overridden (does nothing)
    # Parent: Add the added cuds_objects to the engine
    def _apply_added(self, root_obj, buffer):
        # I suppose this method should be used if we need to add CUDS
        # objects to other CUDS objects?
        pass

    # Overridden
    # Parent: Update the updated cuds_objects in the engine
    def _apply_updated(self, root_obj, buffer):

        # Loop through each object in the buffer
        for obj in buffer.values():

            # If the object is a mass fraction, update its value
            # QUESTION 1, QUESTION 2, QUESTION 3
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

            # If the object is a physical quantity of the heterogenous mixture,
            # update its value
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

            # Update the physical properties of the Carbon Black reactor
            elif obj.is_a(CMCL.LENGTH):
                cb_reactor = obj.get(rel=CMCL.IS_QUANTITATIVE_PROPERTY)[0]
                self._engine.update_length(cb_reactor.uid, obj.value)

            elif obj.is_a(CMCL.AREA):
                cb_reactor = obj.get(rel=CMCL.IS_QUANTITATIVE_PROPERTY)[0]
                self._engine.update_area(cb_reactor.uid, obj.value)

    # Overrriden
    # Parent: Deletes the deleted cuds from the engine.
    def _apply_deleted(self, root_obj, buffer):
        # If we need do, delete objects from the CUDS structure here
        pass

    # Overriden
    # Parent: Load cuds_object with given uids from the database
    def _load_from_backend(self, uids, expired=None):
        for uid in uids:
            if uid in self._registry:
                yield self._registry.get(uid)
            else:
                yield None

    # Override
    # Parent: Run the engine
    def _run(self, root_cuds_object):
        self._engine.run()

            
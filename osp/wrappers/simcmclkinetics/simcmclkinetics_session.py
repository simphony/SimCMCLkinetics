# pylint: disable=no-name-in-module

# Import CUDS objects generated from CMCL ontology
from osp.core import CMCL

# Import generic wrapper class from OSP core
from osp.core.session import SimWrapperSession

# Import CMCL SimulationEngine class
from osp.wrappers.simcmclkinetics import SimulationEngine


class SimCMCLkineticsSession(SimWrapperSession):
    """Entry class for the kinetics simulation system. A single class instance
    handles setting up, running, and returning outputs from a single kinetics
    simulation.

    This should be the only class exposed to calling code.
    """
    

    def __init__(self, **kwargs):
        """Initialises the session and creates a new SimulationEngine instance.
        """
        super().__init__(SimulationEngine(), **kwargs)


    def __str__(self):
        """Returns a textual representation.

        Returns:
            Textual representation
        """
        return "CMCL Kinetics wrapper session"

    def forceRun(self, root_cuds_object):
        """Public testing method to foricbly run this instance.
        """
        self._run(root_cuds_object)

    def _run(self, root_cuds_object):
        """Run the engine to execute a kinetics simulation.

        Arguments:
            root_cuds_object -- Root CUDS object representing input data
        """
        self._engine.run(root_cuds_object)

    
    def _apply_added(self, root_obj, buffer):
        """Not used in the this concrete wrapper.

        Args:
            root_obj (Cuds): The wrapper cuds object
            buffer (Dict[UUID, Cuds]): All Cuds objects that have been added
        """
        pass


    def _apply_updated(self, root_obj, buffer):
        """Not used in the this concrete wrapper.

        Args:
            root_obj (Cuds): The wrapper cuds object
            buffer (Dict[UUID, Cuds]): All Cuds objects that have been updated
        """
        pass


    def _apply_deleted(self, root_obj, buffer):
        """Not used in the this concrete wrapper.

        Args:
            root_obj (Cuds): The wrapper cuds object.
            buffer (Dict[UUID, Cuds]): All Cuds objects that have been deleted
        """
        pass

    
    def _load_from_backend(self, uids, expired=None):
        """Not used in the this concrete wrapper.

        :param uids: List of uids to load
        :type uids: List[UUID]
        :param expired: Which of the cuds_objects are expired.
        :type expired: Set[UUID]
        """
        pass
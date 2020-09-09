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

    
    def _run(self, root_cuds_object):
        """Run the engine to execute a kinetics simulation.

        Arguments:
            root_cuds_object -- Root CUDS object representing input data
        """
        self._engine.run()

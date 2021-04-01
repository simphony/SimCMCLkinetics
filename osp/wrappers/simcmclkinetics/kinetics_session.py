import sys
import json
from osp.core.session import SimWrapperSession
from osp.core.utils import pretty_print

# pylint: disable=no-name-in-module
from osp.core.namespaces import CMCL
from osp.wrappers.simcmclkinetics import KineticsEngine
from osp.wrappers.simcmclkinetics import AgentBridge
from osp.wrappers.simcmclkinetics import CUDSAdaptor


class KineticsSession(SimWrapperSession):
    """This session class wraps a KineticsEngine instance, calls it, then passes the
    JSON data it has produced to an AgentBridge instance that runs the remote
    simulation with the Kinetics and SRM Engine Suite.
    """

    # Possible model flags
    CB_STOCHASIC = 1
    CB_MOMIC = 2
    EAT_GPF = 3
    EAT_TWC = 4

    # Current model flag
    modelFlag = 1

    def __init__(self, engine: KineticsEngine, **kwargs):
        """Initialises the session and creates a new SimulationEngine instance.

        Arguments:
            engine -- KineticsEngine instance
            kwargs -- Keyword arguments
        """

        # TODO - Do we expect an already instantiated KineticsEngine here,
        # or should we be creating it (if so, how to detect with concrete
        # engine class to use)?
        super().__init__(engine, **kwargs)


    def __str__(self):
        """Returns a textual representation.

        Returns:
            Textual representation
        """
        return "Kinetics Wrapper Session"


    def _run(self, root_cuds_object):
        """Runs the AgentBridge class to execute a remote Kinetics simulation.

        Note that once CUDS data is passed into this method, it should be
        considered READ-ONLY by any calling code outside this wrapper.

        Arguments:
            root_cuds_object -- Root CUDS object representing input data
        """
        print("")
        print("===== Start: KineticsSession =====")

        # Save a copy of the CUDS inputs
        inputs_file = open("input_results.txt", "w")
        pretty_print(root_cuds_object, inputs_file)
        inputs_file.close()
        print("CUDS representation of inputs written to: ./input_results.txt")

        # Determine template from root CUDS object
        simulation_template = self._engine.determineTemplate(root_cuds_object, self.modelFlag)

        # Use the engine to generate JSON inputs
        jsonInputs, synEntityToCUDSmap = self._engine.generateJSON(root_cuds_object, simulation_template)

        # Run remote simulation (via AgentBridge)
        agentBridge = AgentBridge()
        jsonResult = agentBridge.runJob(json.dumps(jsonInputs))

        # Pass results (in JSON form) back to the engine for parsing
        self._engine.parseResults(jsonResult, root_cuds_object, synEntityToCUDSmap)

        print("===== End: KineticsSession =====")
        print("")

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
        for uid in uids:
            if uid in self._registry:
                yield self._registry.get(uid)
            else:
                yield None


    def setModelFlag(self, flag):
        """Sets the flag determining the simulation model to use.

        Args:
            flag (integer): Integer representing model flag, see KineticsSession for possible values.
        """
        if (flag <= 0) or (flag > 4):
            raise ValueError("Invalid model flag!")

        # Store the flag
        self.modelFlag = flag
        print("Model flag changed to #" + str(self.modelFlag) + ".")


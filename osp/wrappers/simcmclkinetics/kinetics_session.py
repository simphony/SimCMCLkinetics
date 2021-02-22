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
        simulation_template = self._engine.determineTemplate(root_cuds_object)

        # Use the engine to generate JSON inputs
        jsonInputs, synEntityToCUDSmap = self._engine.generateJSON(root_cuds_object, simulation_template)

        #with open('inputs.json', 'w') as f:
        #    json.dump(jsonInputs, f)

        # Run remote simulation (via AgentBridge)
        agentBridge = AgentBridge()
        jsonResult = agentBridge.runJob(json.dumps(jsonInputs))

        #with open('twc_json_out.txt') as json_file:
        #    jsonResult = json.load(json_file)

        # cached momic results
        #jsonResult = json.loads(('{"$OUT_PART_VOLFRAC":{"unit":"-","value":[6.80018E-6]}, \
        #                "$OUT_MEAN_PART_DIAMETER":{"unit":"nm","value":[468.019]}, \
        #                "$OUT_PART_NUMBER":{"unit":"#","value":[6.81728E8]}}'))
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
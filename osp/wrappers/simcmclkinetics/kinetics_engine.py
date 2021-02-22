import json
from abc import ABC, abstractmethod

from osp.core.utils import pretty_print
import osp.core.utils.simple_search as search

# pylint: disable=no-name-in-module
from osp.core.namespaces import CMCL
from osp.wrappers.simcmclkinetics import AgentBridge
from osp.wrappers.simcmclkinetics import CUDSAdaptor
from osp.wrappers.simcmclkinetics.cuds_adaptor import CUDS_BIND

class KineticsEngine(ABC):
    """Abstract parent engine class. Manages the CUDS objects that contain the
    end-user materials modelling choices, discovers the information inside
    these data structures, and selects/executes the suitable workflow.

    The concrete implementations of this class should be the only ones exposed
    to the core platform.
    """

    # Class variables
    executed = False
    successful = False


    def __init__(self):
        """Initialise a new SimulationEngine instance.
        """
        print("New '" + self.__class__.__name__ + "' instantiated!")


    def __str__(self):
        """Textual representation.

        Returns:
            Textual representation.
        """
        return self.__class__.__name__


    def generateJSON(self, root_cuds_object, simulation_template):
        """Determines the correct simulation template, parses CUDS data into a
        JSON structure and returns it.

        Arguments:
            root_cuds_object -- Root CUDS object representing input data

        Returns:
            JSON data generated from input CUDS objects
        """
        self.executed = False

        # Build the JSON data from the CUDS objects
        jsonData = CUDSAdaptor.toJSON(root_cuds_object, simulation_template)
        print("JSON data successfully generated from CUDS objects.")
        return jsonData


    def parseResults(self, jsonResults, root_cuds_object, synEntityToCUDSmap):
        """Given the results of a remote simulation in JSON form, this
        function parses them in to CUDS objects.

        Arguments:
            jsonResults        -- Remote simulation results
            root_cuds_object   -- Root CUDS object representing input data
            synEntityToCUDSmap -- Dictionary which stores a mapping between syntacitc (key) output
                                  representation that engine understands and the concrete CUDS
                                  instance that the it is associated with
        """

        # TODO - Should we expect the originally input CUDS objects to contain
        # placeholders for the output data, or do we need to generate and append
        # new CUDS objects for them?
        if jsonResults is None:
            print("No valid simulation results detected, session has failed.")
            self.successful = False
        else:
            # Use the CUDSAdaptor to fill CUDS objects with results
            CUDSAdaptor.toCUDS(jsonResults, synEntityToCUDSmap)
            print("CUDS objects have now been populated with simulation results.")
            self.successful = True

        results = [res_dict[CUDS_BIND] for res_dict in list(synEntityToCUDSmap.values())]

        if results is not None:
            if len(results) == 0:
                print("Could not find OUTPUT_RESULTS instance in CUDS")
            else:
                outputs_file = open("output_results.txt", "w")
                for result_item in results:
                    pretty_print(result_item, outputs_file)
                outputs_file.close()
                print("CUDS representation of results written to: ./output_results.txt")

        else:
            print("Could not find CUDS results instances")

        # Mark as complete
        self.executed = True


    def hasExecuted(self) -> bool:
        """Returns true if this engine instance has been executed.

        Returns:
            Execution state
        """
        return self.executed


    def wasSuccessful(self) -> bool:
        """Returns true if the remote simulation completed successfully.

        Returns:
            Remote simulation state
        """
        return self.successful


    @abstractmethod
    def determineTemplate(self, root_cuds_object) -> str:
        """Determines which simulation template to use based on the input
        CUDS data.

        Arguments:
            root_cuds_object -- Root CUDS object representing input data

        Returns:
            Appropriate simulation template name
        """
        pass
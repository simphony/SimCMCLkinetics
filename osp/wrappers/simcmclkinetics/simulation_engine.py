# Import AgentBridge class
from osp.wrappers.simcmclkinetics import AgentBridge

# Import CUDSAdaptor class
from osp.wrappers.simcmclkinetics import CUDSAdaptor

import json

class SimulationEngine:
    """Central class that manages setting up, executing, and parsing outputs from
    a kinetics simulation.
    """

    
    def __init__(self):
        """Initialise a new SimulationEngine instance.
        """
        print("SimulationEngine instantiated!")


    def __str__(self):
        """Textual representation.

        Returns:
            Textual representation.
        """
        return "CMCL SimulationEngine"


    def run(self, root_cuds_object):
        """Sets up, executes, and parses outputs from a remote kinetics simulation.

        Arguments:
            root_cuds_object -- Root CUDS object representing input data
        """
        self.executed = False

        # TODO - Determine template from root CUDS object
        simulation_template = self.determineTemplate(root_cuds_object)

        # TODO - Build the JSON data from the CUDS objects (via CUDSTranslator)
        jsonData = CUDSAdaptor.toJSON(root_cuds_object, simulation_template)

        # TODO - Run remote simulation (via AgentBridge)
        agentBridge = AgentBridge()
        jsonResult = agentBridge.runJob(json.dumps(jsonData))

        if(jsonResult == None):
            # TODO - Return error somehow
            self.executed = True

        # TODO - Populate CUDS from JSON results (via JSONTranslator)
        CUDSAdaptor.toCUDS(jsonResult, root_cuds_object)

        # Mark as complete
        self.executed = True


    def determineTemplate(self, root_cuds_object):
        """Determines which simulation template to use based on the input 
        CUDS data.

        Arguments:
            root_cuds_object -- Root CUDS object representing input data

        Returns:
            Appropriate simulation template name (or index?)
        """

        # TODO - Implementation
        return 1
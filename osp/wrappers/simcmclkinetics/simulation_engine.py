# Import CUDS objects generated from CMCL ontology
# pylint: disable=no-name-in-module
from osp.core import CMCL

# Import AgentBridge class
from osp.wrappers.simcmclkinetics import AgentBridge

# Import CUDSAdaptor class
from osp.wrappers.simcmclkinetics import CUDSAdaptor

# CUDS search functionality
import osp.core.utils.simple_search as search

# Pretty print
from osp.core.utils import pretty_print

import json

class SimulationEngine:
    """Central class that manages setting up, executing, and parsing outputs
    from a kinetics simulation.
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

        # Determine template from root CUDS object
        simulation_template = self.determineTemplate(root_cuds_object)
        print("Detected simulation template as %s" % (simulation_template))

        # Build the JSON data from the CUDS objects (via CUDSTranslator)
        jsonData = CUDSAdaptor.toJSON(simulation_template, root_cuds_object)
            
        # Run remote simulation (via AgentBridge)
        agentBridge = AgentBridge()
        jsonResult = agentBridge.runJob(json.dumps(jsonData))

        if(jsonResult == None):
            # TODO- Return error somehow, populate special error
            # CUDS object?
            self.executed = True

        # Populate CUDS from JSON results (via JSONTranslator)
        CUDSAdaptor.toCUDS(jsonResult, root_cuds_object)

        # Print final CUDS objects for testing
        #pretty_print(root_cuds_object)

        # Mark as complete
        self.executed = True
        

    def determineTemplate(self, root_cuds_object) -> str:
        """Determines which simulation template to use based on the input 
        CUDS data.

        Arguments:
            root_cuds_object -- Root CUDS object representing input data

        Returns:
            Appropriate simulation template name 
        """

        # NOTE - This should probably be done by adding a template name object
        # to the ontology then reading that from the CUDS data. This method
        # forces me to add instances to the CUDS data that are not required
        # for the input JSON request (so I have to generate dummy data, then 
        # detect and remove it later).
        
        twc = search.find_cuds_objects_by_oclass(CMCL.TWC, root_cuds_object, rel=None)
        gpf = search.find_cuds_objects_by_oclass(CMCL.GPF, root_cuds_object, rel=None)
        cb = search.find_cuds_objects_by_oclass(CMCL.CB_SYNTHESIS_REACTOR, root_cuds_object, rel=None)

        if twc:
            return "EAT_TWC"
        elif gpf:
            return "EAT_GPF"
        elif cb:
            mom = search.find_cuds_objects_by_oclass(CMCL.MEAN_PARTICLE_SIZE,cb[0],rel=None)
            if mom:
                return "CarbonBlack_MoMICSolver"
            else:
                return "CarbonBlack_StochasticSolver"
        else:
            pass
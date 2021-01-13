import json
import osp.core.utils.simple_search as search

# pylint: disable=no-name-in-module
from osp.core.namespaces import CMCL
from osp.wrappers.simcmclkinetics import AgentBridge
from osp.wrappers.simcmclkinetics import CUDSAdaptor
from osp.wrappers.simcmclkinetics import KineticsEngine
from osp.core.utils import pretty_print


class EATEngine(KineticsEngine):
    """Engine handling data objects for the EAT use cases.
    """


    def determineTemplate(self, root_cuds_object) -> str:
        """Determines which simulation template to use based on the input 
        CUDS data.

        Arguments:
            root_cuds_object -- Root CUDS object representing input data

        Returns:
            Appropriate simulation template name 
        """

        # TODO - This will probably need revision once we know exactly 
        # what CUDS objects the core GUI will be passing to us.

        # Note - The incoming CUDS objects here should have come from a
        # EAT specific GUI page presented by the core platform.
        # This means that we can safely already assume it's one of the
        # two EAT use cases and ignore EAT.
        
        # Attempt to find the TWC and GPF objects
        twc = search.find_cuds_objects_by_oclass(CMCL.TWC, root_cuds_object, rel=None)
        gpf = search.find_cuds_objects_by_oclass(CMCL.GPF, root_cuds_object, rel=None)

        if twc:
            return "EAT_TWC"
        elif gpf:
            return "EAT_GPF"
        else:
            return "ERROR"
import json
import osp.core.utils.simple_search as search

# pylint: disable=no-name-in-module
from osp.core.namespaces import CMCL
from osp.wrappers.simcmclkinetics import AgentBridge
from osp.wrappers.simcmclkinetics import CUDSAdaptor
from osp.wrappers.simcmclkinetics import KineticsEngine
from osp.core.utils import pretty_print
import osp.wrappers.simcmclkinetics.agent_cases as agent_cases

class CarbonBlackEngine(KineticsEngine):
    """Engine handling data objects for the Carbon Black use cases.
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
        # Carbon Black specific GUI page presented by the core platform.
        # This means that we can safely already assume it's one of the
        # two Carbon Black use cases and ignore EAT.

        # Find the reactor object
        cb = search.find_cuds_objects_by_oclass(CMCL.CB_SYNTHESIS_REACTOR, root_cuds_object, rel=None)
        if cb is None:
            print("Could not determine which template to load, cancelling run.")
            return "ERROR"

        # Find the MoMIC object
        mom = search.find_cuds_objects_by_oclass(CMCL.MEAN_PARTICLE_SIZE,cb[0],rel=None)
        if mom:
            simulation_template = agent_cases.MOMIC
        else:
            simulation_template = agent_cases.STOCH

        print("Detected simulation template as %s" % (simulation_template.template))
        return simulation_template
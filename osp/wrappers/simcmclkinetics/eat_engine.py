import json
import osp.core.utils.simple_search as search

# pylint: disable=no-name-in-module
from osp.core.namespaces import CMCL
from osp.wrappers.simcmclkinetics import AgentBridge
from osp.wrappers.simcmclkinetics import CUDSAdaptor
from osp.wrappers.simcmclkinetics import KineticsEngine
from osp.wrappers.simcmclkinetics import KineticsSession
from osp.core.utils import pretty_print
import osp.wrappers.simcmclkinetics.agent_cases as agent_cases

class EATEngine(KineticsEngine):
    """Engine handling data objects for the EAT use cases.
    """


    def determineTemplate(self, root_cuds_object, modelFlag) -> str:
        """Determines which simulation template to use based on the input
        CUDS data.

        Arguments:
            root_cuds_object -- Root CUDS object representing input data
            modelFlag -- Integer for model (see KineticsSession for values)

        Returns:
            Appropriate simulation template name
        """

        if modelFlag == KineticsSession.EAT_GPF:
            # GPF
            simulation_template = agent_cases.EAT_GPF

        elif modelFlag == KineticsSession.EAT_TWC:
            # TWO
            simulation_template = agent_cases.EAT_TWC

        else:
            return "ERROR"

        print("Detected simulation template as %s" % (simulation_template.template))
        return simulation_template
      
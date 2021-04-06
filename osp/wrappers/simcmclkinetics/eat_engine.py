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

        # Find the EAT Process object
        eat_process = search.find_cuds_objects_by_oclass(
            CMCL.EAT_PROCESS,
            root_cuds_object,
            rel=CMCL.HAS_PART
        )[0]

        if modelFlag == KineticsSession.EAT_GPF:
            # GPF
            simulation_template = agent_cases.EAT_GPF

            # Find GPF object
            gpf = search.find_cuds_objects_by_oclass(
                CMCL.GPF, 
                eat_process, 
                rel=CMCL.HAS_PROPER_PARTICIPANT
            )[0]

            # Add outputs
            gpf.add(
                CMCL.PM_FILTRATION_EFFICIENCY(value=0.0, unit="-"),
                CMCL.PN_FILTRATION_EFFICIENCY(value=0., unit="-"),
                rel=CMCL.HAS_QUANTITATIVE_PROPERTY
            )

        elif modelFlag == KineticsSession.EAT_TWC:
            # TWC
            simulation_template = agent_cases.EAT_TWC

            # Find TWC object
            twc = search.find_cuds_objects_by_oclass(
                CMCL.TWC, 
                eat_process, 
                rel=CMCL.HAS_PROPER_PARTICIPANT
            )[0]

            # Add outputs
            twc.add(
                CMCL.NOX_CAPTURE_EFFICIENCY(value=0.0, unit="-"),
                CMCL.CO_CAPTURE_EFFICIENCY(value=0.0, unit="-"),
                CMCL.CXHY_CAPTURE_EFFICIENCY(value=0.0, unit="-"),
                rel=CMCL.HAS_QUANTITATIVE_PROPERTY
            )

        else:
            return "ERROR"

        print("Detected simulation template as %s" % (simulation_template.template))
        return simulation_template
      
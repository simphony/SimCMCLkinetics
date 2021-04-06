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

class CarbonBlackEngine(KineticsEngine):
    """Engine handling data objects for the Carbon Black use cases.
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

        # Find the CB Synthesis object
        cb_synthesis = search.find_cuds_objects_by_oclass(
            CMCL.CB_SYNTHESIS_PROCESS, 
            root_cuds_object, 
            rel=CMCL.HAS_PART
        )[0]

        # Find the CB Powder object
        cb_powder = search.find_cuds_objects_by_oclass(
            CMCL.CARBON_BLACK_POWDER,
            cb_synthesis,
            rel=CMCL.HAS_PROPER_PARTICIPANT
        )[0]

        if modelFlag == KineticsSession.CB_STOCHASIC:
            # Stochastic
            simulation_template = agent_cases.STOCH

            # Initialise the relevant outputs
            particle_psd = CMCL.PARTICLE_SIZE_DISTRIBUTION()
            particle_psd.add(
                CMCL.PARTICLE_NUMBER_DENSITIES(value_string="", unit=""),
                CMCL.PARTICLE_SIZE_CLASSES(value_string="", unit=""),
                rel=CMCL.HAS_QUANTITATIVE_PROPERTY
            )

            primary_psd = CMCL.PRIMARY_PARTICLE_SIZE_DISTRIBUTION()
            primary_psd.add(
                CMCL.PRIMARY_PARTICLE_NUMBER_DENSITIES(value_string="", unit=""),
                CMCL.PRIMARY_PARTICLE_SIZE_CLASSES(value_string="", unit=""),
                rel=CMCL.HAS_QUANTITATIVE_PROPERTY
            )
           
            # Add the outputs
            cb_powder.add(
                CMCL.PARTICLE_MEAN_FRACTAL_DIMENSION(value=0.0, unit=""),
                particle_psd,
                primary_psd,
                rel=CMCL.HAS_QUANTITATIVE_PROPERTY
            )

        elif modelFlag == KineticsSession.CB_MOMIC:
            # MoMIC
            simulation_template = agent_cases.MOMIC

            # Add new outputs
            cb_powder.add(
                CMCL.MEAN_PARTICLE_SIZE(value=0.0, unit = ""),
                CMCL.PARTICLE_NUMBER_DENSITY(value=0.0, unit = ""),
                CMCL.PARTICLE_VOLUME_FRACTION(value=0.0, unit = ""),
                rel=CMCL.HAS_QUANTITATIVE_PROPERTY
            )
            
        else:
            return "ERROR"

        print("Detected simulation template as %s" % (simulation_template.template))
        return simulation_template
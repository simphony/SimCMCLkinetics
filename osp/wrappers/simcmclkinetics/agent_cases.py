from osp.core.namespaces import CMCL
import osp.wrappers.simcmclkinetics.io_transf as iotransf

class SimCaseTemplate():
    def __init__(self, template='', inputs=[], outputs=[]):
        self.template = template
        self.inputs = inputs
        self.outputs = outputs


class IOSemSynMap():
    def __init__(self, semEntity=None, synValueEntity=None,
                 synUnitEntity=None, transFunc=None, transFuncInpDep=None,
                 transFuncOutDep=None):

        self.semEntity = semEntity
        self.synValueEntity = synValueEntity
        self.synUnitEntity = synUnitEntity
        self.transFunc = transFunc
        self.transFuncInpDep = transFuncInpDep
        self.transFuncOutDep = transFuncOutDep


MOMIC = SimCaseTemplate(
    template="CarbonBlack_MoMICSolver",

    inputs=[IOSemSynMap(semEntity=CMCL.LENGTH, synValueEntity='$INP_LENGTH_VALUE', synUnitEntity='$INP_LENGTH_UNIT'),
            IOSemSynMap(semEntity=CMCL.CROSS_SECTION, synValueEntity='$INP_CROSS_SECTION_VALUE', synUnitEntity='$INP_CROSS_SECTION_UNIT'),
            IOSemSynMap(semEntity=CMCL.MASS_FLOW_RATE, synValueEntity='$INP_MASS_FLOW_RATE_VALUE', synUnitEntity='$INP_MASS_FLOW_RATE_UNIT'),
            IOSemSynMap(semEntity=CMCL.PRESSURE, synValueEntity='$INP_PRESSURE_VALUE', synUnitEntity='$INP_PRESSURE_UNIT'),
            IOSemSynMap(semEntity=CMCL.C2H2_FRACTION, synValueEntity='$INP_MIX_COMP_C2H2_FRACTION', synUnitEntity='$INP_MIX_COMP_UNIT'),
            IOSemSynMap(semEntity=CMCL.C6H6_FRACTION, synValueEntity='$INP_MIX_COMP_C6H6_FRACTION', synUnitEntity='$INP_MIX_COMP_UNIT'),
            IOSemSynMap(semEntity=CMCL.N2_FRACTION, synValueEntity='$INP_MIX_COMP_N2_FRACTION', synUnitEntity='$INP_MIX_COMP_UNIT')],

    outputs=[IOSemSynMap(semEntity=CMCL.MEAN_PARTICLE_SIZE, synValueEntity=['$OUT_MEAN_PART_DIAMETER']),
             IOSemSynMap(semEntity=CMCL.PARTICLE_NUMBER_DENSITY, synValueEntity=['$OUT_PART_NUMBER']),
             IOSemSynMap(semEntity=CMCL.PARTICLE_VOLUME_FRACTION, synValueEntity=['$OUT_PART_VOLFRAC'])]
)

STOCH = SimCaseTemplate(
    template="CarbonBlack_StochasticSolver",

    inputs=[IOSemSynMap(semEntity=CMCL.LENGTH, synValueEntity='$INP_LENGTH_VALUE', synUnitEntity='$INP_LENGTH_UNIT'),
            IOSemSynMap(semEntity=CMCL.CROSS_SECTION, synValueEntity='$INP_CROSS_SECTION_VALUE', synUnitEntity='$INP_CROSS_SECTION_UNIT'),
            IOSemSynMap(semEntity=CMCL.MASS_FLOW_RATE, synValueEntity='$INP_MASS_FLOW_RATE_VALUE', synUnitEntity='$INP_MASS_FLOW_RATE_UNIT'),
            IOSemSynMap(semEntity=CMCL.PRESSURE, synValueEntity='$INP_PRESSURE_VALUE', synUnitEntity='$INP_PRESSURE_UNIT'),
            IOSemSynMap(semEntity=CMCL.C2H2_FRACTION, synValueEntity='$INP_MIX_COMP_C2H2_FRACTION', synUnitEntity='$INP_MIX_COMP_UNIT'),
            IOSemSynMap(semEntity=CMCL.C6H6_FRACTION, synValueEntity='$INP_MIX_COMP_C6H6_FRACTION', synUnitEntity='$INP_MIX_COMP_UNIT'),
            IOSemSynMap(semEntity=CMCL.N2_FRACTION, synValueEntity='$INP_MIX_COMP_N2_FRACTION', synUnitEntity='$INP_MIX_COMP_UNIT')
           ],

    outputs=[IOSemSynMap(semEntity=CMCL.PARTICLE_MEAN_FRACTAL_DIMENSION, synValueEntity=['$OUT_PART_AVG_FRACT_DIM']),
             IOSemSynMap(semEntity=CMCL.PARTICLE_NUMBER_DENSITIES, synValueEntity=['$OUT_PART_SIZE_DISTR_Y']),
             IOSemSynMap(semEntity=CMCL.PARTICLE_SIZE_CLASSES, synValueEntity=['$OUT_PART_SIZE_DISTR_X']),
             IOSemSynMap(semEntity=CMCL.PRIMARY_PARTICLE_NUMBER_DENSITIES, synValueEntity=['$OUT_PRIM_SIZE_DISTR_Y']),
             IOSemSynMap(semEntity=CMCL.PRIMARY_PARTICLE_SIZE_CLASSES, synValueEntity=['$OUT_PRIM_SIZE_DISTR_X'])
            ]
)

EAT_TWC = SimCaseTemplate(
    template="EAT_TWC",

    inputs=[IOSemSynMap(semEntity=CMCL.LENGTH, synValueEntity='$INP_LENGTH_VALUE', synUnitEntity='$INP_LENGTH_UNIT'),
            IOSemSynMap(semEntity=CMCL.DIAMETER, synValueEntity='$INP_DIAMETER_VALUE', synUnitEntity='$INP_DIAMETER_UNIT'),
            IOSemSynMap(semEntity=CMCL.CHANNEL_DENSITY, synValueEntity='$INP_CHANNEL_DENSITY_VALUE', synUnitEntity='$INP_CHANNEL_DENSITY_UNIT'),
            IOSemSynMap(semEntity=CMCL.WALL_THICKNESS, synValueEntity='$INP_WALL_THICKNESS_VALUE', synUnitEntity='$INP_WALL_THICKNESS_UNIT'),
            IOSemSynMap(semEntity=CMCL.CATALYST_SURFACE_MULT, synValueEntity='$INP_CATALYST_SURFACE_MULT_VALUE', synUnitEntity='$INP_CATALYST_SURFACE_MULT_UNIT'),
            IOSemSynMap(semEntity=CMCL.MASS_FLOW_RATE, synValueEntity='$INP_MASS_FLOW_RATE_VALUE', synUnitEntity='$INP_MASS_FLOW_RATE_UNIT'),
            IOSemSynMap(semEntity=CMCL.TEMPERATURE, synValueEntity='$INP_TEMPERATURE_VALUE', synUnitEntity='$INP_TEMPERATURE_UNIT'),
            IOSemSynMap(semEntity=CMCL.PRESSURE, synValueEntity='$INP_PRESSURE_VALUE', synUnitEntity='$INP_PRESSURE_UNIT'),
            IOSemSynMap(semEntity=CMCL.C3H6_FRACTION, synValueEntity='$INP_MIX_COMP_C3H6_FRACTION', synUnitEntity='$INP_MIX_COMP_UNIT'),
            IOSemSynMap(semEntity=CMCL.CO_FRACTION, synValueEntity='$INP_MIX_COMP_CO_FRACTION'),
            IOSemSynMap(semEntity=CMCL.NO_FRACTION, synValueEntity='$INP_MIX_COMP_NO_FRACTION'),
            IOSemSynMap(semEntity=CMCL.NO2_FRACTION, synValueEntity='$INP_MIX_COMP_NO2_FRACTION'),
            IOSemSynMap(semEntity=CMCL.O2_FRACTION, synValueEntity='$INP_MIX_COMP_O2_FRACTION'),
            IOSemSynMap(semEntity=CMCL.N2_FRACTION, synValueEntity='$INP_MIX_COMP_N2_FRACTION'),
            IOSemSynMap(semEntity=CMCL.H2O_FRACTION, synValueEntity='$INP_MIX_COMP_H2O_FRACTION'),
            IOSemSynMap(semEntity=CMCL.CO2_FRACTION, synValueEntity='$INP_MIX_COMP_CO2_FRACTION')
           ],

    outputs=[IOSemSynMap(semEntity=CMCL.NOX_CAPTURE_EFFICIENCY, synValueEntity=['$OUT_NO_OUT'],
                          transFunc=iotransf.getTWCCaptureEff, transFuncInpDep=['$INP_MIX_COMP_NO_FRACTION']),
             IOSemSynMap(semEntity=CMCL.CO_CAPTURE_EFFICIENCY, synValueEntity=['$OUT_CO_OUT'],
                          transFunc=iotransf.getTWCCaptureEff, transFuncInpDep=['$INP_MIX_COMP_CO_FRACTION']),
             IOSemSynMap(semEntity=CMCL.CXHY_CAPTURE_EFFICIENCY, synValueEntity=['$OUT_C3H6_OUT'],
                          transFunc=iotransf.getTWCCaptureEff, transFuncInpDep=['$INP_MIX_COMP_C3H6_FRACTION'])
            ]
)


EAT_GPF = SimCaseTemplate(
    template="EAT_GPF",

    inputs=[IOSemSynMap(semEntity=CMCL.LENGTH, synValueEntity='$INP_LENGTH_VALUE', synUnitEntity='$INP_LENGTH_UNIT'),
            IOSemSynMap(semEntity=CMCL.DIAMETER, synValueEntity='$INP_DIAMETER_VALUE', synUnitEntity='$INP_DIAMETER_UNIT'),
            IOSemSynMap(semEntity=CMCL.CHANNEL_DENSITY, synValueEntity='$INP_CHANNEL_DENSITY_VALUE', synUnitEntity='$INP_CHANNEL_DENSITY_UNIT'),
            IOSemSynMap(semEntity=CMCL.WALL_THICKNESS, synValueEntity='$INP_WALL_THICKNESS_VALUE', synUnitEntity='$INP_WALL_THICKNESS_UNIT'),
            IOSemSynMap(semEntity=CMCL.MASS_FLOW_RATE, synValueEntity='$INP_MASS_FLOW_RATE_VALUE', synUnitEntity='$INP_MASS_FLOW_RATE_UNIT'),
            IOSemSynMap(semEntity=CMCL.TEMPERATURE, synValueEntity='$INP_TEMPERATURE_VALUE', synUnitEntity='$INP_TEMPERATURE_UNIT'),
            IOSemSynMap(semEntity=CMCL.PRESSURE, synValueEntity='$INP_PRESSURE_VALUE', synUnitEntity='$INP_PRESSURE_UNIT'),
            IOSemSynMap(semEntity=CMCL.PERMEABILITY, synValueEntity='$INP_PERMEABILITY_VALUE', synUnitEntity='$INP_PERMEABILITY_UNIT'),
            IOSemSynMap(semEntity=CMCL.PORE_DIAMETER, synValueEntity='$INP_PORE_DIAMETER_VALUE', synUnitEntity='$INP_PORE_DIAMETER_UNIT'),
            IOSemSynMap(semEntity=CMCL.WALL_POROSITY, synValueEntity='$INP_WALL_POROSITY_VALUE', synUnitEntity='$INP_WALL_POROSITY_UNIT'),
            IOSemSynMap(semEntity=CMCL.PSD, synValueEntity='$INP_PSD_VALUE', synUnitEntity='$INP_PSD_UNIT'),
            IOSemSynMap(semEntity=CMCL.O2_FRACTION, synValueEntity='$INP_MIX_COMP_O2_FRACTION', synUnitEntity='$INP_MIX_COMP_UNIT'),
            IOSemSynMap(semEntity=CMCL.N2_FRACTION, synValueEntity='$INP_MIX_COMP_N2_FRACTION'),
            IOSemSynMap(semEntity=[CMCL.PARTICLE_NUMBER_DENSITIES, CMCL.PARTICLE_SIZE_CLASSES], synValueEntity='$INP_PSD_VALUE', synUnitEntity='$INP_PSD_UNIT',
                                   transFunc=iotransf.getPSD, transFuncInpDep = ['$INP_TEMPERATURE_VALUE',
                                                                                 '$INP_PRESSURE_VALUE'])
           ],

    outputs=[IOSemSynMap(semEntity=CMCL.PM_FILTRATION_EFFICIENCY, synValueEntity=['$OUT_PM_IN', '$OUT_PM_OUT'],transFunc=iotransf.getGPFFiltrationEff),
             IOSemSynMap(semEntity=CMCL.PN_FILTRATION_EFFICIENCY, synValueEntity=['$OUT_PN_IN', '$OUT_PN_OUT'],transFunc=iotransf.getGPFFiltrationEff)
            ]
)
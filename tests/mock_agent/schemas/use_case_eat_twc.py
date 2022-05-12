
from marshmallow import Schema, fields, validate
from . import use_case_base

class EAT_TWC_InputsSchema(Schema):
    INP_LENGTH_VALUE = fields.String(data_key="$INP_LENGTH_VALUE", required=True)
    INP_LENGTH_UNIT = fields.String(data_key="$INP_LENGTH_UNIT", required=True)
    INP_DIAMETER_VALUE = fields.String(data_key="$INP_DIAMETER_VALUE", required=True)
    INP_DIAMETER_UNIT = fields.String(data_key="$INP_DIAMETER_UNIT", required=True)
    INP_CHANNEL_DENSITY_VALUE = fields.String(data_key="$INP_CHANNEL_DENSITY_VALUE", required=True)
    INP_CHANNEL_DENSITY_UNIT = fields.String(data_key="$INP_CHANNEL_DENSITY_UNIT", required=True)
    INP_WALL_THICKNESS_VALUE = fields.String(data_key="$INP_WALL_THICKNESS_VALUE", required=True)
    INP_WALL_THICKNESS_UNIT = fields.String(data_key="$INP_WALL_THICKNESS_UNIT", required=True)
    INP_CATALYST_SURFACE_MULT_VALUE = fields.String(data_key="$INP_CATALYST_SURFACE_MULT_VALUE", required=True)
    INP_CATALYST_SURFACE_MULT_UNIT = fields.String(data_key="$INP_CATALYST_SURFACE_MULT_UNIT", required=True)
    INP_MASS_FLOW_RATE_VALUE = fields.String(data_key="$INP_MASS_FLOW_RATE_VALUE", required=True)
    INP_MASS_FLOW_RATE_UNIT = fields.String(data_key="$INP_MASS_FLOW_RATE_UNIT", required=True)
    INP_TEMPERATURE_VALUE = fields.String(data_key="$INP_TEMPERATURE_VALUE", required=True)
    INP_TEMPERATURE_UNIT = fields.String(data_key="$INP_TEMPERATURE_UNIT", required=True)
    INP_PRESSURE_VALUE = fields.String(data_key="$INP_PRESSURE_VALUE", required=True)
    INP_PRESSURE_UNIT = fields.String(data_key="$INP_PRESSURE_UNIT", required=True)
    INP_MIX_COMP_UNIT = fields.String(data_key="$INP_MIX_COMP_UNIT", required=True)
    INP_MIX_COMP_C3H6_FRACTION = fields.String(data_key="$INP_MIX_COMP_C3H6_FRACTION", required=True)
    INP_MIX_COMP_CO_FRACTION = fields.String(data_key="$INP_MIX_COMP_CO_FRACTION", required=True)
    INP_MIX_COMP_NO_FRACTION = fields.String(data_key="$INP_MIX_COMP_NO_FRACTION", required=True)
    INP_MIX_COMP_NO2_FRACTION = fields.String(data_key="$INP_MIX_COMP_NO2_FRACTION", required=True)
    INP_MIX_COMP_O2_FRACTION = fields.String(data_key="$INP_MIX_COMP_O2_FRACTION", required=True)
    INP_MIX_COMP_N2_FRACTION = fields.String(data_key="$INP_MIX_COMP_N2_FRACTION", required=True)
    INP_MIX_COMP_H2O_FRACTION = fields.String(data_key="$INP_MIX_COMP_H2O_FRACTION", required=True)
    INP_MIX_COMP_CO2_FRACTION = fields.String(data_key="$INP_MIX_COMP_CO2_FRACTION", required=True)

class EAT_TWC_UseCaseSchema(use_case_base.BaseUseCaseSchema):
    Inputs = fields.Nested(EAT_TWC_InputsSchema)
    Outputs = fields.List(
                fields.String(
                    required=True,
                    validate=validate.OneOf(
                        [
                            "$OUT_NO_OUT",
                            "$OUT_CO_OUT",
                            "$OUT_C3H6_OUT"
                        ]
                    )
                ),
                required=True
            )
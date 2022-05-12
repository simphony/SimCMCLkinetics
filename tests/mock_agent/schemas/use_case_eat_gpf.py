
from marshmallow import Schema, fields, validate
from . import use_case_base

class EAT_GPF_InputsSchema(Schema):
    INP_LENGTH_VALUE = fields.String(data_key="$INP_LENGTH_VALUE", required=True)
    INP_LENGTH_UNIT = fields.String(data_key="$INP_LENGTH_UNIT", required=True)
    INP_DIAMETER_VALUE = fields.String(data_key="$INP_DIAMETER_VALUE", required=True)
    INP_DIAMETER_UNIT = fields.String(data_key="$INP_DIAMETER_UNIT", required=True)
    INP_CHANNEL_DENSITY_VALUE = fields.String(data_key="$INP_CHANNEL_DENSITY_VALUE", required=True)
    INP_CHANNEL_DENSITY_UNIT = fields.String(data_key="$INP_CHANNEL_DENSITY_UNIT", required=True)
    INP_WALL_THICKNESS_VALUE = fields.String(data_key="$INP_WALL_THICKNESS_VALUE", required=True)
    INP_WALL_THICKNESS_UNIT = fields.String(data_key="$INP_WALL_THICKNESS_UNIT", required=True)
    INP_PERMEABILITY_VALUE = fields.String(data_key="$INP_PERMEABILITY_VALUE", required=True)
    INP_PERMEABILITY_UNIT = fields.String(data_key="$INP_PERMEABILITY_UNIT", required=True)
    INP_PORE_DIAMETER_VALUE = fields.String(data_key="$INP_PORE_DIAMETER_VALUE", required=True)
    INP_PORE_DIAMETER_UNIT = fields.String(data_key="$INP_PORE_DIAMETER_UNIT", required=True)
    INP_WALL_POROSITY_VALUE = fields.String(data_key="$INP_WALL_POROSITY_VALUE", required=True)
    INP_WALL_POROSITY_UNIT = fields.String(data_key="$INP_WALL_POROSITY_UNIT", required=True)
    INP_MASS_FLOW_RATE_VALUE = fields.String(data_key="$INP_MASS_FLOW_RATE_VALUE", required=True)
    INP_MASS_FLOW_RATE_UNIT = fields.String(data_key="$INP_MASS_FLOW_RATE_UNIT", required=True)
    INP_TEMPERATURE_VALUE = fields.String(data_key="$INP_TEMPERATURE_VALUE", required=True)
    INP_TEMPERATURE_UNIT = fields.String(data_key="$INP_TEMPERATURE_UNIT", required=True)
    INP_PRESSURE_VALUE = fields.String(data_key="$INP_PRESSURE_VALUE", required=True)
    INP_PRESSURE_UNIT = fields.String(data_key="$INP_PRESSURE_UNIT", required=True)
    INP_PSD_UNIT = fields.String(data_key="$INP_PSD_UNIT", required=True)
    INP_PSD_VALUE = fields.String(data_key="$INP_PSD_VALUE", required=True)

class EAT_GPF_UseCaseSchema(use_case_base.BaseUseCaseSchema):
    Inputs = fields.Nested(EAT_GPF_InputsSchema)
    Outputs = fields.List(
                fields.String(
                    required=True,
                    validate=validate.OneOf(
                        [
                            "$OUT_PM_IN",
                            "$OUT_PM_OUT",
                            "$OUT_PN_IN",
                            "$OUT_PN_OUT"
                        ]
                    )
                ),
                required=True
            )
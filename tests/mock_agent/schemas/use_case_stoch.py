
from marshmallow import Schema, fields, validate
from . import use_case_base

class StochasticInputsSchema(Schema):
    INP_LENGTH_VALUE = fields.String(data_key="$INP_LENGTH_VALUE", required=True)
    INP_LENGTH_UNIT = fields.String(data_key="$INP_LENGTH_UNIT", required=True)
    INP_CROSS_SECTION_VALUE = fields.String(data_key="$INP_CROSS_SECTION_VALUE", required=True)
    INP_CROSS_SECTION_UNIT = fields.String(data_key="$INP_CROSS_SECTION_UNIT", required=True)
    INP_MASS_FLOW_RATE_VALUE = fields.String(data_key="$INP_MASS_FLOW_RATE_VALUE", required=True)
    INP_MASS_FLOW_RATE_UNIT = fields.String(data_key="$INP_MASS_FLOW_RATE_UNIT", required=True)
    INP_PRESSURE_VALUE = fields.String(data_key="$INP_PRESSURE_VALUE", required=True)
    INP_PRESSURE_UNIT = fields.String(data_key="$INP_PRESSURE_UNIT", required=True)
    INP_MIX_COMP_UNIT = fields.String(data_key="$INP_MIX_COMP_UNIT", required=True)
    INP_MIX_COMP_C6H6_FRACTION = fields.String(data_key="$INP_MIX_COMP_C6H6_FRACTION", required=True)
    INP_MIX_COMP_C2H2_FRACTION = fields.String(data_key="$INP_MIX_COMP_C2H2_FRACTION", required=True)
    INP_MIX_COMP_N2_FRACTION = fields.String(data_key="$INP_MIX_COMP_N2_FRACTION", required=True)

class StochasticUseCaseSchema(use_case_base.BaseUseCaseSchema):
    Inputs = fields.Nested(StochasticInputsSchema)
    Outputs = fields.List(
                fields.String(
                    validate=validate.OneOf(
                        [
                            "$OUT_PART_SIZE_DISTR_Y",
                            "$OUT_PART_SIZE_DISTR_X",
                            "$OUT_PRIM_SIZE_DISTR_Y",
                            "$OUT_PRIM_SIZE_DISTR_X",
                            "$OUT_PART_AVG_FRACT_DIM"
                        ]
                    ),
                    required=True,
                ),
                required=True,
            )
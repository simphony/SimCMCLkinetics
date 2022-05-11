
from marshmallow import Schema, fields, validate
from . import use_case_base

class MomicInputsSchema(Schema):
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

class MomicUseCaseSchema(use_case_base.BaseUseCaseSchema):
    Inputs = fields.Nested(MomicInputsSchema)
    Outputs = fields.List(
                fields.String(
                    required=True,
                    validate=validate.OneOf(
                        [
                            "$OUT_MEAN_PART_DIAMETER",
                            "$OUT_PART_NUMBER",
                            "$OUT_PART_NUMBER_DENS",
                            "$OUT_PART_VOLFRAC"
                        ]
                    )
                ),
                required=True
            )
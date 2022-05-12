import json
import pytest

@pytest.fixture()
def momic_inputs() -> str:
    return json.dumps(
            {
                "Case": "CarbonBlack_MoMICSolver",
                "Inputs": {
                    "$INP_LENGTH_VALUE": "1.0",
                    "$INP_LENGTH_UNIT": "m",
                    "$INP_CROSS_SECTION_VALUE": "0.000201062",
                    "$INP_CROSS_SECTION_UNIT": "m^2",
                    "$INP_MASS_FLOW_RATE_VALUE": "5.82383E-05",
                    "$INP_MASS_FLOW_RATE_UNIT": "kg/s",
                    "$INP_PRESSURE_VALUE": "1.0",
                    "$INP_PRESSURE_UNIT": "atm",
                    "$INP_MIX_COMP_UNIT": "mole fraction",
                    "$INP_MIX_COMP_C6H6_FRACTION": "0.001",
                    "$INP_MIX_COMP_C2H2_FRACTION": "0.03",
                    "$INP_MIX_COMP_N2_FRACTION": "0.969"
                },
                "Outputs":[
                    "$OUT_MEAN_PART_DIAMETER",
                    "$OUT_PART_NUMBER_DENS",
                    "$OUT_PART_VOLFRAC"
                ]
            }
        )

@pytest.fixture()
def stoch_inputs() -> str:
    return json.dumps(
            {
                "Case": "CarbonBlack_StochasticSolver",
                "Inputs": {
                    "$INP_LENGTH_VALUE": "1.0",
                    "$INP_LENGTH_UNIT": "m",
                    "$INP_CROSS_SECTION_VALUE": "0.000201062",
                    "$INP_CROSS_SECTION_UNIT": "m^2",
                    "$INP_MASS_FLOW_RATE_VALUE": "5.82383E-05",
                    "$INP_MASS_FLOW_RATE_UNIT": "kg/s",
                    "$INP_PRESSURE_VALUE": "1.0",
                    "$INP_PRESSURE_UNIT": "atm",
                    "$INP_MIX_COMP_UNIT": "mole fraction",
                    "$INP_MIX_COMP_C6H6_FRACTION": "0.001",
                    "$INP_MIX_COMP_C2H2_FRACTION": "0.03",
                    "$INP_MIX_COMP_N2_FRACTION": "0.969"
                },
                "Outputs":[
                    "$OUT_PART_SIZE_DISTR_Y",
                    "$OUT_PART_SIZE_DISTR_X",
                    "$OUT_PRIM_SIZE_DISTR_Y",
                    "$OUT_PRIM_SIZE_DISTR_X",
                    "$OUT_PART_AVG_FRACT_DIM"
                ]
            }
    )
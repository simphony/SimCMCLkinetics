from sys import exc_info
from flask import Blueprint, request
from flask import current_app
from ..schemas import (
    get_outputs,
    use_case_base,
    use_case_momic,
    use_case_stoch,
    use_case_eat_twc,
    use_case_eat_gpf
)
from pprint import pformat
import json
import uuid
from typing import Dict

class InputSchemaException(Exception):
    """Raise if input does not match the schema."""

class UnsupportedCaseException(Exception):
    """Raise if the request case is not supported."""

# Blueprint Configuration
kinetics_agent_bp = Blueprint("kinetics_agent_bp", __name__)

JOB_INPUTS = {}
SUPPORTED_CASES = [
    'CarbonBlack_MoMICSolver',
    'CarbonBlack_StochasticSolver',
    'EAT_TWC',
    'EAT_GPF']

# Show an instructional message at the app root
@kinetics_agent_bp.route("/request", methods=["GET"])
def runSimulation():
    current_app.logger.debug("runSimulation call")
    current_app.logger.debug(f"request.args['query'] = {request.args['query']}")
    query = json.loads(request.args["query"])

    # this validates inputs against the base schema
    error = use_case_base.BaseUseCaseSchema().validate(query)
    if error:
        msg = "Incorrect inputs query."
        current_app.logger.debug(f"{msg} Details: {error}")
        return msg, 422

    jobId = str(uuid.uuid4())

    current_app.logger.debug("jsonified query:")
    current_app.logger.debug(pformat(query))
    outputs = {}
    try:
        outputs = _run_case(inputs=query)
    except UnsupportedCaseException as e:
        msg = "Requested Case is not supported."
        current_app.logger.exception(msg=msg, exc_info=e)
        return msg, 422
    except InputSchemaException as e:
        msg = "Invalid Case Inputs/Ouptuts specification."
        current_app.logger.exception(msg=msg, exc_info=e)
        return msg, 422
    except Exception as e:
        msg = "Problem with generating the results."
        current_app.logger.exception(msg=msg, exc_info=e)
        return msg, 400

    current_app.logger.debug("Generated outputs:")
    current_app.logger.debug(pformat(outputs))

    JOB_INPUTS[jobId] = outputs
    return {"jobId": jobId}, 200

def _run_case(inputs: Dict) -> Dict:
    case = inputs['Case']
    if case == 'CarbonBlack_MoMICSolver':
        generate_outputs_func = _generate_momic_outputs
    elif case == 'CarbonBlack_StochasticSolver':
        generate_outputs_func = _generate_stoch_outputs
    elif case == 'EAT_TWC':
        generate_outputs_func = _generate_eat_twc_outputs
    elif case == 'EAT_GPF':
        generate_outputs_func = _generate_eat_gpf_outputs
    else:
        raise UnsupportedCaseException(
            (
                f"Error: Selected Case: {inputs['Case']} is not supported. "
                f"Please choose from the following options: {SUPPORTED_CASES}."
            )
        )
    outputs = generate_outputs_func(inputs=inputs)
    return outputs

# Show an instructional message at the app root
@kinetics_agent_bp.route("/output/request", methods=["GET"])
def getOutputs():
    query = json.loads(request.args["query"])

    # this validates get outputs query
    error = get_outputs.GetOutputsSchema().validate(query)
    if error:
        msg = "Incorrect get output query."
        current_app.logger.debug(f"{msg} Details: {error}")
        return msg, 422

    jobId = query["jobId"]
    outputs = {}
    try:
        outputs = JOB_INPUTS.pop(jobId)
    except KeyError as e:
        msg = f"The requested job: {jobId} does not exist."
        current_app.logger.exception(msg, exc_info=e)
        return msg, 422
    return outputs, 200


def _generate_momic_outputs(inputs: Dict) -> Dict:
    error = use_case_momic.MomicUseCaseSchema().validate(inputs)
    if error:
        raise InputSchemaException(f"Error: Incorrect MoMIC inputs: {error}")
    return json.loads("""{
                "$OUT_MEAN_PART_DIAMETER": {
                    "value": [
                        62.2685
                    ],
                    "unit": "nm"
                },
                "$OUT_PART_VOLFRAC": {
                    "value": [
                        6.155939999999999e-7
                    ],
                    "unit": "-"
                },
                "$OUT_PART_NUMBER_DENS": {
                    "value": [
                        0.0,
                        1.45514e-25,
                        1.0444499999999999e-21,
                        2.3982599999999997e-20
                    ],
                    "unit": "#/m^3"
                }
            }""")


def _generate_stoch_outputs(inputs: Dict) -> Dict:
    error = use_case_stoch.StochasticUseCaseSchema().validate(inputs)
    if error:
        raise InputSchemaException(f"Error: Incorrect Stochastic inputs: {error}")
    return json.loads("""
            {
                "$OUT_PART_SIZE_DISTR_Y": {
                    "value": [
                        9.999999999999999e-31,
                        9.999999999999999e-31,
                        9.999999999999999e-31,
                        9.999999999999999e-31,
                        2.31065e-19,
                        85642700.0,
                        1807830000.0,
                        951688000.0,
                        70.8509,
                        9.999999999999999e-31
                    ],
                    "unit": "#/cm^3"
                },
                "$OUT_PART_SIZE_DISTR_X": {
                    "value": [
                        1.0,
                        1.9966400000000002,
                        3.9865800000000005,
                        7.95978,
                        15.8928,
                        31.7323,
                        63.358,
                        126.50299999999999,
                        252.582,
                        504.316
                    ],
                    "unit": "nm"
                },
                "$OUT_PRIM_SIZE_DISTR_Y": {
                    "value": [
                        3.22612e-17,
                        111126000.0,
                        1267780000.0,
                        706795000.0,
                        175969000.0,
                        727096000.0,
                        2669150000.0,
                        3.18379e-14,
                        9.999999999999999e-31,
                        9.999999999999999e-31
                    ],
                    "unit": "#/cm^3"
                },
                "$OUT_PRIM_SIZE_DISTR_X": {
                    "value": [
                        1.0,
                        1.9966400000000002,
                        3.9865800000000005,
                        7.95978,
                        15.8928,
                        31.7323,
                        63.358,
                        126.50299999999999,
                        252.582,
                        504.316
                    ],
                    "unit": "nm"
                },
                "$OUT_PART_AVG_FRACT_DIM": {
                    "value": [
                        2.3751700000000002
                        ],
                    "unit": "-"
                }
            }
            """)

def _generate_eat_twc_outputs(inputs: Dict) -> Dict:
    error = use_case_eat_twc.EAT_TWC_UseCaseSchema().validate(inputs)
    if error:
        raise InputSchemaException(f"Error: Incorrect Stochastic inputs: {error}")
    return json.loads("""
            {
                "$OUT_NO_OUT": {
                    "value": [
                        0.0,
                        3.1357159999999994e-43,
                        5.385191e-37,
                        7.060616e-30,
                        9.849207999999998e-22,
                        4.689654e-12,
                        0.0003701335
                    ],
                    "unit": "-"
                },
                "$OUT_CO_OUT": {
                    "value": [
                        0.0,
                        4.2593360000000004e-24,
                        1.499715e-16,
                        3.257333e-16,
                        5.299159e-16,
                        5.171069e-10,
                        0.009207145
                    ],
                    "unit": "-"
                },
                "$OUT_C3H6_OUT": {
                    "value": [
                        0.0,
                        4.3507179999999995e-40,
                        1.326385e-32,
                        2.2670309999999998e-26,
                        4.441866e-18,
                        5.664421e-11,
                        0.00021589799999999999
                    ],
                    "unit": "-"
                }
            }
            """)

def _generate_eat_gpf_outputs(inputs: Dict) -> Dict:
    error = use_case_eat_gpf.EAT_GPF_UseCaseSchema().validate(inputs)
    if error:
        raise InputSchemaException(f"Error: Incorrect Stochastic inputs: {error}")
    return json.loads("""
            {
                "$OUT_PM_IN": {
                    "value": [
                        4.18471e-09,
                        4.18471e-09,
                        4.18471e-09,
                        4.18471e-09,
                        4.18471e-09,
                        4.18471e-09,
                        4.18471e-09,
                        4.18471e-09,
                        4.18471e-09
                    ],
                    "unit": "kg/s"
                },
                "$OUT_PM_OUT": {
                    "value": [
                        0.0,
                        1.98075e-38,
                        1.1004e-29,
                        4.91931e-23,
                        9.731060000000001e-14,
                        1.04121e-09,
                        1.71433e-09,
                        1.71537e-09,
                        1.71403e-09
                    ],
                    "unit": "kg/s"
                },
                "$OUT_PN_IN": {
                    "value": [
                        0.0,
                        3.3179,
                        19.6466,
                        67.3381,
                        187.513,
                        192.405,
                        192.405,
                        192.405,
                        192.405
                    ],
                    "unit": "#"
                },
                "$OUT_PN_OUT": {
                    "value": [
                        0.0,
                        5.58811e-28,
                        2.97848e-19,
                        1.2991e-12,
                        0.00257282,
                        27.6361,
                        45.6641,
                        45.6921,
                        45.654
                    ],
                    "unit": "#"
                }
            }
            """)
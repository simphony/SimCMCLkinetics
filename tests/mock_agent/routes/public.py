from sys import exc_info
from flask import Blueprint, request
from flask import current_app
from ..schemas import use_case_base, use_case_momic, use_case_stoch
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
SUPPORTED_CASES = ['CarbonBlack_MoMICSolver', 'CarbonBlack_StochasticSolver']

# Show an instructional message at the app root
@kinetics_agent_bp.route("/request", methods=["GET"])
def runSimulation():
    current_app.logger.debug("runSimulation call")
    current_app.logger.debug(f"request.args['query'] = {request.args['query']}")
    query = json.loads(request.args["query"])

    # this validates inputs against the base schema
    error = use_case_base.BaseUseCaseSchema().validate(query)
    if error:
        current_app.logger.debug(f"Error: Incorrect inputs: {error}")
        return error, 400

    jobId = str(uuid.uuid4())

    current_app.logger.debug("jsonified query:")
    current_app.logger.debug(pformat(query))
    outputs = {}
    try:
        outputs = _run_case(inputs=query)
    except UnsupportedCaseException as e:
        current_app.logger.exception(msg="Requested Case is not supported.", exc_info=e)
        return "Requested Case is not supported.", 400
    except InputSchemaException as e:
        current_app.logger.exception(msg="Invalid inputs.", exc_info=e)
        return "Invalid inputs.", 400
    except Exception as e:
        current_app.logger.exception(msg="Problem with generating the results.", exc_info=e)
        return "Problem with generating the results.", 400

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
    # logger.info(request.args)
    query = json.loads(request.args["query"])
    jobId = query["jobId"]
    outputs = {}
    try:
        outputs = JOB_INPUTS.pop(jobId)
    except KeyError:
        current_app.logger.error(f"The requested job: {jobId} does not exist.")
        return f"The requested job: {jobId} does not exist.", 400
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

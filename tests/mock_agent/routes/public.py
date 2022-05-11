from flask import Blueprint, request
from flask import current_app
from pprint import pformat
import json
import uuid
from typing import Dict

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
    jobId = str(uuid.uuid4())

    current_app.logger.debug("jsonified query:")
    current_app.logger.debug(pformat(query))

    outputs = {}

    if query['Case'] == 'CarbonBlack_MoMICSolver':
        generate_outputs_func = _generate_momic_outputs
    elif query['Case'] == 'CarbonBlack_StochasticSolver':
        generate_outputs_func = _generate_stoch_outputs
    else:
        raise Exception("Incorrect simulation case")

    current_app.logger.debug(f"Running the {query['Case']}")
    try:
        outputs = generate_outputs_func()
    except Exception as e:
        current_app.logger.exception("Problem with generating outputs.")
    current_app.logger.debug("Generated outputs:")
    current_app.logger.debug(pformat(outputs))

    JOB_INPUTS[jobId] = outputs

    return {"jobId": jobId}, 200


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
        current_app.logger.error("Incorrect simulation inputs.")
        return outputs, 400
    return outputs, 200


def _generate_momic_outputs() -> Dict:
    return json.loads("""{
                "$OUT_MEAN_PART_DIAMETER": {
                    "value": [
                        62.2685
                    ],
                    "unit": "nm"
                },
                "$OUT_PART_NUMBER": {
                    "value": [
                        313308000.0
                    ],
                    "unit": "#"
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


def _generate_stoch_outputs() -> Dict:
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

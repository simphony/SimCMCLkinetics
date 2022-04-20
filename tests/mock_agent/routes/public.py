import logging
from flask import Blueprint, request
import json
import uuid

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Blueprint Configuration
kinetics_agent_bp = Blueprint("kinetics_agent_bp", __name__)

JOB_INPUTS = {}


# Show an instructional message at the app root
@kinetics_agent_bp.route("/request", methods=["GET"])
def runSimulation():
    # logger.info(request.args)
    query = json.loads(request.args["query"])

    outputs = {}

    jobId = str(uuid.uuid4())
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
        outputs = JOB_INPUTS[jobId]
    except LookupError:
        logger.error("Incorrect simulation inputs.")
        return outputs, 400
    return outputs, 200

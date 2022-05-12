import pytest
import json
from typing  import Dict


def test_admin(flask_client) -> None:
    response = flask_client.get(f"/admin/")
    assert response.status_code == 200


@pytest.mark.parametrize(
    "query, out_msg, status_code",
    [
        (
            {},
            "Incorrect inputs query.",
            422
        ),
        (
            {"Case": 'A_Case', "Inputs": {}, "Outputs": []},
            "Requested Case is not supported.",
            422
        ),
        (
            {"Case": 'EAT_TWC', "Inputs": {}, "Outputs": []},
            "Invalid Case Inputs/Ouptuts specification.",
            422
        ),
    ],
)
def test_runSimulation(query: Dict, out_msg: str, status_code: int, flask_client) -> None:
    response = flask_client.get(f"/request?query={json.dumps(query)}")

    assert response.text == out_msg
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "query, out_msg, status_code",
    [
        (
            {},
            "Incorrect get output query.",
            422
        ),
        (
            {"jobId": "testId", "testFiled": "testValue"},
            "Incorrect get output query.",
            422
        ),
        (
            {"jobId": "testId"},
            f"The requested job: testId does not exist.",
            422
        ),
    ],
)
def test_getOutputs(query: Dict, out_msg: str, status_code: int, flask_client) -> None:
    response = flask_client.get(f"/output/request?query={json.dumps(query)}")

    assert response.text == out_msg
    assert response.status_code == status_code
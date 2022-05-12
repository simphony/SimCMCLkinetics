import pytest
import json
import urllib.parse

@pytest.mark.parametrize(
    "inputs_id",
    [
        ("momic_inputs"),
        ("stoch_inputs"),
    ],
)
def test_runSimulation(inputs_id: str, request, flask_client) -> None:
    inputs = request.getfixturevalue(inputs_id)
    case_inputs_parsed = urllib.parse.quote(inputs)
    response = flask_client.get(f"/request?query={case_inputs_parsed}")

    assert response.status_code == 200

    # Parse into JSON
    returnedJSON = json.loads(response.text)
    # Get the generated job ID from the JSON
    jobId_parsed = urllib.parse.quote(json.dumps({"jobId": returnedJSON["jobId"]}))

    # Check if results are successfully generated
    results = flask_client.get(f"/output/request?query={jobId_parsed}")

    assert results.status_code == 200


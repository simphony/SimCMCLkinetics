from osp.wrappers.simcmclkinetics import AgentBridge
import pytest
import json

def _mocked_request_get(url):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.text = json.dumps(json_data)
            self.status_code = status_code

        def json(self):
            return self.json_data

    if 'output' in url:
        return MockResponse({"key1": "value1"}, 200)
    else:
        return MockResponse({"jobId": "testId"}, 200)


def test_encodeURL(agent_bridge: AgentBridge):
    """Tests encoding of simple JSON string
    """
    print("\nRunning test_encodeURL()...")

    sampleJSON = "{ \"name\":\"John\", \"age\":30, \"car\":null }"
    url = agent_bridge.encodeURL(sampleJSON)

    # Check against expected result
    expectedURL = "%7B%20%22name%22%3A%22John%22%2C%20%22age%22%3A30%2C%20%22car%22%3Anull%20%7D"

    print("Result:   " + url)
    print("Expected: " + expectedURL)
    assert url == expectedURL


def test_buildSubmissionURL(agent_bridge: AgentBridge):
    """Tests that a job submission URL can be built
    """
    print("\nRunning test_buildSubmissionURL()...")

    sampleJSON = "{ \"name\":\"John\", \"age\":30, \"car\":null }"
    url = agent_bridge.buildSubmissionURL(sampleJSON)

    # Check against expected result
    expectedURL = agent_bridge.base_url + "request?query=%7B%20%22name%22%3A%22John%22%2C%20%22age%22%3A30%2C%20%22car%22%3Anull%20%7D"

    print("Result:   " + url)
    print("Expected: " + expectedURL)
    assert url == expectedURL


def test_buildOutputURL(agent_bridge: AgentBridge):
    """Tests that an outputs request URL can be built
    """
    print("\nRunning test_buildOutputURL()...")

    agent_bridge.jobID = "login.hpc.co.uk_0123456789"
    url = agent_bridge.buildOutputURL()

    # Check against expected result
    expectedURL = agent_bridge.base_url + "output/request?query=%7B%22jobId%22%3A%22login.hpc.co.uk_0123456789%22%7D"

    print("Result:   " + url)
    print("Expected: " + expectedURL)
    assert url == expectedURL


def test_runJob(agent_bridge: AgentBridge, mocker):
    """Tests if a job can be run via HTTP requests using the runJob() function of the AgentBridge class.
    """
    mocker.patch("osp.wrappers.simcmclkinetics.agent_bridge.requests.get",
        side_effect=_mocked_request_get)

    # Try to run the job
    result = agent_bridge.runJob('{}')

    assert result is not None


@pytest.mark.parametrize(
    "jsonString, result",
    [
        ("", False),
        ('{"key": "value"}', True)
    ]
)
def test_submitJob(jsonString: str, result: bool, agent_bridge: AgentBridge, mocker):
    """Tests if a job can be run via HTTP requests using the runJob() function of the AgentBridge class.
    """
    mocker.patch("osp.wrappers.simcmclkinetics.agent_bridge.requests.get",
        side_effect=_mocked_request_get)

    # Try to run the job
    result = agent_bridge.submitJob(jsonString)

    assert result == result
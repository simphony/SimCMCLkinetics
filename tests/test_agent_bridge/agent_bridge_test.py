from osp.wrappers.simcmclkinetics import AgentBridge

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


def test_runJob(agent_bridge: AgentBridge):
    """Tests if a job can be run via HTTP requests using the runJob() function of the AgentBridge class.
    """
    agent_bridge.jobID = None

    # Try to run the job
    result = agent_bridge.runJob('{}')

    assert result is not None
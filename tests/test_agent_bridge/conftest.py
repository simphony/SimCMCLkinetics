from osp.wrappers.simcmclkinetics import AgentBridge
import pytest

@pytest.fixture()
def agent_bridge() -> AgentBridge:
    agent_bridge = AgentBridge()
    # mock the following functions
    agent_bridge.submitJob = lambda jsonString: True
    agent_bridge.requestOutputs = lambda : {}
    agent_bridge.POLL_INTERVAL = 0 # type: ignore
    return agent_bridge
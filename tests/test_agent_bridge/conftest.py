from osp.wrappers.simcmclkinetics import AgentBridge
import pytest

@pytest.fixture()
def agent_bridge() -> AgentBridge:
    agent_bridge = AgentBridge()
    agent_bridge.POLL_INTERVAL = 0 # type: ignore
    return agent_bridge
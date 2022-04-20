from osp.wrappers.simcmclkinetics import AgentBridge
import time
import subprocess
import signal
import os
import pytest

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
AGENT_TEST_HOST="127.0.0.1"
AGENT_TEST_PORT="5000"
FLASK_APP=os.path.join(THIS_DIR, "mock_agent","app.py")

def pytest_configure(config):
  # this is run before any tests and sets env vars
  # required for the tests
  os.environ['AGENT_TEST_HOST'] = AGENT_TEST_HOST
  os.environ['AGENT_TEST_PORT'] = AGENT_TEST_PORT
  os.environ['KINETICS_AGENT_URL'] = f"http://{AGENT_TEST_HOST}:{AGENT_TEST_PORT}/"
  os.environ['FLASK_APP'] = FLASK_APP
  return config


@pytest.fixture(scope="session", autouse=True)
def kinetics_mock_agent():
    """
        This fixture starts a mock_agent flask server on a
        different process for all the tests. The server must be run
        on a different process as otherwise it would block the tests
        execution. Additionally, a care is taken to start the server
        with the the same python interpreter as the one used to run
        the tests.
        Thanks to the session scope the fixture is run only once
        prior to any tests.
    """
    agent_proc_args = []
    # check if tests are run using python virt env
    virt_env = os.environ.get('VIRTUAL_ENV')
    if virt_env is not None:
        if os.name == 'nt':
            # activate virt env for windows
            agent_proc_args.extend([
                os.path.join(virt_env,"Scripts","activate.bat"), "&&"
            ]
            )
        else:
            # activate virt env for unix
            agent_proc_args.extend([".",os.path.join(virt_env,"bin","activate"), ";"])

    test_host = os.environ['AGENT_TEST_HOST']
    test_port = os.environ['AGENT_TEST_PORT']
    agent_proc_args.extend([
        "python",
        "-m",
        "flask",
        "run",
        "-h",
        test_host,
        "-p",
        test_port])

    agent_proc_args = ' '.join(agent_proc_args)
    agent_proc = subprocess.Popen(
        args = agent_proc_args,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=True,
        start_new_session=True
    )
    # Give the server time to start
    time.sleep(2)
    # Check if started successfully
    yield agent_proc
    # Shut it down at the end of the pytest session
    if os.name == 'nt':
        subprocess.call(['taskkill', '/F', '/T', '/PID', str(agent_proc.pid)])
    else:
        os.killpg(os.getpgid(agent_proc.pid), signal.SIGTERM)

@pytest.fixture(scope="session")
def agent_bridge() -> AgentBridge:
    return AgentBridge()

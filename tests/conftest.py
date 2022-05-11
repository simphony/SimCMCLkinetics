import pytest
import logging
import mock_agent
import json

def pytest_configure(config):
  logger = logging.getLogger('osp.core.ontology')
  logger.setLevel(logging.ERROR)
  return config


@pytest.fixture
def flask_client(scope="session"):
    app = mock_agent.create_app({'TESTING': True})
    with app.test_client() as client:
        yield client
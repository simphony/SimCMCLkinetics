import os
import sys

import pytest
from osp.core.cuds import Cuds

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(THIS_DIR,"..", "..", "examples"))

from examples.use_cases import cb_synthesis, eat_gpf, eat_twc

@pytest.fixture()
def carbon_black_cuds() -> Cuds:
    return cb_synthesis.assemble_cb_synthesis()

@pytest.fixture()
def eat_gpf_cuds() -> Cuds:
    return eat_gpf.assemble_eat_gpf()

@pytest.fixture()
def eat_twc_cuds() -> Cuds:
    return eat_twc.assemble_eat_twc()
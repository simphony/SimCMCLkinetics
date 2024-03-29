from osp.core.cuds import Cuds
from osp.core import CMCL
import osp.core.utils.simple_search as cuds_search
from osp.wrappers.simcmclkinetics.carbon_black_engine import CarbonBlackEngine
from osp.wrappers.simcmclkinetics.eat_engine import EATEngine
from osp.wrappers.simcmclkinetics.kinetics_session import KineticsSession
from osp.wrappers.simcmclkinetics import KineticsEngine
from functools import partial
import urllib.parse

def _case_runner(case_cuds: Cuds, engine: KineticsEngine, model_flag: int, client, mocker) -> Cuds:
    mocker.patch("osp.wrappers.simcmclkinetics.agent_bridge.requests.get",
        side_effect=partial(_flask_app_client, client = client))
    mocker.patch("osp.wrappers.simcmclkinetics.agent_bridge.AgentBridge.POLL_INTERVAL",
        return_value=0)
    with KineticsSession(engine) as session:
        session.setModelFlag(model_flag)
        wrapper = CMCL.wrapper(session=session)
        wrapper.add(case_cuds, rel=CMCL.HAS_PART)
        wrapper.session.run()
    return wrapper

def _flask_app_client(url, client):
    url_split = urllib.parse.urlsplit(url)
    output_chunk = ''
    if 'output' in url_split.path:
        output_chunk = 'output/'
    new_url = f"/{output_chunk}request?{url_split.query}"
    response = client.get(new_url)
    return response

def test_carbon_black_momic(carbon_black_cuds: Cuds, flask_client, mocker) -> None:
    wrapper = _case_runner(
        case_cuds= carbon_black_cuds,
        engine= CarbonBlackEngine(),
        model_flag= KineticsSession.CB_MOMIC,
        client = flask_client,
        mocker = mocker)

    # Find all the output CUDS
    mean_part_size = cuds_search.find_cuds_objects_by_oclass(
        oclass = CMCL.MEAN_PARTICLE_SIZE,
        root = wrapper,
        rel=None
    )
    part_num_dens = cuds_search.find_cuds_objects_by_oclass(
        oclass = CMCL.PARTICLE_NUMBER_DENSITY,
        root = wrapper,
        rel=None
    )
    part_vol_frac = cuds_search.find_cuds_objects_by_oclass(
        oclass = CMCL.PARTICLE_VOLUME_FRACTION,
        root = wrapper,
        rel=None
    )

    # check all the output CUDS
    assert len(mean_part_size) == 1
    assert mean_part_size[0].value != 0.0

    assert len(part_num_dens) == 1
    assert part_num_dens[0].value != 0.0

    assert len(part_vol_frac) == 1
    assert part_vol_frac[0].value != 0.0


def test_carbon_black_stochastoc(carbon_black_cuds: Cuds, flask_client, mocker) -> None:
    wrapper = _case_runner(
        case_cuds= carbon_black_cuds,
        engine= CarbonBlackEngine(),
        model_flag= KineticsSession.CB_STOCHASIC,
        client = flask_client,
        mocker = mocker)

    # Find all the output CUDS
    part_num_dens = cuds_search.find_cuds_objects_by_oclass(
        oclass = CMCL.PARTICLE_NUMBER_DENSITIES,
        root = wrapper,
        rel=None
    )
    part_num_size_classes = cuds_search.find_cuds_objects_by_oclass(
        oclass = CMCL.PARTICLE_SIZE_CLASSES,
        root = wrapper,
        rel=None
    )
    prim_num_dens = cuds_search.find_cuds_objects_by_oclass(
        oclass = CMCL.PRIMARY_PARTICLE_NUMBER_DENSITIES,
        root = wrapper,
        rel=None
    )
    prim_num_size_classes = cuds_search.find_cuds_objects_by_oclass(
        oclass = CMCL.PRIMARY_PARTICLE_SIZE_CLASSES,
        root = wrapper,
        rel=None
    )
    part_fract_dim = cuds_search.find_cuds_objects_by_oclass(
        oclass = CMCL.PARTICLE_MEAN_FRACTAL_DIMENSION,
        root = wrapper,
        rel=None
    )
    # check all the output CUDS
    assert len(part_num_dens) == 1
    assert part_num_dens[0].value_string != ""

    assert len(part_num_size_classes) == 1
    assert part_num_size_classes[0].value_string != ""

    assert len(prim_num_dens) == 1
    assert prim_num_dens[0].value_string != ""

    assert len(prim_num_size_classes) == 1
    assert prim_num_size_classes[0].value_string != ""

    assert len(part_fract_dim) == 1
    assert part_fract_dim[0].value != 0.0


def test_eat_twc(eat_twc_cuds: Cuds, flask_client, mocker) -> None:
    wrapper = _case_runner(
        case_cuds= eat_twc_cuds,
        engine= EATEngine(),
        model_flag= KineticsSession.EAT_TWC,
        client = flask_client,
        mocker = mocker)

    # Find all the output CUDS
    nox_capt_eff = cuds_search.find_cuds_objects_by_oclass(
        oclass = CMCL.NOX_CAPTURE_EFFICIENCY,
        root = wrapper,
        rel=None
    )
    co_capt_eff = cuds_search.find_cuds_objects_by_oclass(
        oclass = CMCL.CO_CAPTURE_EFFICIENCY,
        root = wrapper,
        rel=None
    )
    cxhy_capt_eff = cuds_search.find_cuds_objects_by_oclass(
        oclass = CMCL.CXHY_CAPTURE_EFFICIENCY,
        root = wrapper,
        rel=None
    )

    # check all the output CUDS
    assert len(nox_capt_eff) == 1
    assert nox_capt_eff[0].value != 0.0

    assert len(co_capt_eff) == 1
    assert co_capt_eff[0].value != 0.0

    assert len(cxhy_capt_eff) == 1
    assert cxhy_capt_eff[0].value != 0.0

def test_eat_gpf(eat_gpf_cuds: Cuds, flask_client, mocker) -> None:
    wrapper = _case_runner(
        case_cuds= eat_gpf_cuds,
        engine= EATEngine(),
        model_flag= KineticsSession.EAT_GPF,
        client = flask_client,
        mocker = mocker)


    # Find all the output CUDS
    pm_eff = cuds_search.find_cuds_objects_by_oclass(
        oclass = CMCL.PM_FILTRATION_EFFICIENCY,
        root = wrapper,
        rel=None
    )
    pn_eff = cuds_search.find_cuds_objects_by_oclass(
        oclass = CMCL.PN_FILTRATION_EFFICIENCY,
        root = wrapper,
        rel=None
    )


    # check all the output CUDS
    assert len(pm_eff) == 1
    assert pm_eff[0].value != 0.0

    assert len(pn_eff) == 1
    assert pn_eff[0].value != 0.0
import logging
import sys

from osp.core.namespaces import cuba, CMCL
from osp.core.session import SimWrapperSession
from osp.core.cuds import Cuds

from osp.wrappers.simcmclkinetics.kinetics_session import KineticsSession
from osp.wrappers.simcmclkinetics.carbon_black_engine import CarbonBlackEngine
from osp.wrappers.simcmclkinetics.eat_engine import EATEngine
from use_cases import cb_synthesis, eat_gpf, eat_twc

def run_use_case(case_cuds: Cuds, session: SimWrapperSession) -> None:

    # Construct a wrapper and run a new session
    with session as s:
        wrapper = cuba.wrapper(session=s)

        # Add CB Synthesis process to the wrapper
        wrapper.add(case_cuds, rel=CMCL.HAS_PART)

        # Run the wrapper
        wrapper.session.run()


def run_cb_momic() -> None:
    logger.info('----Running CB MoMIC Use Case----')
    case_cuds = cb_synthesis.assemble_cb_synthesis()
    engine = CarbonBlackEngine()
    session = KineticsSession(engine)
    session.setModelFlag(KineticsSession.CB_MOMIC)

    run_use_case(
        case_cuds= case_cuds,
        session= session)

def run_cb_stochastic() -> None:
    logger.info('----Running CB Stochastic Use Case----')
    case_cuds = cb_synthesis.assemble_cb_synthesis()
    engine = CarbonBlackEngine()
    session = KineticsSession(engine)
    session.setModelFlag(KineticsSession.CB_STOCHASIC)

    run_use_case(
        case_cuds= case_cuds,
        session= session)

def run_eat_gpf() -> None:
    logger.info('----Running EAT GPF Use Case----')
    case_cuds = eat_gpf.assemble_eat_gpf()
    engine = EATEngine()
    session = KineticsSession(engine)
    session.setModelFlag(KineticsSession.EAT_GPF)

    run_use_case(
        case_cuds= case_cuds,
        session= session)

def run_eat_twc() -> None:
    logger.info('----Running EAT TWC Use Case----')
    case_cuds = eat_twc.assemble_eat_twc()
    engine = EATEngine()
    session = KineticsSession(engine)
    session.setModelFlag(KineticsSession.EAT_TWC)

    run_use_case(
        case_cuds= case_cuds,
        session= session)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(message)s',
                        handlers=[logging.StreamHandler()])
    logging.getLogger("osp.core.ontology").setLevel(logging.ERROR)
    logger = logging.getLogger(__name__)

    args = dict(enumerate(sys.argv))

    case_type = args.get(1,None)
    case_sub_type = args.get(2,'')

    momic = case_type is None or \
           (case_type == 'cb' and case_sub_type == '') or \
           (case_type == 'cb' and case_sub_type == 'momic')

    stoch = case_type is None or \
           (case_type == 'cb' and case_sub_type == '') or \
           (case_type == 'cb' and case_sub_type == 'stoch')

    twc = case_type is None or \
           (case_type == 'eat' and case_sub_type == '') or \
           (case_type == 'eat' and case_sub_type == 'twc')

    gpf = case_type is None or \
           (case_type == 'eat' and case_sub_type == '') or \
           (case_type == 'eat' and case_sub_type == 'gpf')

    if not any([momic, stoch, twc, gpf]):
        logger.warning("Warning: Selected use case(s) not supported.")
    else:
        if momic: run_cb_momic()
        if stoch: run_cb_stochastic()
        if twc: run_eat_twc()
        if gpf: run_eat_gpf()
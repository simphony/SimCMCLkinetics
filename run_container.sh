#!/bin/bash
set -o allexport
source .env
set +o allexport

# runs the kinetics osp wrapper
if [ "$1" = "bash" ] ; then
    docker run --rm -it --entrypoint bash cmcl/sim_cmcl_kinetics_osp_wrapper:$SIM_CMCL_KINETICS_OSP_WRAPPER_VERSION
else
    docker run --rm cmcl/sim_cmcl_kinetics_osp_wrapper:$SIM_CMCL_KINETICS_OSP_WRAPPER_VERSION $@
fi
#!/bin/sh

if [ "$1" = "examples" ] ; then
    python examples/examples_runner.py $2 $3
else
    pytest tests
fi
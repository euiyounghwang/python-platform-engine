#!/bin/bash
set -e

SCRIPTDIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
source $SCRIPTDIR/.venv/bin/activate
# --
python $SCRIPTDIR/cluster-consumer.py
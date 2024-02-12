#!/bin/bash
set -e

export PYTHONDONTWRITEBYTECODE=1

SCRIPTDIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

source $SCRIPTDIR/Monitoring/Curator/.venv/bin/activate
python $SCRIPTDIR/Monitoring/Curator/Create-index-data.py
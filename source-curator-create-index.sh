#!/bin/bash
set -e

export PYTHONDONTWRITEBYTECODE=1


SCRIPTDIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

VENV=".venv"
if [ -d $SCRIPTDIR/Search-Engine/Docker/elasticsearch/$VENV ]; then
    echo "VirtualEnv exists."
    # --
    # source ./source-curator-env.sh
    source $SCRIPTDIR/Monitoring/Curator/$VENV/bin/activate
else
    echo "VirtualEnv doesn't exists."
    source $SCRIPTDIR/Monitoring/Curator/create_virtual_env.sh
fi

python $SCRIPTDIR/Monitoring/Curator/Create-index-data.py
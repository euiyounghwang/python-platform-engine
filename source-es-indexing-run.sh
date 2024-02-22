#!/bin/bash
set -e

export PYTHONDONTWRITEBYTECODE=1

SCRIPTDIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

VENV=".venv"

if [ -d $SCRIPTDIR//Search-Engine/Docker/elasticsearch/$VENV ]; then
    echo "VirtualEnv exists."
    # --
    # source ./source-elasticsearch-env.sh
    source $SCRIPTDIR/Search-Engine/Docker/elasticsearch/$VENV/bin/activate
else
    echo "VirtualEnv doesn't exists."
    source $SCRIPTDIR/Search-Engine/Docker/elasticsearch/create_virtual_env.sh
fi


# --
# default script for test indexing
python $SCRIPTDIR/Search-Engine/Docker/elasticsearch/Search-indexing-script.py

# default script for db indexing
# python $SCRIPTDIR//Search-Engine/Docker/elasticsearch/Search-indexing-db-script.py


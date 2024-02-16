#!/bin/bash
set -e

SCRIPTDIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

VENV=".venv"

if [ -d $SCRIPTDIR//Search-Engine/Docker/elasticsearch/$VENV ]; then
    echo "VirtualEnv exists."
    # --
    # source ./source-elasticsearch-env.sh
    source $SCRIPTDIR/Apache-Kafka/$VENV/bin/activate
else
    echo "VirtualEnv doesn't exists."
    source $SCRIPTDIR/Apache-Kafka/create_virtual_env.sh
fi


# --
python $SCRIPTDIR/Apache-Kafka/cluster-producer.py
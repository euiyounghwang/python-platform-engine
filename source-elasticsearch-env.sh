#!/bin/bash
set -e

export PYTHONDONTWRITEBYTECODE=1

SCRIPTDIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

# --
# source ./source-elasticsearch-env.sh
source $SCRIPTDIR/Search-Engine/Docker/elasticsearch/.venv/bin/activate
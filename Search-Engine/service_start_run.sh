#!/bin/bash
set -e

export PYTHONDONTWRITEBYTECODE=1

# cd /Users/euiyoung.hwang/ES/Python_Workspace/python-django
SCRIPTDIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

echo $SCRIPTDIR
# source $SCRIPTDIR/.venv/bin/activate

source $SCRIPTDIR/read_config.sh
# --
# Call this function from './DevOps_Shell/read_config.yaml.sh' to get ES_HOST value in config.yaml file
get_value_from_yaml
# --


# --
# Waitng for ES
$SCRIPTDIR/wait_for_es.sh $ES_HOST

# uvicorn main:app --reload --host=0.0.0.0 --port=5555 --workers 4
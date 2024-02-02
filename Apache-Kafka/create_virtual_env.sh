#!/bin/bash
set -e

export PYTHONDONTWRITEBYTECODE=1

SCRIPTDIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

VENV=".venv"

function activate_virtual_env() {
    # Create virtualenv
    python -m venv $SCRIPTDIR/$VENV
    
    source $SCRIPTDIR/$VENV/bin/activate
    echo "Created virtual enviroment >>" + $SCRIPTDIR/$VENV/bin/activate
    
    echo "Install requirements.txt"
    pip install --upgrade pip
    pip install -r $SCRIPTDIR/requirements.txt
    echo "Install Completely.."
}

if [ -d $SCRIPTDIR/$VENV ]; then
  echo "VirtualEnv exists."
  rm -rf $SCRIPTDIR/$VENV
fi

activate_virtual_env




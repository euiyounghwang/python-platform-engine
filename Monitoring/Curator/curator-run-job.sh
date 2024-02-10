#!/bin/bash
set -e

SCRIPTDIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
# echo $SCRIPTDIR

# cd $SCRIPTDIR
# cd ..
# filepath=`pwd`
# echo $filepath

# source $filepath/.venv/bin/activate
source $SCRIPTDIR/.venv/bin/activate

NOW=$(date +"%y-%m-%d %T")
echo "[$NOW] ***** Start *****" >> $SCRIPTDIR/debug.log

# Test
$SCRIPTDIR/.venv/bin/curator --config $SCRIPTDIR/curator-config.yml --dry-run $SCRIPTDIR/delete-indices.yml | tee -a $SCRIPTDIR/debug.log

# -- snapshot
# curator --config $SCRIPTDIR/curator-config.yml --dry-run $SCRIPTDIR/action_snapshot.yml
# Run
# curator --config $SCRIPTDIR/curator-config.yml $SCRIPTDIR/delete-indices.yml

echo "[$NOW] ***** End *****" >> $SCRIPTDIR/debug.log
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

# $filepath/.venv/bin/curator --config ./Curator/curator-config.yml --dry-run ./Curator/delete-indices.yml
# Test
curator --config $SCRIPTDIR/curator-config.yml --dry-run $SCRIPTDIR/delete-indices.yml | tee -a $SCRIPTDIR/debug.log

# -- snapshot
# curator --config $SCRIPTDIR/curator-config.yml --dry-run $SCRIPTDIR/action_snapshot.yml
# curator --config $SCRIPTDIR/curator-config.yml --dry-run $SCRIPTDIR/restore_snapshot.yml
# Run
# curator --config ./Curator/curator-config.yml ./Curator/delete-indices.yml
# curator --config $SCRIPTDIR/curator-config.yml $SCRIPTDIR/delete-indices.yml

echo "[$NOW] ***** End *****" >> $SCRIPTDIR/debug.log
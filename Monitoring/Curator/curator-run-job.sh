#!/bin/bash
set -e

# https://github.com/elastic/curator/blob/master/examples/actions/snapshot.yml
# https://whatthaburger.tistory.com/113

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
# $SCRIPTDIR/.venv/bin/curator --config $SCRIPTDIR/curator-config.yml --dry-run $SCRIPTDIR/delete-indices.yml | tee -a $SCRIPTDIR/debug.log
# $SCRIPTDIR/.venv/bin/curator --config $SCRIPTDIR/curator-config.yml --dry-run $SCRIPTDIR/create-index.yml | tee -a $SCRIPTDIR/debug.log

# -- snapshot
# $SCRIPTDIR/.venv/bin/curator --config $SCRIPTDIR/curator-config.yml --dry-run $SCRIPTDIR/action_snapshot.yml

# Run
# $SCRIPTDIR/.venv/bin/curator --config $SCRIPTDIR/curator-config.yml $SCRIPTDIR/delete-indices.yml
# $SCRIPTDIR/.venv/bin/curator --config $SCRIPTDIR/curator-config.yml $SCRIPTDIR/create-index.yml | tee -a $SCRIPTDIR/debug.log

# -- snapshot
$SCRIPTDIR/.venv/bin/curator --config $SCRIPTDIR/curator-config.yml $SCRIPTDIR/action_snapshot.yml | tee -a $SCRIPTDIR/debug.log



echo "[$NOW] ***** End *****" >> $SCRIPTDIR/debug.log
#!/bin/bash
set -e

SCRIPTDIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

# echo $SCRIPTDIR
# echo $PWD

export LOGSTASH_INTERNAL_PASSWORD=gsaadmin

$PWD/Kafka/logstash-7.9.0/bin/logstash -f $SCRIPTDIR/logstash_udp.conf
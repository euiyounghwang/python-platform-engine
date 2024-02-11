#!/bin/bash
set -e

SCRIPTDIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

function get_value_from_yaml()
{
    #cat ./config.yaml | jq .app.es.es_host
    ES_HOST=$(cat $SCRIPTDIR/config.yaml | jq .app.es.es_host)
    ES_HOST=$(sed -e 's/^"//' -e 's/"$//' <<< $ES_HOST)
    echo 'get_value_from_yaml -> ' ${ES_HOST}
}
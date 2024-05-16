#!/bin/bash

ELKSERVER=${1:-localhost}
ELKPORT=${2:-9200}
if [ -z "$ELKSERVER" ]; then
  # Usage
  echo 'Usage: check-health.sh <elk-server=localhost> <elk-port=9200>'
  # create-index.sh "logstash-solr-*" 
else
#   curl -s "http://elastic:gsaadmin@$ELKSERVER:$ELKPORT/_cat/health?v"
  curl -s "http://elastic:gsaadmin@$ELKSERVER:$ELKPORT/_cat/health?format=json" | jq
fi
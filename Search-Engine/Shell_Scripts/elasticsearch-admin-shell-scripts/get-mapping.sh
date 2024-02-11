#!/bin/bash
ELKSERVER=${2:-localhost}
ELKPORT=${3:-9200}

if [ -z "$1" ]; then
  # Usage
  echo 'Usage: get-mapping.sh <index-name="logstash-2017.10.23">'
else
  curl -s http://$ELKSERVER:$ELKPORT/$1/_mapping | jq ".\"$1\".mappings.doc.properties"| jshon -k 
fi
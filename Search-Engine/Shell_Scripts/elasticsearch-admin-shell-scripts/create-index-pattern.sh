#!/bin/bash
KIBANASERVER=${2:-localhost}
KIBANAPORT=${3:-5601}
if [ -z "$1" ]; then
  # Usage
  echo 'Usage: create-index-pattern.sh <index-name="logstash-*">'
  # create-index.sh "logstash-solr-*" 
else
  echo "Creating index pattern $1 in Kibana"

  curl -XPOST -D- "http://$KIBANASERVER:$KIBANAPORT/api/saved_objects/index-pattern" \
    -H 'Content-Type: application/json' \
    -H 'kbn-version: 6.1.0' \
    -d "{\"attributes\":{\"title\":\"$1\",\"timeFieldName\":\"@timestamp\"}}"
fi
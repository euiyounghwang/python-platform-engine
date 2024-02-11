#!/bin/bash

ELKMODE=${1:-"-f"}
ELKSERVER=${2:-localhost}
ELKPORT=${3:-9200}
if [ -z "$ELKMODE" ]; then
  # Usage
  echo 'Usage: list-indices.sh <-b|-f> [<elk-server=localhost> <elk-port=9200>]'
  # create-index.sh "logstash-solr-*" 
else
  if [ "$ELKMODE" = "-b" ]; then
    curl -s "http://$ELKSERVER:$ELKPORT/_cat/indices?v" | awk '{print $3}' | grep -v "index" | sort
  else
    curl -s "http://$ELKSERVER:$ELKPORT/_cat/indices?v"
  fi
fi
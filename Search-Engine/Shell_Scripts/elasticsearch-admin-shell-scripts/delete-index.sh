#!/bin/bash
ELKSERVER=${2:-localhost}
ELKPORT=${3:-9200}

if [ -z "$1" ]; then
  # Usage
  echo 'Usage: delete-index.sh <index-name="logstash-2017.10.23">'
else
  echo "Deleting index pattern $1 in Elastic Search"
  curl -s -XDELETE "http://$ELKSERVER:$ELKPORT/$1"
fi
#!/bin/bash
QUERY=${1:-*:*}
ELKINDEX=${2:-_all}
ROWS=${3:-10}
FL=${4:-host,message,@timestamp}
ELKSERVER=${5:-localhost}
ELKPORT=${6:-9200}

if [ -z "$1" ]; then
  # Usage
  echo 'Usage: do-search.sh <q=*:*> <index-name="logstash-2017.10.23"> <rows=10> <fl=host,message,@timestamp>'
else
  COMMAND=`curl -s "http://$ELKSERVER:$ELKPORT/$ELKINDEX/_search?q=$QUERY&size=$ROWS&_source=$FL&pretty=true"`
  echo $COMMAND | jq
  echo "Number of results for search: $QUERY" 
  echo $COMMAND | jq ".hits.total"
fi
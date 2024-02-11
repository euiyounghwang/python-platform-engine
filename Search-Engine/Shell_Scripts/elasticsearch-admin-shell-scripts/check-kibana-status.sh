#!/bin/bash
KIBANAMODE=${1:-"-b"}
KIBANASERVER=${2:-localhost}
KIBANAPORT=${3:-5801}
if [ -z "$KIBANASERVER" ]; then
  # Usage
  echo 'Usage: check-kibana-status.sh <-b|-f> [<kibana-server=localhost> <kibana-port=5601>]'
else
  if [ "$KIBANAMODE" = "-b" ]; then
    curl -s "http://$KIBANASERVER:$KIBANAPORT/api/status" | jq ".status.overall"
  else
    curl -s "http://$KIBANASERVER:$KIBANAPORT/api/status" | jq ".status.statuses"
  fi
fi
#!/bin/bash

SERVER=${1:-localhost}
PORT=${2:-5601}
VAR=${3:-status}
WARNING=${4:-1}
CRITICAL=${5:-2}

if [ "$PORT" = "443" ]; then
   PROTOCOL="https" 
else
   PROTOCOL="http" 
fi

# Endpoint for Kibana API status 
ENDPOINT="$PROTOCOL://${SERVER}:${PORT}/api/status"

if [[ "$1" == "" ]]; then
  echo "USAGE:"
  echo "  check_kibana.sh <SERVER> <PORT> <VAR=status|load|heap> <WARNING> <CRITICAL>"
  exit
fi

CURL=`curl --silent -X GET ${ENDPOINT}`
CHCK=`echo $CURL | grep "$VAR"`

if [[ "$CHCK" == "" ]]; then
   CHECK="Failed"
else
   CHECK="OK"
fi

if [[ "$CHECK" == "OK" ]]; then
   if [[ "$VAR" == "status" ]]; then
      MYDIV=`echo $CURL | jq ".status.overall.state"`
      if [[ "$MYDIV" == "\"green\"" ]]; then
        echo "INFO: Kibana ($VAR) = $MYDIV"
        exit 0
      else
        echo "WARN: Kibana ($VAR) = $MYDIV"
        exit 1
      fi
   fi
   if [[ "$VAR" == "load" ]]; then
      # Kibana 6
      MYDIV=`echo $CURL | jq ".metrics.os.cpu.load_average" | tr '\n' ' ' | sed -e 's/  / /g'`
      # Kibana 5
      #MYDIV=`echo $CURL | jshon -e "metrics" | jshon -e "load" | jshon -e 0 | jshon -e 1 | tr '\n' ' '`
      echo "INFO: Kibana ($VAR) = $MYDIV"
      exit 0
   fi  
   if [[ "$VAR" == "heap" ]]; then
      # Kibana 6
      MYDIV=`echo $CURL | jq ".metrics.process.mem" | tr '\n' ' ' | sed -e 's/  / /g'`
      echo "INFO: Kibana ($VAR) = $MYDIV"
      exit 0
   fi  
   # Kibana 5 
   #MYDIV=`echo $CURL | jshon -e "metrics" | jshon -e "$VAR" | jshon -e 0 | jshon -e 1`
   #echo "INFO: Kibana ($VAR) = $MYDIV"
   #exit 0
elif [[ "$CHECK" == "Failed" ]]; then
   echo "CRITICAL: ${SERVER}"
   exit 2
else
   echo "Check failed."
   exit 3
fi
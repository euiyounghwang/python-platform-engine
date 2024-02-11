#!/bin/bash

# --
# SEARCH-635_Tools_ES_Mapping_Script: [Tools][ES Mappings] Script to apply ES mapping changes to all relevant indexes
# Make environment to local environment (Actually, it can't be access to BEES all instances with ESPERC Prod from local env)
# --

# BEES_DEV to localhost
export BEES_DEV_LOCAL_URL=http://localhost:8881
echo -e "-- BEES_DEV_LOCAL_URL: $BEES_DEV_LOCAL_URL"

# BEES_Staging to localhost
export BEES_STAGING_LOCAL_URL=http://localhost:8882
echo -e "-- BEES_STAGING_LOCAL_URL: $BEES_STAGING_LOCAL_URL"

# BEES_Prod to localhost
export BEES_PROD_LOCAL_URL=http://localhost:8883
echo -e "-- BEES_PROD_LOCAL_URL: $BEES_PROD_LOCAL_URL"

# ESPERC_Prod to localhost
export ESPERC_PROD_LOCAL_URL=http://localhost:9999
echo -e "-- ESPERC_PROD_LOCAL_URL: $ESPERC_PROD_LOCAL_URL"


function ssh_tunnel() {
  echo -e "\n$1"
  if [ $? = 1 ]; then
    echo -e "\nFailed to access"
  else
    status_code=$(curl --head --location --connect-timeout 5 --write-out %{http_code} --silent --output /dev/null "$4")
    if [ "$status_code" == "200" ]; then
      echo -e "Access to $4 with $status_code without retrying"
    else
      ssh -fN -L "$2:$3":9200 euiyoung.hwang@"$3"
      curl "$4"
    fi
  fi
}

# Access to AWS EC2 instances directly from local env. Use ssh tunneling
ssh_tunnel "Access to BEES Dev .." "8881" "172.33.8.244" "$BEES_DEV_LOCAL_URL"
ssh_tunnel "Access to BEES Staging .." "8882" "172.32.23.44" "$BEES_STAGING_LOCAL_URL"
ssh_tunnel "Access to BEES Prod .." "8883" "172.31.8.194" "$BEES_PROD_LOCAL_URL"
ssh_tunnel "Access to ESPERC LB Prod .." "9999" "172.31.40.84" "$ESPERC_PROD_LOCAL_URL"

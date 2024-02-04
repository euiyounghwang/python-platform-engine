#!/bin/bash
set -e

today=$(date '+%Y%m%d')

delete_days=2

result=`expr $today - $delete_days`
# 20240122
# echo $result

# 엘라스틱 쿼리문 
curl -X POST -u elastic:gsaadmin "http://localhost:9209/test_idx/_delete_by_query?conflicts=proceed&pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "match": {
      "ymd": '$result'
    }
  }
}'

curl -X DELETE -u elastic:gsaadmin "http://localhost:9209/curator_manual_create_1-240110" -H 'Content-Type: application/json'
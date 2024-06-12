
#!/bin/sh

sudo /home/devuser/kafka_cluster/kafka-connect-start.sh status
sudo netstat -nlp | grep :8083

curl -XGET  'localhost:8083/connectors/postgres-source/status' | jq
curl -XGET  'localhost:8083/connectors' | jq
curl -XGET  'localhost:8083/connectors/postgres-source"' | jq

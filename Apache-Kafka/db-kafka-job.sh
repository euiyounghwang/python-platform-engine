#!/bin/bash
set -e

#python ./cluster-consumer.py --topic users_tb_topic --brokers localhost:9092
python ./db-kafka-consumer.py --topic ELASTIC_PIPELINE_QUEUE --brokers localhost:9092 --db_run false --url jdbc:oracle:thin:test/test@localhost/test_db --sql "SELECT JSON_OBJECT FROM {} WHERE {}" --master_tb "SELECT JSON_SRC_VW FROM TEST WHERE PROCESS_NAME = '{}'"

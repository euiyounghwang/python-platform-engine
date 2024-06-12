#!/bin/bash
set -e

python ./cluster-producer.py --topic users_tb_topic --brokers localhost:9092

#!/bin/bash
set -e

python ./cluster-consumer.py --topic users_tb_topic --brokers localhost:9092
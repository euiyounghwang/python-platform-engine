
# Kafka Cluster with Elasticsearch
- URl : <i>https://github.com/euiyounghwang/python-search_engine/tree/master/kafka</i>


#### Using Python Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate

Or

➜  Apache-Kafka git:(master) ✗ source ./create_virtual_env.sh 
➜  Apache-Kafka git:(master) ✗ source ./create_virtual_env.sh 
Directory exists.
Created virtual enviroment >> + /Users/euiyoung.hwang/ES/Python_Workspace/python-platform-engine/Apache-Kafka/.venv/bin/activate
Install requirements.txt
Installing dependencies from lock file

Package operations: 1 install, 0 updates, 0 removals

  • Installing kafka-python (2.0.2)
Install Completely..
```

- Docker is one of the most popular container engines used in the software industry to create, package and deploy applications.
- Apache Kafka is an open-source distributed event streaming platform used by thousands of companies for high-performance data pipelines, streaming analytics, data integration, and mission-critical applications.
  1) __ZooKeeper__ is used in distributed systems for service synchronization and as a naming registry.  When working with Apache Kafka, ZooKeeper is primarily used to track the status of nodes in the Kafka cluster and maintain a list of Kafka topics and messages.
  2) __Producer__ : Once a topic has been created with Kafka, the next step is to send data into the topic. This is where Kafka Producers come in. Applications that send data into topics are known as Kafka producers. Applications typically integrate a Kafka client library to write to Apache Kafka
  3) __Consumer__ : Kafka consumers are typically part of a consumer group. When multiple consumers are subscribed to a topic and belong to the same consumer group, each consumer in the group will receive messages from a different subset of the partitions in the topic.


To start an Apache Kafka server, we’d first need to start a Zookeeper server.
We can configure this dependency in a docker-compose.yml file, which will ensure that the Zookeeper server always starts before the Kafka server and stops after it.

Let’s start the Kafka server by spinning up the containers using the docker-compose command:
```bash
$ docker-compose up -d
Creating network "kafka_default" with the default driver
Creating kafka_zookeeper_1 ... done
Creating kafka_kafka_1     ... done
```

- Guide : <i>https://velog.io/@jskim/Muti-Broker-Kafka-Cluster%EC%99%80-%ED%86%B5%EC%8B%A0%ED%95%98%EB%8A%94-%EA%B0%84%EB%8B%A8%ED%95%9C-Producer-Consumer-%EB%A7%8C%EB%93%A4%EA%B8%B0, 
https://www.baeldung.com/ops/kafka-docker-setup</i>


For more stable environments, we’ll need a resilient setup. Let’s extend our docker-compose.yml file to create a multi-node Kafka cluster setup.
A cluster setup for Apache Kafka needs to have redundancy for both Zookeeper servers and the Kafka servers.

So, let’s add configuration for one more node each for Zookeeper and Kafka services into docker-compose.yml


### Kafka Install
```bash
# Monitoring
kafka-monitoring:
    image: obsidiandynamics/kafdrop
    restart: "no"
    ports:
      - "9009:9000"
    environment:
      KAFKA_BROKER_CONNECT: "kafka-1:9092"
    depends_on:
      - kafka-1
      - kafka-2
```
What are the best monitoring tools for Apache Kafka?
- Confluent Control Centre: Confluent(Confluent Control Centre) is the company founded by the original creators of Apache Kafka.
Confluent Control Center delivers understanding and insight about the inner workings of the Apache Kafka clusters and the data that flows through them.
- Lenses
- Datadog Kafka Dashboard
- Cloudera Manager
- Yahoo Kafka Manager
- KafDrop
- LinkedIn Burrow
- Kafka Tool

- URl : http://localhost:9009/

![Alt text](../screenshot/kafka-monitoring.png)


### Create Topic
```bash
➜  ~ docker exec -it kafka-cluster-kafka-1-1 kafka-topics --bootstrap-server=localhost:9092 --create --topic test-topic --partitions 3 --replication-factor 1
Created topic test-topic.
```


### Test Producer/Consumer based on Python Script
- Make a sample json message from producer script.
```bash
(.venv) ➜  python-elasticsearch git:(master) ✗ python ./kafka/cluster-producer.py
```
- Receive message from kafka-broker to fastapi service
```bash
2024-01-23 23:07:45,237] [INFO] [main] [kafka_event] --message -- ConsumerRecord(topic='test1-topic', partition=0, offset=126, timestamp=1706072865230, timestamp_type=0, key=None, value=b'{"author": "choyiny", "content": "Kafka is cool!", "created_at": "2024-01-23T23:07:45.230507"}', checksum=None, serialized_key_size=-1, serialized_value_size=94, headers=()), topic : test1-topic, message : {"author": "choyiny", "content": "Kafka is cool!", "created_at": "2024-01-23T23:07:45.230507"}
[2024-01-23 23:07:45,237] [INFO] [main] [kafka_event] choyiny
[2024-01-23 23:07:45,257] [INFO] [main] [kafka_event] --message -- ConsumerRecord(topic='test-topic', partition=0, offset=83, timestamp=1706072865236, timestamp_type=0, key=None, value=b'{"author": "choyiny", "content": "Kafka is cool!", "created_at": "2024-01-23T23:07:45.236650"}', checksum=None, serialized_key_size=-1, serialized_value_size=94, headers=()), topic : test-topic, message : {"author": "choyiny", "content": "Kafka is cool!", "created_at": "2024-01-23T23:07:45.236650"}
[2024-01-23 23:07:45,257] [INFO] [main] [kafka_event] choyiny
[2024-01-23 23:07:45,258] [INFO] [main] [kafka_event] --message -- ConsumerRecord(topic='test1-topic', partition=0, offset=127, timestamp=1706072865251, timestamp_type=0, key=None, value=b'{"author": "choyiny", "content": "Kafka is cool!", "created_at": "2024-01-23T23:07:45.251348"}', checksum=None, serialized_key_size=-1, serialized_value_size=94, headers=()), topic : test1-topic, message : {"author": "choyiny", "content": "Kafka is cool!", "created_at": "2024-01-23T23:07:45.251348"}
[2024-01-23 23:07:45,258] [INFO] [main] [kafka_event] choyiny
[2024-01-23 23:07:45,260] [INFO] [main] [kafka_event] --message -- ConsumerRecord(topic='test1-topic', partition=0, offset=128, timestamp=1706072865257, timestamp_type=0, key=None, value=b'{"author": "choyiny", "content": "Kafka is cool!", "created_at": "2024-01-23T23:07:45.257780"}', checksum=None, serialized_key_size=-1, serialized_value_size=94, headers=()), topic : test1-topic, message : {"author": "choyiny", "content": "Kafka is cool!", "created_at": "2024-01-23T23:07:45.257780"}
[2024-01-23 23:07:45,260] [INFO] [main] [kafka_event] choyiny
[2024-01-23 23:07:45,261] [INFO] [main] [kafka_event] --message -- ConsumerRecord(topic='test-topic', partition=2, offset=71, timestamp=1706072865255, timestamp_type=0, key=None, value=b'{"author": "choyiny", "content": "Kafka is cool!", "created_at": "2024-01-23T23:07:45.254931"}', checksum=None, serialized_key_size=-1, serialized_value_size=94, headers=()), topic : test-topic, message : {"author": "choyiny", "content": "Kafka is cool!", "created_at": "2024-01-23T23:07:45.254931"}
[2024-01-23 23:07:45,261] [INFO] [main] [kafka_event] choyiny
```

### Test Producer/Consumer using logstash
- Make a sample json message from producer script.
```bash
(.venv) ➜  python-elasticsearch git:(master) ✗ python ./kafka/cluster-producer.py
```

- Receive message from kafka-broker to logstash-kafka input plugin and then indexing into elasticsearch cluster
```bash
...
{
        "author" => "choyiny",
    "created_at" => "2024-01-24T11:48:14.477997",
         "pName" => "topic1",
    "@timestamp" => 2024-01-24T17:48:14.581Z,
      "@version" => "1",
       "message" => "{\"author\": \"choyiny\", \"content\": \"Kafka is cool!\", \"created_at\": \"2024-01-24T11:48:14.477997\"}",
     "TIMESTAMP" => "2024-01-25 02:48:14",
       "content" => "Kafka is cool!"
}
{
        "author" => "choyiny",
    "created_at" => "2024-01-24T11:48:14.454760",
         "pName" => "topic1",
    "@timestamp" => 2024-01-24T17:48:14.579Z,
      "@version" => "1",
       "message" => "{\"author\": \"choyiny\", \"content\": \"Kafka is cool!\", \"created_at\": \"2024-01-24T11:48:14.454760\"}",
     "TIMESTAMP" => "2024-01-25 02:48:14",
       "content" => "Kafka is cool!"
}
...
```
![Alt text](../screenshot/kafka-logstash-elasticsearch.png)


### Kafka Cluster Monitoring using Prometheus/Kafka-Exporter
- Docker-Compose (<i>https://github.com/danielqsj/kafka_exporter?tab=readme-ov-file#download</i>)
```bash
...

kafka-exporter:
  image: danielqsj/kafka-exporter 
  command: ["--kafka.server=kafka-1:9092", "--kafka.server=kafka-2:9092"]
  ports:
    - 9308:9308
  networks:
    - bridge    
    
# http://localhost:9308/metrics (Docker)
2024-01-24 22:53:29 I0125 04:53:29.985948       1 kafka_exporter.go:800] Starting kafka_exporter (version=1.7.0, branch=master, revision=b66d284be28b53fe37ca472029fefa4a521d9f6e)
2024-01-24 22:53:30 I0125 04:53:30.035843       1 kafka_exporter.go:971] Listening on HTTP :9308


# http://localhost:9308/metrics    

# HELP go_gc_duration_seconds A summary of the pause duration of garbage collection cycles.
# TYPE go_gc_duration_seconds summary
go_gc_duration_seconds{quantile="0"} 0.000155583
go_gc_duration_seconds{quantile="0.25"} 0.000219625
go_gc_duration_seconds{quantile="0.5"} 0.000251166
go_gc_duration_seconds{quantile="0.75"} 0.000268
go_gc_duration_seconds{quantile="1"} 0.000268
go_gc_duration_seconds_sum 0.000894374
go_gc_duration_seconds_count 4
# HELP go_goroutines Number of gorout
...
```
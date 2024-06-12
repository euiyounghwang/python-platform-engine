
# Kafka Cluster : Manually Setup
- URl : <i>https://yn971106.tistory.com/85, https://yn971106.tistory.com/81, https://puk0806.tistory.com/44, https://cjw-awdsd.tistory.com/53</i>
<i>

Apache Kafka is an open-source distributed event streaming platform used by thousands of companies for high-performance data pipelines, streaming analytics, data integration, and mission-critical applications. 

A Kafka consumer is any application or process that processes data from Kafka topics (Collection of Messages). Consumers subscribe to topics, and Kafka ensures that each message within a topic is delivered to all subscribed consumers in a scalable and parallel manner. a Kafka consumer can listen to (and subscribe to) more than one topic. This capability is one of Kafka’s strengths.


`Kafka Connect` (https://datacouch.medium.com/getting-started-with-kafka-connect-1b9c54a8b80a) is a framework and toolset for building and running data pipelines between Apache Kafka® and other data systems. It provides a scalable and reliable way to move data in and out of Kafka. It has reusable connector plugins that you can use to stream data between Kafka and various external systems conveniently.

Connectors are the key element in Kafka Connect and there are two types of them: source and sink. 

1)  `A source connector` collects data from a system. Source systems can be entire databases, streams tables, or message brokers. A source connector could also collect metrics from application servers into Kafka topics, making the data available for stream processing with low latency.
    - Source connectors detect the update in the data store and stream the changes to Kafka topics. We can think of it as a producer.

2) `A sink connector` delivers data from Kafka topics into other systems, which might be indexes such as Elasticsearch, batch systems such as Hadoop, or any kind of database.
    - Sink connectors, on the other hand, deliver messages in topics to the data store. We can think of it as a consumer.


Kafka connect does not execute/run anything. Kafka connector is used to establish a connection between Kafka and source DB.

### Kafka Cluster Standalone Setup
```bash
# https://kafka.apache.org/downloads
tar -xzf kafka_2.13-3.1.0.tgz
cd kafka_2.13-3.1.0

#- Set zookeeper.properties


# the directory where the snapshot is stored.
dataDir=/home/devuser/zookeeper/data
# the port at which the clients will connect
clientPort=2181
# disable the per-ip limit on the number of connections since this is a non-production config
maxClientCnxns=0
server.1=localhost:2888:3888
#server.2=localhost:2888:3888
#server.3=localhost:2888:3888
#add here more servers if you want
initLimit=5



#- Set server.properties
..
# The id of the broker. This must be set to a unique integer for each broker.
broker.id=1

# Switch to enable topic deletion or not, default value is false
delete.topic.enable=true

# listeners = PLAINTEXT://your.host.name:9092
listeners=PLAINTEXT://localhost:9092

# Hostname and port the broker will advertise to producers and consumers. If not set,
# it uses the value for "listeners" if configured.  Otherwise, it will use the value
# returned from java.net.InetAddress.getCanonicalHostName().
advertised.listeners=PLAINTEXT://localhost:9092

# Maps listener names to security protocols, the default is for them to be the same. See the config documentation for more details
#listener.security.protocol.map=PLAINTEXT:PLAINTEXT,SSL:SSL,SASL_PLAINTEXT:SASL_PLAINTEXT,SASL_SSL:SASL_SSL

# The number of threads that the server uses for receiving requests from the network and sending responses to the network
num.network.threads=3

# The number of threads that the server uses for processing requests, which may include disk I/O
num.io.threads=8


# The send buffer (SO_SNDBUF) used by the socket server
socket.send.buffer.bytes=102400

# The receive buffer (SO_RCVBUF) used by the socket server
socket.receive.buffer.bytes=102400

# The maximum size of a request that the socket server will accept (protection against OOM)
socket.request.max.bytes=104857600



############################# Log Basics #############################

# A comma seperated list of directories under which to store log files
log.dirs=/apps/kafka-logs

# The default number of log partitions per topic. More partitions allow greater
# parallelism for consumption, but this will also result in more files across
# the brokers.
num.partitions=3

# The number of threads per data directory to be used for log recovery at startup and flushing at shutdown.
# This value is recommended to be increased for installations with data dirs located in RAID array.
num.recovery.threads.per.data.dir=1

############################# Internal Topic Settings  #############################
# The replication factor for the group metadata internal topics "__consumer_offsets" and "__transaction_state"
# For anything other than development testing, a value greater than 1 is recommended for to ensure availability such as 3.
offsets.topic.replication.factor=3
transaction.state.log.replication.factor=3
transaction.state.log.min.isr=3

############################# Log Retention Policy #############################

# The following configurations control the disposal of log segments. The policy can
# be set to delete segments after a period of time, or after a given size has accumulated.
# A segment will be deleted whenever *either* of these criteria are met. Deletion always happens
# from the end of the log.

# The minimum age of a log file to be eligible for deletion due to age
log.retention.hours=4

# A size-based retention policy for logs. Segments are pruned from the log as long as the remaining
# segments don't drop below log.retention.bytes. Functions independently of log.retention.hours.
#log.retention.bytes=1073741824

# The maximum size of a log segment file. When this size is reached a new log segment will be created.
log.segment.bytes=1073741824

# The interval at which log segments are checked to see if they can be deleted according
# to the retention policies
log.retention.check.interval.ms=300000


############################# Zookeeper #############################

# Zookeeper connection string (see zookeeper docs for details).
# This is a comma separated host:port pairs, each corresponding to a zk
# server. e.g. "127.0.0.1:3000,127.0.0.1:3001,127.0.0.1:3002".
# You can also append an optional chroot string to the urls to specify the
# root directory for all kafka znodes.
zookeeper.connect=localhost:2181

# Timeout in ms for connecting to zookeeper
zookeeper.connection.timeout.ms=6000

..


#- set connect-distributed.properties


# This file contains some of the configurations for the Kafka Connect distributed worker. This file is intended
# to be used with the examples, and some settings may differ from those used in a production system, especially
# the `bootstrap.servers` and those specifying replication factors.

# A list of host/port pairs to use for establishing the initial connection to the Kafka cluster.
bootstrap.servers=localhost:9092

# unique name for the cluster, used in forming the Connect cluster group. Note that this must not conflict with consumer group IDs
group.id=test-cluster

# The converters specify the format of data in Kafka and how to translate it into Connect data. Every Connect user will
# need to configure these based on the format they want their data in when loaded from or stored into Kafka
key.converter=org.apache.kafka.connect.json.JsonConverter
value.converter=org.apache.kafka.connect.json.JsonConverter
# Converter-specific settings can be passed in by prefixing the Converter's setting with the converter we want to apply
# it to
key.converter.schemas.enable=false
value.converter.schemas.enable=false

# The internal converter used for offsets, config, and status data is configurable and must be specified, but most users will
# always want to use the built-in default. Offset, config, and status data is never visible outside of Kafka Connect in this format.


# always want to use the built-in default. Offset, config, and status data is never visible outside of Kafka Connect in this format.
internal.key.converter=org.apache.kafka.connect.json.JsonConverter
internal.value.converter=org.apache.kafka.connect.json.JsonConverter
internal.key.converter.schemas.enable=false
internal.value.converter.schemas.enable=false

# Topic to use for storing offsets. This topic should have many partitions and be replicated and compacted.
# Kafka Connect will attempt to create the topic automatically when needed, but you can always manually create
# the topic before starting Kafka Connect if a specific topic configuration is needed.
# Most users will want to use the built-in default replication factor of 3 or in some cases even specify a larger value.
# Since this means there must be at least as many brokers as the maximum replication factor used, we'd like to be able
# to run this example on a single-broker cluster and so here we instead set the replication factor to 1.
offset.storage.topic=connect-offsets
offset.storage.replication.factor=1
#offset.storage.partitions=25

config.storage.topic=connect-configs
config.storage.replication.factor=1

# Topic to use for storing statuses. This topic can have multiple partitions and should be replicated and compacted.
# Kafka Connect will attempt to create the topic automatically when needed, but you can always manually create
# the topic before starting Kafka Connect if a specific topic configuration is needed.
# Most users will want to use the built-in default replication factor of 3 or in some cases even specify a larger value.
# Since this means there must be at least as many brokers as the maximum replication factor used, we'd like to be able
# to run this example on a single-broker cluster and so here we instead set the replication factor to 1.
status.storage.topic=connect-status
status.storage.replication.factor=1
#status.storage.partitions=5

# Flush much faster than normal, whi
..

./bin/zookeeper-server-start.sh config/zookeeper.properties
./bin/kafka-server-start.sh config/server.properties

- Start Kafka Local Cluster : `/home/devuser/kafka_cluster/kafka-start.sh`
- Create topic: /home/devuser/kafka_cluster/kafka_2.13-3.7.0/bin/kafka-topics.sh --create --topic testtopic --bootstrap-server localhost:9092
- Validate topic : /home/devuser/kafka_cluster/kafka_2.13-3.7.0/bin/kafka-topics.sh --list --bootstrap-server localhost:9092
- ISR check
 /kafka_2.11-0.11.0.0/bin/kafka-topics.sh --describe --zookeeper localhost:2181,localhost1:2181,localhost2:2181 --topic test_queue

```

- Producer : ./bin/kafka-console-producer.sh --topic testtopic --bootstrap-server localhost:9092
- Consumer : ./bin/kafka-console-consumer.sh --topic testtopic --from-beginning --bootstrap-server localhost:9092


### Kafka Pruducer/Consumer Test
```bash
[devuser@localhost kafka_2.13-3.7.0]$ /home/devuser/kafka_cluster/kafka_2.13-3.7.0/bin/kafka-console-producer.sh --topic testtopic --bootstrap-server localhost:9092
>test
>

[devuser@localhost kafka_2.13-3.7.0]$ /home/devuser/kafka_cluster/kafka_2.13-3.7.0/bin/kafka-console-consumer.sh --topic testtopic --from-beginning --bootstrap-server localhost:9092
test

#-- Delete Group
[devuser@localhost bin]$ /home/devuser/kafka_cluster/kafka_2.13-3.7.0/bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --delete --group Python_Kafka_Consumer_App_Job
Deletion of requested consumer groups ('Python_Kafka_Consumer_App_Job') was successful.

```

#### Kafka Offset
```bash
KAFKA_OFFSET COMMAND
/home/kafka_2.11-0.11.0.0/bin/kafka-run-class.sh kafka.tools.GetOffsetShell --topic TEST_QUEUE  --broker-list localhost:9092,localhost1:92092,localhost2:9092

When resetting the “kafka_offsets” you must do the following 1st:

Stop spark job
Stop the spark custom app/cluster
Run command to get Kafka offsets from data transfer nodes
Apply values to DB table “kafka_offsets”
Start the spark custom app/cluster
Start spark job 
```


### Kafka Connect : Manually Setup

- Install Kafka Connect JDBC: https://www.confluent.io/hub/confluentinc/kafka-connect-jdbc?_ga=2.107759370.982329993.1715000302-584283732.1711591074&_gac=1.116930932.1715050217.Cj0KCQjw_-GxBhC1ARIsADGgDjvFKyvxCvEapUXlvCeozZcAFKMjFjAfCeeW4oYnt_Pi0xqWNoqVusgaAl4pEALw_wcB&_gl=1*16rk0iu*_ga*NTg0MjgzNzMyLjE3MTE1OTEwNzQ.*_ga_D2D3EGKSGD*MTcxNTA1MDAyNS4xMS4xLjE3MTUwNTA5NTIuNjAuMC4w

- Validate topic after running Kafka-Connect : ./bin/kafka-topics.sh --list --bootstrap-server localhost:9092
- Start Kafka Connect 
```bash
/home/devuser/kafka_cluster/kafka-connect-start.sh 

KAFKA_PATH=/home/devuser/kafka_cluster/kafka_2.13-3.7.0
KAFKA_CONNECT_LIB_PATH=/home/devuser/kafka_cluster/confluent_lib/confluentinc-kafka-connect-jdbc-10.7.6

export CLASSPATH=:$KAFKA_PATH/libs/*:$KAFKA_CONNECT_LIB_PATH/lib/kafka-connect-jdbc-10.7.6.jar:$KAFKA_CONNECT_LIB_PATH/lib/postgresql-42.4.4.jar:$KAFKA_CONNECT_LIB_PATH/lib/kafka-connect-elasticsearch-4.0.0.jar:$CLASSPATH
nohup $KAFKA_PATH/bin/connect-distributed.sh /$KAFKA_PATH/config/connect-distributed.properties &> /dev/null &
```

- Create connectors
```bash
POST http://localhost:8083/connectors
{
    "name": "postgres-source",
    "config": {
        "connector.class": "io.confluent.connect.jdbc.JdbcSourceConnector",
        "connection.url": "jdbc:postgresql://172.25.224.1:5432/postgres",
        "connection.user": "postgres",
        "connection.password": "1234",
        "topic.prefix": "users_tb_topic",
        "poll.interval.ms": "1000",
        "query": "SELECT * FROM postgres.user",
        "transforms":"createKey,ExtractField",
        "transforms.createKey.type":"org.apache.kafka.connect.transforms.ValueToKey",
        "transforms.createKey.fields":"user_id",
        "transforms.ExtractField.type":"org.apache.kafka.connect.transforms.ExtractField$Key",
        "transforms.ExtractField.field":"user_id",
        "mode": "timestamp",
        "timestamp.column.name": "created_at",
        "tasks.max": "1",
        "schema.pattern": "postgres",
        "name": "postgres-source"
    }
}

{
    "name": "postgres-sink",
    "config": {
        "connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
        "connection.url": "jdbc:postgresql://localhost:5432/postgres",
        "connection.user": "postgres",
        "connection.password": "1234",
        "tasks.max": "1",
        "auto.create":"true",
        "auto.evolve":"true",
        "delete.enabled":"false",
        "pk.mode":"none",
        "topics":"users_tb_topic"
    }
}
```

- `status_kafka_connect.sh`
```bash
Connect Running as PID: 17586
tcp6       0      0 :::8083                 :::*                    LISTEN      17586/java
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   169  100   169    0     0   7878      0 --:--:-- --:--:-- --:--:--  8047
{
  "name": "postgres-source",
  "connector": {
    "state": "RUNNING",
    "worker_id": "127.0.0.1:8083"
  },
  "tasks": [
    {
      "id": 0,
      "state": "RUNNING",
      "worker_id": "127.0.0.1:8083"
    }
  ],
  "type": "source"
}
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100    19  100    19    0     0    722      0 --:--:-- --:--:-- --:--:--   730
[
  "postgres-source"
]
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   552  100   552    0     0  25003      0 --:--:-- --:--:-- --:--:-- 26285
{
  "name": "postgres-source",
  "config": {
    "connector.class": "io.confluent.connect.jdbc.JdbcSourceConnector",
    "timestamp.column.name": "created_at",
    "connection.password": "1234",
    "tasks.max": "1",
    "query": "SELECT * FROM postgres.user",
    "transforms.ExtractId.field": "user_id",
    "mode": "timestamp",
    "topic.prefix": "users_tb_topic",
    "connection.user": "postgres",
    "schema.pattern": "postgres",
    "poll.interval.ms": "1000",
    "name": "postgres-source",
    "connection.url": "jdbc:postgresql://localhost:5432/postgres"
  },
  "tasks": [
    {
      "connector": "postgres-source",
      "task": 0
    }
  ],
  "type": "source"
}
(.venv) [devuser@localhost kafka_cluster]$

```

### Kafka Connect RESTAPI
- Reference : https://developer.confluent.io/courses/kafka-connect/rest-api/
- Getting Basic Connect Cluster Information : `http://localhost:8083/`
- Listing Installed Plugins: `http://localhost:8083/connector-plugins`
```bash
[{"class":"io.confluent.connect.elasticsearch.ElasticsearchSinkConnector","type":"sink","version":"4.0.0"},{"class":"io.confluent.connect.jdbc.JdbcSinkConnector","type":"sink","version":"10.7.6"},{"class":"org.apache.kafka.connect.file.FileStreamSinkConnector","type":"sink","version":"3.7.0"},{"class":"io.confluent.connect.jdbc.JdbcSourceConnector","type":"source","version":"10.7.6"},{"class":"org.apache.kafka.connect.file.FileStreamSourceConnector","type":"source","version":"3.7.0"},{"class":"org.apache.kafka.connect.mirror.MirrorCheckpointConnector","type":"source","version":"3.7.0"},{"class":"org.apache.kafka.connect.mirror.MirrorHeartbeatConnector","type":"source","version":"3.7.0"},{"class":"org.apache.kafka.connect.mirror.MirrorSourceConnector","type":"source","version":"3.7.0"}]
```
- Formatting the Result of the Installed Plugin List : `curl -s localhost:8083/connector-plugins | jq '.'`


### Test between Postgres and Kafka Connect
```bash
-- Active: 1715042518972@@localhost@5432@postgres@postgres
SELECT * FROM postgres.user;
SELECT * FROM postgres.users_tb_topic;

-- Generated by the database client.
CREATE TABLE postgres."user"(
    user_id varchar(255) NOT NULL,
    user_name varchar(30) NOT NULL,
    user_age integer NOT NULL,
    created_at timestamp DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE postgres."users_tb_topic"(
    user_id varchar(255) NOT NULL,
    user_name varchar(30) NOT NULL,
    user_age integer NOT NULL,
    created_at timestamp DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO postgres.user (user_id, user_name, user_age) VALUES ('euiyoung', 'ehwang', 11);
INSERT INTO postgres.user (user_id, user_name, user_age) VALUES ('test', 'ehwang', 12);
INSERT INTO postgres.user (user_id, user_name, user_age) VALUES ('test1', '12', 12);
INSERT INTO postgres.user (user_id, user_name, user_age) VALUES ('add', '12', 12);
INSERT INTO postgres.user (user_id, user_name, user_age) VALUES ('addd', '12', 12);
INSERT INTO postgres.user (user_id, user_name, user_age) VALUES ('with-consumer', '12', 12);
INSERT INTO postgres.user (user_id, user_name, user_age) VALUES ('with-consumer1', '12', 12);
INSERT INTO postgres.user (user_id, user_name, user_age) VALUES ('with-consumer2', '12', 12);
INSERT INTO postgres.user (user_id, user_name, user_age) VALUES ('aa', '12', 12);
INSERT INTO postgres.user (user_id, user_name, user_age) VALUES ('cc', '12', 12);
INSERT INTO postgres.user (user_id, user_name, user_age) VALUES ('newrecord', '12', 12);
INSERT INTO postgres.user (user_id, user_name, user_age) VALUES ('today', '12', 12);
INSERT INTO postgres.user (user_id, user_name, user_age) VALUES ('test', '12', 12);
INSERT INTO postgres.user (user_id, user_name, user_age) VALUES ('test-new', '12', 12);
INSERT INTO postgres.user (user_id, user_name, user_age) VALUES ('new3', '11', 12);
UPDATE postgres.user SET user_name='new3_update', created_at = CURRENT_TIMESTAMP WHERE user_id='new3';

#- Running ./cluster-consumer.py for localhost:9092 Kafka Cluster
```


###  Create a message in Topic automatically from Postgres to Kafak Cluster through Kafka connect
```bash
...

2024-05-08 15:36:09,279 : INFO : <BrokerConnection node_id=bootstrap-0 host=localhost:9092 <connected> [IPv6 ('::1', 9092, 0, 0)]>: Closing connection.
2024-05-08 15:36:35,035 : INFO : {"user_id":"new1","user_name":"11","user_age":12,"created_at":1715200595365}
2024-05-08 15:36:35,035 : INFO : -- consumer checking..--

Q receiving -- {"user_id":"new1","user_name":"11","user_age":12,"created_at":1715200595365}
2024-05-08 15:39:30,613 : INFO : {"user_id":"new2","user_name":"11","user_age":12,"created_at":1715200771045}
2024-05-08 15:39:30,613 : INFO : -- consumer checking..--

Q receiving -- {"user_id":"new2","user_name":"11","user_age":12,"created_at":1715200771045}
2024-05-08 15:42:28,171 : INFO : {"user_id":"new3","user_name":"11","user_age":12,"created_at":1715200948545}
2024-05-08 15:42:28,171 : INFO : -- consumer checking..--

Q receiving -- {"user_id":"new3","user_name":"11","user_age":12,"created_at":1715200948545}
2024-05-08 15:45:32,031 : INFO : {"user_id":"new2","user_name":"new2_change","user_age":12,"created_at":1715201132278}
2024-05-08 15:45:32,031 : INFO : -- consumer checking..--
2024-05-08 15:45:32,031 : INFO : {"user_id":"new2","user_name":"new2_change","user_age":12,"created_at":1715201132278}
2024-05-08 15:45:32,031 : INFO : -- consumer checking..--

Q receiving -- {"user_id":"new2","user_name":"new2_change","user_age":12,"created_at":1715201132278}

Q receiving -- {"user_id":"new2","user_name":"new2_change","user_age":12,"created_at":1715201132278}
2024-05-08 15:46:02,370 : INFO : {"user_id":"new3","user_name":"new3_change","user_age":12,"created_at":1715201163040}
2024-05-08 15:46:02,370 : INFO : -- consumer checking..--

Q receiving -- {"user_id":"new3","user_name":"new3_change","user_age":12,"created_at":1715201163040}
2024-05-08 15:57:05,956 : INFO : {"user_id":"new3","user_name":"new3_update","user_age":12,"created_at":1715201826464}
2024-05-08 15:57:05,956 : INFO : -- consumer checking..--

Q receiving -- {"user_id":"new3","user_name":"new3_update","user_age":12,"created_at":1715201826464}
2024-05-08 16:24:14,925 : INFO : {"user_id":"new3","user_name":"new3_update1","user_age":12,"created_at":1715203454699}
2024-05-08 16:24:14,926 : INFO : -- consumer checking..--

Q receiving -- {"user_id":"new3","user_name":"new3_update1","user_age":12,"created_at":1715203454699}
...

```
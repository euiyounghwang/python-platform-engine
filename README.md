# Platform-Repository
Platform-Repository : Build local environment with a Docker and some scripts for testing

- Apache Kafka (`./Apache-Kafka`) : Indexing through Logstash from Kafka Broker : Kafka Producer/Consumer (https://github.com/euiyounghwang/python-search_engine/blob/master/kafka/READMD.md), Kafka-Logstash-Elasticsearch using Python Virtual Enviroment. It can be build & install a enviroment using this script `source ./create_virtual_env.sh`
- Logstash (`./Logstash`): Logstash is part of the Elastic Stack along with Beats, Elasticsearch and Kibana. Logstash is a server-side data processing pipeline that ingests data from a multitude of sources simultaneously. It can be handle with a amount of log messages from Restful API to elasticsearch through this logstash configuration.
- Monitoring `./Monitoring` : `Grafana`(a multi-platform open source analytics and interactive visualization web application. It provides charts, graphs, and alerts for the web when connected to supported data sources), `Prometheus, Cerebro, AlertManager`
 ```bash
   grafana-cli admin reset-admin-password <new password>
 ```
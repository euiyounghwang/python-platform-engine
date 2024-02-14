# Platform-Repository
<i>Platform-Repository : Build local environment with a Docker and some scripts for testing (<i>git remote set-url origin git@github.com:euiyounghwang/python-platform-engine.git</i>)

- Ansible (`./Ansible`) : Open-source automation platform that allows you to define and manage infrastructure as code. It provides modules and playbooks for installing, configuring, and managing Elasticsearch clusters.
- Fabric (`./Fabric`, https://github.com/euiyounghwang/python-DevOps) : a high level Python (2.7, 3.4+) library designed to execute shell commands remotely over SSH, yielding useful Python objects in return. 
- Docker (`./Dockerfile`) : Docker is one of the most popular container engines used in the software industry to create, package and deploy applications. I have added a sample Dockerfile to build an instance of Elasticsearch V.8 with `./Dockerfile/docker-compose.yml`
- Apache Kafka (`./Apache-Kafka`) : Indexing through Logstash from Kafka Broker : Kafka Producer/Consumer (https://github.com/euiyounghwang/python-search_engine/blob/master/kafka/READMD.md), Kafka-Logstash-Elasticsearch using Python Virtual Enviroment. It can be build & install a enviroment using this script `source ./create_virtual_env.sh`
- Logstash (`./Logstash`): Logstash is part of the Elastic Stack along with Beats, Elasticsearch and Kibana. Logstash (`./Logstash/logstash-run.sh`) is a server-side data processing pipeline that ingests data from a multitude of sources simultaneously. It can be handle with a amount of log messages from Restful API to elasticsearch through this logstash configuration.
- Monitoring (`./Monitoring`, https://github.com/euiyounghwang/python-search_engine) : `Grafana`(a multi-platform open source analytics and interactive visualization web application. It provides charts, graphs, and alerts for the web when connected to supported data sources), `Prometheus, Cerebro, AlertManager, Elasticsearch Curator/ILM Policy, Python Export_Script`. Before execute the command as the following, you need to create virtualenv via create_virtual_env.sh like  `source ./Monitoring/Curator/create_virtual_env.sh` (https://github.com/euiyounghwang/python-platform-engine/blob/master/Monitoring/Curator/create_virtual_env.sh) in each tool
    - Elasticsearch Curator : `source ./source-curator-env.sh`, `./source-curator-create-index.sh` for creating sample indexes into ES for executing curator shell script to index, delete or take a snapshot

- Search-Engine `./Search-Engine` : Install the numer of search-engine such as Elasticsearch, Opensearch, Solr based on `./Search-Engine/Docker-compose.yml`. Also you can be create an instance of Elasticsearch node V.8 with `bulid_index_script.py` and `reindex script`.
- RabbitMQ (`./RabbitMQ`) : an open-source message-broker software (sometimes called message-oriented middleware) that originally implemented the Advanced Message Queuing Protocol (AMQP)


#### Example for Crontab
- All Linux distributions are equipped with the cron utility, which allows users to schedule jobs to run at certain fixed times.
- The system-wide root cron jobs are located in the /etc/crontab file. The file contents can be displayed using any text editor, or utilities like cat and more. sudo is not required to display the system cron jobs.
```bash
# Example of job definition:
# .---------------- minute (0 - 59)
# |  .------------- hour (0 - 23)
# |  |  .---------- day of month (1 - 31)
# |  |  |  .------- month (1 - 12) OR jan,feb,mar,apr ...
# |  |  |  |  .---- day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
# |  |  |  |  |
# *  *  *  *  * user-name command to be executed
17 *	* * *	root    cd / && run-parts --report /etc/cron.hourly
25 6	* * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
47 6	* * 7	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
52 6	1 * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )
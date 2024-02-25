# Platform-Repository
<i>Platform-Repository : Build local environment with a Docker and some scripts for testing (<i>git remote set-url origin git@github.com:euiyounghwang/python-platform-engine.git</i>)

- Ansible (`./Ansible`) : Open-source automation platform that allows you to define and manage infrastructure as code. It provides modules and playbooks for installing, configuring, and managing Elasticsearch clusters.
- Fabric (`./Fabric`, https://github.com/euiyounghwang/python-DevOps) : a high level Python (2.7, 3.4+) library designed to execute shell commands remotely over SSH, yielding useful Python objects in return. 
- Docker (`./Dockerfile`) : Docker is one of the most popular container engines used in the software industry to create, package and deploy applications. I have added a sample Dockerfile to build an instance of Elasticsearch V.8 with `./Dockerfile/docker-compose.yml`
- Apache Kafka (`./Apache-Kafka`) : Indexing through Logstash from Kafka Broker : Kafka Producer/Consumer (https://github.com/euiyounghwang/python-search_engine/blob/master/kafka/READMD.md), Kafka-Logstash-Elasticsearch using Python Virtual Enviroment. It can be build & install a enviroment using this script `source ./create_virtual_env.sh`
    - Script for producer/consumers: `./source-kafka-create-run.sh` script to create messages in several topics, `./source-kafka-consumer.sh` script to receive messages from the topics.
    
- Logstash (`./Logstash`): Logstash is part of the Elastic Stack along with Beats, Elasticsearch and Kibana. Logstash (`./Logstash/logstash-run.sh`) is a server-side data processing pipeline that ingests data from a multitude of sources simultaneously. It can be handle with a amount of log messages from Restful API to elasticsearch through this logstash configuration.
- Monitoring (`./Monitoring`, https://github.com/euiyounghwang/python-search_engine) : `Grafana`(a multi-platform open source analytics and interactive visualization web application. It provides charts, graphs, and alerts for the web when connected to supported data sources), `Prometheus, Cerebro, AlertManager, Elasticsearch Curator/ILM Policy, Python Export_Script`. Before execute the command as the following, you need to create virtualenv via create_virtual_env.sh like  `source ./Monitoring/Curator/create_virtual_env.sh` (https://github.com/euiyounghwang/python-platform-engine/blob/master/Monitoring/Curator/create_virtual_env.sh) in each tool
    - Elasticsearch Curator : `source ./source-curator-env.sh`, `./source-curator-create-index.sh` for creating sample indexes into ES for executing curator shell script to index, delete or take a snapshot

- Search-Engine (`./Search-Engine`) : Install the number of search-engines such as Elasticsearch, Opensearch, Solr based on `./Search-Engine/Docker-compose.yml`. 
    - Script with build Docker : You can be create an instance of Elasticsearch node V.8(`./Search-Engine/Docker-compose.yml`) with `bulid_index_script.py` and `reindex script`. Also it can be accesed to the enviroment using `source ./source-es-env.sh` for the scripts.
    - Script for reindexing or others : `./source-es-reindex-run.sh` to run reindexing script, `./source-es-indexing-run.sh`to run test/db script
    ```bash 
    (.venv) ➜  python-platform-engine git:(master) ✗ ./source-es-reindex-run.sh
    VirtualEnv exists.
    ...
    2024-02-15 19:21:51,437 : INFO : ('http://localhost:9209', 'http://localhost:9203', '.monitoring-es-7-2024.02.16', 'cp_recommendation_test')
    2024-02-15 19:21:51,769 : INFO : POST http://localhost:9209/.monitoring-es-7-2024.02.16/_search?scroll=1m&size=1000 [status:200 request:0.330s]
    2024-02-15 19:21:51,816 : INFO : Ingest data .. : 1000
    <Elasticsearch([{'host': 'localhost', 'port': 9203}])>
    2024-02-15 19:21:51,833 : INFO : HEAD http://localhost:9203/cp_recommendation_test [status:200 request:0.017s]
    Successfully deleted: cp_recommendation_test
    2024-02-15 19:21:52,018 : INFO : DELETE http://localhost:9203/cp_recommendation_test [status:200 request:0.183s]
    2024-02-15 19:21:52,192 : INFO : PUT http://localhost:9203/cp_recommendation_test [status:200 request:0.174s]
    2024-02-15 19:21:52,204 : INFO : POST http://localhost:9203/cp_recommendation_test/_refresh [status:200 request:0.011s]
    Successfully created: cp_recommendation_test
    2024-02-15 19:21:52,204 : INFO : buffered_json_to_es Loading..
    2024-02-15 19:21:53,967 : INFO : POST http://localhost:9203/_bulk [status:200 request:0.372s]
    2024-02-15 19:21:53,968 : INFO : ** indexing ** : 269
    ...
    ```
    
- RabbitMQ (`./RabbitMQ`) : an open-source message-broker software (sometimes called message-oriented middleware) that originally implemented the Advanced Message Queuing Protocol (AMQP)

- Apache Hadoop (`./Apache-Hadoop`) : The Apache Hadoop software library is a framework that allows for the distributed processing of large data sets across clusters of computers using simple programming models. 
    - Build docker in local environment : `./Apache-Hadoop/docker-compose.yml` to run resource manager, nodemanager, namenode, and datanode


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
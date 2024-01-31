
# Python-Search-Engine
- URl : <i>https://github.com/euiyounghwang/python-search_engine/tree/master</i>

<img src="https://img.shields.io/badge/fastapi-109989?style=for-the-badge&logo=FASTAPI&logoColor=white"/> <img src="https://img.shields.io/badge/Elastic_Search-005571?style=for-the-badge&logo=elasticsearch&logoColor=white" /> <img src="https://img.shields.io/badge/Apache_Kafka-231F20?style=for-the-badge&logo=apache-kafka&logoColor=white" /> <img src="https://img.shields.io/badge/Prometheus-000000?style=for-the-badge&logo=prometheus&labelColor=000000" /> <img src="	https://img.shields.io/badge/Grafana-F2F4F9?style=for-the-badge&logo=grafana&logoColor=orange&labelColor=F2F4F9" /> <img src="https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white" /> <img src="https://img.shields.io/badge/Shell_Script-121011?style=for-the-badge&logo=gnu-bash&logoColor=white" /> <img src="https://img.shields.io/badge/Ansible-000000?style=for-the-badge&logo=ansible&logoColor=white" /> <img src="https://img.shields.io/badge/Grafana-F2F4F9?style=for-the-badge&logo=grafana&logoColor=orange&labelColor=F2F4F9" /> <img src="https://img.shields.io/badge/Swagger-85EA2D?style=for-the-badge&logo=Swagger&logoColor=white" />
	

I will use this project as a basic api for building and searching with Elasticsearch(`In 7.10, Elasticsearch released the point-in-time API`. As of 2021, starting with the version 7.11 release, it’s free under the Server Side Public License (SSPL) or Elastic License)
- Build docker service and pytest instance with a Dockerfile for creating an index with sample datasets and searching with Elasticsearch
- Also run local environment with this project using `./service_start.sh` script
- Build Docker Instance for testing with pytest using using `./docker-compose.yml` or different ways the following method like the step `Install Service and Test with Elasicsearch Cluster based on Docker`
- __<i>[Resharding Stratege]<i>__ : To optimize for better performance of elasticsearch clusters, we have to think of a few questions like how to organize the index? Shard number? Replica Number?  Mapping? Any other settings?  (Optmize index, Index/Search Peformance with the number of shards)
- Estimate the number of primary/replica(replica should be one by default) shards with resharding stratege by using `'/cluster/sharding_predict'` with POST method against data size 
- Also we can test Opensearch & Dashboard with Cerebro tool for implementing & monitoring after building the docker instance using single node or multiple nodes with `./docker-compose.yml`
- Implement script file(`https://github.com/euiyounghwang/python-search_engine/tree/master/tools`) for indexing with Elasticsearch and Opensearch
- Elasticsearch Curator : Curator(`./Curator/curator-run-job.sh`) is breaking into version dependent releases. Curator 6.x will work with Elasticsearch 6.x, Curator 7.x will work with Elasticsearch 7.x, and when it is released, Curator 8.x will work with Elasticsearch 8.x. (<i>https://github.com/euiyounghwang/python-search_engine/blob/master/Curator/README.md</i>)
- Indexing through Logstash from Kafka Broker : Kafka Producer/Consumer (https://github.com/euiyounghwang/python-search_engine/blob/master/kafka/READMD.md), Kafka-Logstash-Elasticsearch, Kafka Consumer with Fastapi Framework, Kafka-Prometheus-Exporter for monitoring


#### Install Poerty
```bash
https://python-poetry.org/docs/?ref=dylancastillo.co#installing-with-the-official-installer
```

#### Using Python Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate
```

#### Using Poetry: Create the virtual environment in the same directory as the project and install the dependencies with basic library:
```bash
poetry config virtualenvs.in-project true
poetry init
poetry add fastapi
poetry add uvicorn
poetry add pytz
poetry add elasticsearch==7.10
poetry add numpy
poetry add pytest
poetry add python-dotenv
poetry add opensearch-py
```

#### Install this project to make an environment using Poetry Dependency
```bash
source .venv/bin/activate
poetry install (using --no-root option when building the docker on CircleCI or Docker env)
```

#### Install Service and Test with Elasicsearch Cluster based on Docker
- Build Single Node ES with Kibana based on 7.10.0 version (You have to choose to build & create REST-API Service (`fn-elasticsearch-api`) and Pytest(`fn-elasticsearch-api-test`) instances using `./docker-compose.yml` for interacting with single ES cluster)
```bash
docker run --name kibaba-run --network bridge -e "ELASTICSEARCH_URL=http://host.docker.internal:9209" -e "ES_JAVA_OPTS=-Xms1g -Xmx1g" -e "ELASTICSEARCH_HOSTS=http://host.docker.internal:9209" -p 5801:5601 docker.elastic.co/kibana/kibana:7.10.0
docker run --name es8-run --network bridge -p 9209:9200 -p 9114:9114 -p 9309:9300 -e "http.cors.enabled=true" -e "http.cors.allow-origin=\"*\"" -e "http.cors.allow-headers=X-Requested-With,X-Auth-Token,Content-Type,Content-Length,Authorization" -e "http.cors.allow-credentials=true" -e "xpack.security.enabled=false" -e "discovery.type=single-node" -e "ES_JAVA_OPTS=-Xms2g -Xmx2g" docker.elastic.co/elasticsearch/elasticsearch:7.10.0
```
- Build Multiple Nodes ES  based on 7.10.0 version with Kibana, REST-API Service & Pytest instances : Build & create instances using `./docker-compose.yml` or `./docker-build.sh` for building the docker image, `./docker-run.sh` for running the service and `./docker-tests.sh` for testing using pytest (Also you can build single cluster(`single_node`, `single_node_kibana`) without xpack option or multiple cluster with xpack : `docker-compose -f ./create-certs.yml run --rm create_certs` to create certs)


#### Elasticsearh Cluster Diagnostics (Support by Elasticsearch)
- The support diagnostic utility is a Java application that can interrogate a running Elasticsearch cluster or Logstash process to obtain data about the state of the cluster at that point in time. It is compatible with all versions of Elasticsearch (including alpha, beta and release candidates), and for Logstash versions greater than 5.0, and for Kibana v6.5+. The release version of the diagnostic is independent of the Elasticsearch, Kibana or Logstash version it is being run against.
- `Diagnostics Guide` <i>(https://olamideolajide.medium.com/how-to-collect-diagnostics-for-a-cloud-elasticsearch-cluster-4a20841a815a, https://github.com/elastic/support-diagnostics/releases/tag/8.0.3)</i>
```bash
python-elasticsearch git:(master) ✗ ./support-diagnostics-8.0.3/diagnostics.sh --host localhost --port 9209
Using /usr/bin/java as Java Runtime
Using -Xms256m -Xmx2000m  for options.
Processing diagnosticInputs...

Creating temp directory: /Users/euiyoung.hwang/ES/Python_Workspace/python-elasticsearch/local-diagnostics
Configuring log file.
Checking for diagnostic version updates.
Issue encountered while checking diagnostic version for updates.
Failed to get current diagnostic version from Github.
If Github is not accessible from this environemnt current supported version cannot be confirmed.
Getting Elasticsearch Version.
Checking the supplied hostname against the node information retrieved to verify location. This may take some time.
...
Results written to: /Users/euiyoung.hwang/ES/Python_Workspace/python-elasticsearch/local-diagnostics/commercial/watcher_stack.json
Results written to: /Users/euiyoung.hwang/ES/Python_Workspace/python-elasticsearch/local-diagnostics/commercial/xpack.json
Writing diagnostic manifest.
Closing logger.
Archiving diagnostic results.
Archive: /Users/euiyoung.hwang/ES/Python_Workspace/python-elasticsearch/local-diagnostics-20231215-160457.tar.gz was created
Deleted directory: /Users/euiyoung.hwang/ES/Python_Workspace/python-elasticsearch/local-diagnostics.
```
- Extract diagnotics files like `local-diagnostics-20231215-160457.tar` with folder

#### Install OpenSearch based on Docker for testing
- OpenSearch(<i>https://opensearch.org/docs/latest/install-and-configure/install-opensearch/docker</i>) is a scalable, flexible, and extensible open-source software suite for search, analytics, and observability applications licensed under Apache 2.0.
- Build Single Node OpenSearch with Dashboard(`http://localhost:5901`) based on the recent version (You can test using `https://localhost:9250` or `curl https://localhost:9250 -ku 'admin:admin'`)
```bash
docker run --name opensearch-es01 --network bridge -p 9250:9200 -e "node.name=opensearch-es01" -e "discovery.type=single-node" opensearchproject/opensearch
docker exec -it  opensearch-es01 /bin/bash -c /usr/share/opensearch/plugins/opensearch-security/tools/hash.sh
# docker run --name opensearch-dashboard --network bridge -p 5901:5601 -e "opensearch_hosts='[\"https://host.docker.internal:9250\"]'" opensearchproject/opensearch-dashboards
docker run --name opensearch-dashboard --network bridge -p 5901:5601 -v /Users/euiyoung.hwang/ES/Python_Workspace/python-elasticsearch/custom-opensearch-dashboards.yml:/usr/share/opensearch-dashboards/config/opensearch_dashboards.yml opensearchproject/opensearch-dashboards
```
- Send requests to the server to verify that OpenSearch is up and running:
```bash
curl -XGET https://localhost:9250 -u 'admin:admin' --insecure
curl -XGET https://localhost:9250/_cat/nodes?v -u 'admin:admin' --insecure
curl -XGET https://localhost:9250/_cat/plugins?v -u 'admin:admin' --insecure
```

#### Run Local Environment
- It will be validate the status of elasticsearch cluster using `./wait_for_es.sh` and `./DevOps_Shell/read_config.sh` for reading es host value in `./config.yaml` automatically when running `./service_start.sh` script.
```bash
source .venv/bin/activate
(.venv) ➜  python-elasticsearch git:(master) ✗ ./service_start.sh
get_value_from_yaml ->  http://localhost:9209
ElasticSearch is up
INFO:     Will watch for changes in these directories: ['/Users/euiyoung.hwang/ES/Python_Workspace/python-elasticsearch']
WARNING:  "workers" flag is ignored when reloading is enabled.
INFO:     Uvicorn running on http://0.0.0.0:8888 (Press CTRL+C to quit)
INFO:     Started reloader process [17469] using StatReload
[2023-12-09 20:36:18,420] [INFO] [injector] [read_config_yaml] {
  "app": {
    "es": {
      "es_host": "http://localhost:9209",
      "index": {
        "alias": "metrics_search"
      }
    }
  }
}
[2023-12-09 20:36:18,421] [INFO] [config] [__init__] @@self.hosts - http://localhost:9209
INFO:     Started server process [17471]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```


#### Swagger for REST-API
![Alt text](./screenshot/Swagger_API.png)


### Pytest
- Go to virtual enviroment using `source .venv/bin/activate`
- Run this command manually: `poetry run py.test -v --junitxml=test-reports/junit/pytest.xml --cov-report html --cov tests/` or `./pytest.sh`
```bash
(.venv) ➜  python-elasticsearch git:(master) ./pytest.sh 
============================================= test session starts ==============================================
platform darwin -- Python 3.9.7, pytest-7.4.3, pluggy-1.3.0 -- /Users/euiyoung.hwang/ES/Python_Workspace/python-elasticsearch/.venv/bin/python
cachedir: .pytest_cache
rootdir: /Users/euiyoung.hwang/ES/Python_Workspace/python-elasticsearch/tests
configfile: pytest.ini
plugins: cov-4.1.0, anyio-3.7.1
collected 7 items                                                                                              

tests/test_api.py::test_skip SKIPPED (no way of currently testing this)                                  [ 14%]
tests/test_api.py::test_api PASSED                                                                       [ 28%]
tests/test_api.py::test_rest_api PASSED                                                                  [ 42%]
tests/test_elasticsearch.py::test_elasticsearch PASSED                                                   [ 57%]
tests/test_elasticsearch.py::test_indics_analyzer_elasticsearch PASSED                                   [ 71%]
tests/test_elasticsearch.py::test_search_elasticsearch PASSED                                            [ 85%]
tests/test_elasticsearch.py::test_api_es_search PASSED                                                   [100%]
```

- Badge : https://github.com/alexandresanlim/Badges4-README.md-Profile
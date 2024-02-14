### Prometheus

__Prometheus__ (<i>https://prometheus.io/download/, https://yoo11052.tistory.com/201</i>) is an open-source monitoring system that collects metrics from your application and stores them in a time series database. It can be used to monitor the performance of your application and alert you when something goes wrong

- __Elasticserach Exporter__ : This is a builtin exporter from Elasticsearch to Prometheus. It collects all relevant metrics and makes them available to Prometheus via the Elasticsearch REST API. (https://github.com/vvanholl/elasticsearch-prometheus-exporter/, https://blog.naver.com/PostView.naver?blogId=whddbsml&logNo=222405287424)
- __Python Exporter__ (https://pypi.org/project/prometheus-flask-exporter/)
- __Node Exporter__ : The node_exporter is designed to monitor the host system. It's not recommended to deploy it as a Docker container because it requires access to the host system (https://github.com/prometheus/node_exporter/, https://github.com/prometheus/node_exporter/releases/download/v1.6.1/node_exporter-1.6.1.darwin-amd64.tar.gz)

```bash
  # My local environment to install node-exporter Docker instance
  # docker run --rm -p 9100:9100 prom/node-exporter 
  # docker compose up -d node-exporter
  node_exporter:
    # http://localhost:9100/metrics
    image: prom/node-exporter
    container_name: node_exporter
    depends_on:
      - prometheus
    restart: always
    ports:
    - 9100:9100
```

- __RabbitMQ Exporter__ : Prometheus exporter for RabbitMQ metrics. Data is scraped by prometheus. You can install plugin promethus from RabbitMQ Plugin 
```bash
# Install Plugin
/opt/homebrew/opt/rabbitmq/sbin/rabbitmq-plugins enable rabbitmq_prometheus
brew services restart rabbitmq
```

- The Alertmanager(<i>http://localhost:9091/alerts?search, http://localhost:9093/#/alerts, http://localhost:9093/api/v2/alerts</i>) handles alerts sent by client applications such as the Prometheus server. Alerting with Prometheus is separated into two parts. Alerting rules in Prometheus servers send alerts to an Alertmanager. 
```
# Alertmanager Configuration
alerting:
  alertmanagers:
    - static_configs:
      - targets: ['host.docker.internal:9093']

# loading at once and evaluate the rule periodically based on 'evaluation_interval'
rule_files:
  - "/Alertmanager/alert.rules"
```

![Alt text](/screenshot/AlertManager-Installation.png)

- Prometheus.yml
```bash
- job_name: rabbitmq-exporter
  scrape_interval: 10s
  metrics_path: "/metrics"
  static_configs:
  - targets: ['host.docker.internal:15692']
```

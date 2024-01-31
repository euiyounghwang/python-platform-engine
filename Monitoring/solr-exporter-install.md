### Guide
```
https://medium.com/yapsody-engineering/how-to-run-apache-solr-with-docker-dfb0d7660a89
https://stackoverflow.com/questions/58169520/execute-command-into-docker-image-to-launch-solr-exporter

/opt/solr-9.3.0/contrib/prometheus-exporter/bin/solr-exporter -p 9854 -b http://host.docker.internal:8983/solr -f /opt/solr-9.3.0/contrib/prometheus-exporter/conf/solr-exporter-config.xml
  
```

### Docker Version
```
# http://localhost:8983/solr
  solr-exporter:
    image: solr:9.3.0
    ports:
     - "9854:9854"
    entrypoint:
      - "/opt/solr-9.3.0/contrib/prometheus-exporter/bin/solr-exporter"
      - "-p"
      - "9854"
      - "-b"
      - "http://host.docker.internal:8983/solr"
      - "-f"
      - "/opt/solr-9.3.0/contrib/prometheus-exporter/conf/solr-exporter-config.xml"
      - "-n"
      - "8"
```

 
### Test configuration file
```
/opt/solr-9.3.0/contrib/prometheus-exporter/bin/solr-exporter -p 9854 -b http://host.docker.internal:8983/solr -f /opt/solr-9.3.0/contrib/prometheus-exporter/conf/solr-exporter-config.xml
```

 ### Run
```
https://grafana.com/grafana/dashboards/12456-solr-dashboard/

# Run thius command inside Docker
docker run -d -v "$PWD/solrdata:/var/solr" -p 8983:8983 -p 9854:9854 --name solr-engine solr solr-precreate gettingstarted -e "/opt/solr-9.3.0/contrib/prometheus-exporter/bin/solr-exporter -p 9854 -b http://host.docker.internal:8983/solr -f /opt/solr-9.3.0/contrib/prometheus-exporter/conf/solr-exporter-config.xml"
solr@31172ca1ef75:/opt/solr-9.3.0$ /opt/solr-9.3.0/contrib/prometheus-exporter/bin/solr-exporter -p 9854 -b http://host.docker.internal:8983/solr -f /opt/solr-9.3.0/contrib/prometheus-exporter/conf/solr-exporter-config.xml &
# or
# Run other solr-exporter docker env
http://localhost:9854/metrics
```
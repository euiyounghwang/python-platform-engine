### Guide
```
https://velog.io/@sosimina/Prometheus-%EB%AA%A8%EB%8B%88%ED%84%B0%EB%A7%81-%EC%84%A4%EC%B9%98-%EB%B0%8F-Node-exporter-%EC%A1%B0%EC%9D%B8
https://github.com/prometheus/node_exporter/
```

### Docker Version
```
  # docker run --rm -p 9100:9100 prom/node-exporter 
  # docker compose up -d node-exporter
  # https://github.com/prometheus/node_exporter/
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


### Download and unpack
```
wget https://github.com/prometheus/node_exporter/releases/download/v1.6.1/node_exporter-1.6.1.linux-amd64.tar.gz
tar -zxvf node_exporter-1.6.1.linux-amd64.tar.gz
node_exporter-1.6.1.linux-amd64/
node_exporter-1.6.1.linux-amd64/NOTICE
node_exporter-1.6.1.linux-amd64/node_exporter
node_exporter-1.6.1.linux-amd64/LICENSE

cd node_exporter-1.6.1.linux-amd64/

/home/devuser/ES/node_exporter-1.6.1.linux-amd64/node_exporter

sudo cp /home/devuser/ES/node_exporter-1.6.1.linux-amd64/node_exporter /usr/local/bin/node_exporter
sudo chown devuser /usr/local/bin/node_exporter
 ```
 
 
### Test configuration file
```
/usr/local/bin/node_exporter
```

### Register the service for node_exporter systemd 
```
sudo vi /etc/systemd/system/node_exporter.service

[Unit]
Description=node_exporter
Wants=network-online.target
After=network-online.target

[Service]
User=devuser
Group=devuser
Type=simple
WorkingDirectory=/home/devuser/ES/node_exporter-1.6.1.linux-amd64
ExecStart=/usr/local/bin/node_exporter
[Install]
WantedBy=multi-user.target

# Run service
systemctl daemon-reload
# Autostart when rebooting
sudo systemctl enable node_exporter.service
systemctl start node_exporter
```
 
### Prometheus.yml
```
- job_name: node-exporter
    #scrape_interval: 10s
    metrics_path: "/metrics"
    static_configs:
    - targets: ['localhost:9100'] 
```
 
 
### Prometheus Log
```
devuser@ubuntu-master-1:~/ES/prometheus-2.37.0.linux-amd64$ systemctl status node_exporter.service
● node_exporter.service - node_exporter
     Loaded: loaded (/etc/systemd/system/node_exporter.service; enabled; vendor preset: enabled)
     Active: active (running) since Thu 2023-10-05 22:32:55 CDT; 2min 12s ago
   Main PID: 3590 (node_exporter)
      Tasks: 6 (limit: 976)
     Memory: 19.6M
        CPU: 216ms
     CGroup: /system.slice/node_exporter.service
             └─3590 /usr/libexec/qemu-binfmt/x86_64-binfmt-P /usr/local/bin/node_exporter /usr/local/bin/node_exporter

Oct 05 22:32:55 ubuntu-master-1 node_exporter[3590]: ts=2023-10-06T03:32:55.335Z caller=node_exporter.go:117 level=info collector=thermal_zone
Oct 05 22:32:55 ubuntu-master-1 node_exporter[3590]: ts=2023-10-06T03:32:55.335Z caller=node_exporter.go:117 level=info collector=time
Oct 05 22:32:55 ubuntu-master-1 node_exporter[3590]: ts=2023-10-06T03:32:55.335Z caller=node_exporter.go:117 level=info collector=timex
Oct 05 22:32:55 ubuntu-master-1 node_exporter[3590]: ts=2023-10-06T03:32:55.335Z caller=node_exporter.go:117 level=info collector=udp_queues
Oct 05 22:32:55 ubuntu-master-1 node_exporter[3590]: ts=2023-10-06T03:32:55.335Z caller=node_exporter.go:117 level=info collector=uname
Oct 05 22:32:55 ubuntu-master-1 node_exporter[3590]: ts=2023-10-06T03:32:55.335Z caller=node_exporter.go:117 level=info collector=vmstat
Oct 05 22:32:55 ubuntu-master-1 node_exporter[3590]: ts=2023-10-06T03:32:55.335Z caller=node_exporter.go:117 level=info collector=xfs
Oct 05 22:32:55 ubuntu-master-1 node_exporter[3590]: ts=2023-10-06T03:32:55.335Z caller=node_exporter.go:117 level=info collector=zfs
Oct 05 22:32:55 ubuntu-master-1 node_exporter[3590]: ts=2023-10-06T03:32:55.349Z caller=tls_config.go:274 level=info msg="Listening on" address=[::]:9100
Oct 05 22:32:55 ubuntu-master-1 node_exporter[3590]: ts=2023-10-06T03:32:55.350Z caller=tls_config.go:277 level=info msg="TLS is disabled." http2=false address=[::]:9100
```
 
 ### Run
```
http://localhost:9100/metrics
https://grafana.com/grafana/dashboards/1860
```
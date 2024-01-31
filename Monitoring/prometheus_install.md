### Guide
```
https://prometheus.io/download/, 
https://yoo11052.tistory.com/201
https://yoo11052.tistory.com/201
```

### Docker Version
```
 prometheus:
    image: prom/prometheus
    container_name: prometheus
    restart: unless-stopped
    ports:
      - 9091:9090
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - ./prometheus:/prometheus
      # - ./alertmanager/alert.rules:/alertmanager/alert.rules
      - ./alertmanager/alert_rules.yml:/alertmanager/alert_rules.yml
    command:
      - --config.file=/etc/prometheus/prometheus.yml
      - --storage.tsdb.path=/prometheus
      - --storage.tsdb.retention.time=2d # 90일보다 오래된 metrics는 삭제
      - --storage.tsdb.retention.size=1GB # 10GB를 넘을 시 오래된 metrics 삭제
      - --web.console.libraries=/usr/share/prometheus/console_libraries
      - --web.console.templates=/usr/share/proemtheus/consoles
      - --web.enable-admin-api
    networks:
      - bridge
```


### Download and unpack
```
wget https://github.com/prometheus/prometheus/releases/download/v2.37.0/prometheus-2.37.0.linux-amd64.tar.gz
tar -zxvf prometheus-2.37.0.linux-amd64.tar.gz
prometheus-2.37.0.linux-amd64/
prometheus-2.37.0.linux-amd64/consoles/
prometheus-2.37.0.linux-amd64/consoles/index.html.example
prometheus-2.37.0.linux-amd64/consoles/node-cpu.html
prometheus-2.37.0.linux-amd64/consoles/node-disk.html
prometheus-2.37.0.linux-amd64/consoles/node-overview.html
prometheus-2.37.0.linux-amd64/consoles/node.html
prometheus-2.37.0.linux-amd64/consoles/prometheus-overview.html
prometheus-2.37.0.linux-amd64/consoles/prometheus.html
prometheus-2.37.0.linux-amd64/console_libraries/
prometheus-2.37.0.linux-amd64/console_libraries/menu.lib
prometheus-2.37.0.linux-amd64/console_libraries/prom.lib
prometheus-2.37.0.linux-amd64/prometheus.yml
prometheus-2.37.0.linux-amd64/LICENSE
prometheus-2.37.0.linux-amd64/NOTICE
prometheus-2.37.0.linux-amd64/prometheus
prometheus-2.37.0.linux-amd64/promtool

cd prometheus-2.37.0.linux-amd64/
/home/devuser/ES/prometheus-2.37.0.linux-amd64/prometheus --config.file=/home/devuser/ES/prometheus-2.37.0.linux-amd64/prometheus.yml --storage.tsdb.retention.time=2d --storage.tsdb.retention.size=1GB --web.enable-admin-api --storage.tsdb.path=./

sudo cp /home/devuser/ES/prometheus-2.37.0.linux-amd64/prometheus /usr/local/bin/prometheus
sudo chown devuser /usr/local/bin/prometheus
 ```
 
 
### Test configuration file
```
/usr/local/bin/prometheus --config.file=/home/devuser/ES/prometheus-2.37.0.linux-amd64/prometheus.yml --storage.tsdb.retention.time=2d --storage.tsdb.retention.size=1GB --web.enable-admin-api --storage.tsdb.path=./
```

### Register the service for Prometheus systemd 
```
sudo vi /etc/systemd/system/prometheus.service

[Unit]
Description=Prometheus
Wants=network-online.target
After=network-online.target

[Service]
User=devuser
Group=devuser
Type=simple
WorkingDirectory=/home/devuser/ES/prometheus-2.37.0.linux-amd64
ExecStart=/usr/local/bin/prometheus --config.file=/home/devuser/ES/prometheus-2.37.0.linux-amd64/prometheus.yml --storage.tsdb.retention.time=2d --storage.tsdb.retention.size=1GB --web.enable-admin-api --storage.tsdb.path=./

[Install]
WantedBy=multi-user.target

# Run service
systemctl daemon-reload
# Autostart when rebooting
sudo systemctl enable prometheus.service
systemctl start prometheus
```
 
 
### Prometheus Log
```
 devuser@ubuntu-master-1:~/ES/prometheus-2.37.0.linux-amd64$ /home/devuser/ES/prometheus-2.37.0.linux-amd64/prometheus --storage.tsdb.retention.time=2d
ts=2023-09-28T04:11:16.489Z caller=main.go:535 level=info msg="Starting Prometheus Server" mode=server version="(version=2.37.0, branch=HEAD, revision=b41e0750abf5cc18d8233161560731de05199330)"
ts=2023-09-28T04:11:16.490Z caller=main.go:540 level=info build_context="(go=go1.18.4, user=root@0ebb6827e27f, date=20220714-15:13:18)"
ts=2023-09-28T04:11:16.491Z caller=main.go:541 level=info host_details="(Linux 5.15.0-83-generic #92-Ubuntu SMP Mon Aug 14 09:34:05 UTC 2023 x86_64 ubuntu-master-1 (none))"
ts=2023-09-28T04:11:16.491Z caller=main.go:542 level=info fd_limits="(soft=1024, hard=1048576)"
ts=2023-09-28T04:11:16.491Z caller=main.go:543 level=info vm_limits="(soft=unlimited, hard=unlimited)"
ts=2023-09-28T04:11:16.515Z caller=web.go:553 level=info component=web msg="Start listening for connections" address=0.0.0.0:9090
ts=2023-09-28T04:11:16.523Z caller=main.go:972 level=info msg="Starting TSDB ..."
ts=2023-09-28T04:11:16.541Z caller=tls_config.go:195 level=info component=web msg="TLS is disabled." http2=false
ts=2023-09-28T04:11:16.555Z caller=head.go:493 level=info component=tsdb msg="Replaying on-disk memory mappable chunks if any"
ts=2023-09-28T04:11:16.557Z caller=head.go:536 level=info component=tsdb msg="On-disk memory mappable chunks replay completed" duration=1.934708ms
ts=2023-09-28T04:11:16.558Z caller=head.go:542 level=info component=tsdb msg="Replaying WAL, this may take a while"
ts=2023-09-28T04:11:16.584Z caller=head.go:613 level=info component=tsdb msg="WAL segment loaded" segment=0 maxSegment=3
ts=2023-09-28T04:11:16.591Z caller=head.go:613 level=info component=tsdb msg="WAL segment loaded" segment=1 maxSegment=3
ts=2023-09-28T04:11:16.595Z caller=head.go:613 level=info component=tsdb msg="WAL segment loaded" segment=2 maxSegment=3
ts=2023-09-28T04:11:16.595Z caller=head.go:613 level=info component=tsdb msg="WAL segment loaded" segment=3 maxSegment=3
ts=2023-09-28T04:11:16.596Z caller=head.go:619 level=info component=tsdb msg="WAL replay completed" checkpoint_replay_duration=335.833µs wal_replay_duration=37.422009ms total_replay_duration=40.028468ms
ts=2023-09-28T04:11:16.603Z caller=main.go:993 level=info fs_type=EXT4_SUPER_MAGIC
ts=2023-09-28T04:11:16.603Z caller=main.go:996 level=info msg="TSDB started"
ts=2023-09-28T04:11:16.603Z caller=main.go:1177 level=info msg="Loading configuration file" filename=prometheus.yml
ts=2023-09-28T04:11:16.614Z caller=main.go:1214 level=info msg="Completed loading of configuration file" filename=prometheus.yml totalDuration=10.83167ms db_storage=82.667µs remote_storage=182.042µs web_handler=53.792µs query_engine=70.667µs scrape=4.620793ms scrape_sd=946.625µs notify=1.783292ms notify_sd=286.5µs rules=210µs tracing=1.118334ms
ts=2023-09-28T04:11:16.614Z caller=main.go:957 level=info msg="Server is ready to receive web requests."
ts=2023-09-28T04:11:16.615Z caller=manager.go:941 level=info component="rule manager" msg="Starting rule manager..."
 ```
 
 ### Run
```
http://192.168.64.2:9090/targets?search=
```
### Guide
```
https://velog.io/@enosoup/PostgreSQLExporter-%EA%B5%AC%EC%84%B1
https://nelsoncode.medium.com/how-to-monitor-posgresql-with-prometheus-and-grafana-docker-36d216532ea2
```

### Docker Version
```
  postgres-exporter:
    image: prometheuscommunity/postgres-exporter
    ports:
      - 9187:9187
    environment:
      DATA_SOURCE_NAME: "postgresql://postgres:1234@host.docker.internal:15432/postgres?sslmode=disable"
    links:
      # - postgres
      - prometheus
    networks:
      - bridge
```


### Download and unpack
```
wget https://github.com/wrouesnel/postgres_exporter/releases/download/v0.8.0/postgres_exporter_v0.8.0_linux-amd64.tar.gz
tar -zxvf postgres_exporter_v0.8.0_linux-amd64.tar.gz
postgres_exporter_v0.8.0_linux-amd64/
postgres_exporter_v0.8.0_linux-amd64/postgres_exporter

cd postgres_exporter_v0.8.0_linux-amd64/
export DATA_SOURCE_NAME=postgresql://postgres:1234@192.168.64.1:15432/postgres?sslmode=disable
/home/devuser/ES/postgres_exporter_v0.8.0_linux-amd64/postgres_exporter

sudo cp /home/devuser/ES/postgres_exporter_v0.8.0_linux-amd64/postgres_exporter /usr/local/bin/postgres_exporter
sudo chown devuser /usr/local/bin/postgres_exporter
 ```
 
 
### Test configuration file
```
/usr/local/bin/postgres_exporter
```

### Register the service for postgres_exporter systemd 
```
sudo vi /etc/systemd/system/postgres_exporter.service

[Unit]
Description=Prometheus PostgreSQL Exporter
After=network.target

[Service]
Type=simple
#Restart=always
User=devuser
Group=devuser
#Environment=DATA_SOURCE_NAME="user=postgres host=/var/run/postgresql/ sslmode=disable"
Environment=DATA_SOURCE_NAME=postgresql://postgres:1234@192.168.64.1:15432/postgres?sslmode=disable
ExecStart=/usr/local/bin/postgres_exporter
#ExecStart=/home/devuser/ES/postgres_exporter_v0.8.0_linux-amd64/postgres_exporter
[Install]
WantedBy=multi-user.target


# Run service
systemctl daemon-reload
# Autostart when rebooting
sudo systemctl enable postgres_exporter.service
systemctl start postgres_exporter
```
 
 
### Prometheus Log
```
devuser@ubuntu-master-1:~/ES/postgres_exporter_v0.8.0_linux-amd64$ systemctl status postgres_exporter.service
● postgres_exporter.service - Prometheus PostgreSQL Exporter
     Loaded: loaded (/etc/systemd/system/postgres_exporter.service; enabled; vendor preset: enabled)
     Active: active (running) since Wed 2023-10-04 17:01:38 CDT; 20s ago
   Main PID: 2738 (postgres_export)
      Tasks: 11 (limit: 976)
     Memory: 22.7M
        CPU: 518ms
     CGroup: /system.slice/postgres_exporter.service
             └─2738 /usr/libexec/qemu-binfmt/x86_64-binfmt-P /usr/local/bin/postgres_exporter /usr/local/bin/postgres_exporter

Oct 04 17:01:38 ubuntu-master-1 systemd[1]: Started Prometheus PostgreSQL Exporter.
Oct 04 17:01:38 ubuntu-master-1 postgres_exporter[2738]: time="2023-10-04T17:01:38-05:00" level=info msg="Established new database connection to \"192.168.64.1:15432\"." source="postgr>
Oct 04 17:01:38 ubuntu-master-1 postgres_exporter[2738]: time="2023-10-04T17:01:38-05:00" level=info msg="Semantic Version Changed on \"192.168.64.1:15432\": 0.0.0 -> 15.3.0" source="p>
Oct 04 17:01:39 ubuntu-master-1 postgres_exporter[2738]: time="2023-10-04T17:01:39-05:00" level=info msg="Starting Server: :9187" source="postgres_exporter.go:1672" 
```
 
 ### Run
```
journalctl -u postgres_exporter.service
http://localhost:9187/metrics
https://grafana.com/grafana/dashboards/9628-postgresql-database/
```
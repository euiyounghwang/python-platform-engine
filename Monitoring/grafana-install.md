### Guide
```
https://grafana.com/grafana/download?platform=arm
https://veneas.tistory.com/entry/Linux-CentOS7-%EA%B7%B8%EB%9D%BC%ED%8C%8C%EB%82%98Grafana-%EC%84%A4%EC%B9%98%ED%95%98%EA%B8%B0-Data-Visualization
```

### Docker Version
```
grafana:
    container_name: grafana
    environment:
      GF_INSTALL_PLUGINS: alexanderzobnin-zabbix-app
    image: grafana/grafana:latest
    ports:
      - 3001:3000/tcp
    volumes:
      - /etc/localtime:/etc/localtime:ro
    restart: unless-stopped
    networks:
      - bridge
```


### Download and unpack
```
wget https://dl.grafana.com/enterprise/release/grafana-enterprise-10.1.2.linux-arm64.tar.gz
tar -zxvf grafana-enterprise-10.1.2.linux-arm64.tar.gz

cd grafana-10.1.2/
/home/devuser/ES/grafana-10.1.2/bin/grafana-server

#sudo cp /home/devuser/ES/grafana-10.1.2/bin/grafana-server /usr/local/bin/grafana
#sudo chown devuser /usr/local/bin/grafana
 ```
 
 
### Test configuration file
```
/usr/local/bin/grafana
```

### Register the service for grafana systemd 
```
sudo vi /etc/systemd/system/grafana.service

[Unit]
Description=grafana
Wants=network-online.target
After=network-online.target

[Service]
User=devuser
Group=devuser
Type=simple
WorkingDirectory=/home/devuser/ES/grafana-10.1.2
ExecStart=/home/devuser/ES/grafana-10.1.2/bin/grafana-server

[Install]
WantedBy=multi-user.target

# Run service
systemctl daemon-reload
# Autostart when rebooting
sudo systemctl enable grafana.service
systemctl start grafana
```
 
 
### Grafana Log
```
devuser@ubuntu-master-1:~/ES/grafana-10.1.2$ systemctl status grafana.service
● grafana.service - grafana
     Loaded: loaded (/etc/systemd/system/grafana.service; enabled; vendor preset: enabled)
     Active: active (running) since Thu 2023-09-28 18:07:14 CDT; 13s ago
   Main PID: 149118 (grafana)
      Tasks: 16 (limit: 976)
     Memory: 85.8M
        CPU: 2.478s
     CGroup: /system.slice/grafana.service
             └─149118 grafana server

Sep 28 18:07:16 ubuntu-master-1 grafana-server[149118]: logger=ngalert.state.manager t=2023-09-28T18:07:16.242738508-05:00 level=info msg="State cache has been initialized" st>
Sep 28 18:07:16 ubuntu-master-1 grafana-server[149118]: logger=ngalert.scheduler t=2023-09-28T18:07:16.242800884-05:00 level=info msg="Starting scheduler" tickInterval=10s
Sep 28 18:07:16 ubuntu-master-1 grafana-server[149118]: logger=ticker t=2023-09-28T18:07:16.242853509-05:00 level=info msg=starting first_tick=2023-09-28T18:07:20-05:00
Sep 28 18:07:16 ubuntu-master-1 grafana-server[149118]: logger=ngalert.multiorg.alertmanager t=2023-09-28T18:07:16.242873592-05:00 level=info msg="Starting MultiOrg Alertmanag>
Sep 28 18:07:16 ubuntu-master-1 grafana-server[149118]: logger=grafanaStorageLogger t=2023-09-28T18:07:16.242949759-05:00 level=info msg="storage starting"
Sep 28 18:07:16 ubuntu-master-1 grafana-server[149118]: logger=caching.service t=2023-09-28T18:07:16.243998264-05:00 level=warn msg="Caching service is disabled"
Sep 28 18:07:16 ubuntu-master-1 grafana-server[149118]: logger=report t=2023-09-28T18:07:16.253822265-05:00 level=warn msg="Scheduling and sending of reports disabled, SMTP is>
Sep 28 18:07:16 ubuntu-master-1 grafana-server[149118]: logger=grafana.update.checker t=2023-09-28T18:07:16.330887479-05:00 level=info msg="Update check succeeded" duration=87>
Sep 28 18:07:16 ubuntu-master-1 grafana-server[149118]: logger=plugins.update.checker t=2023-09-28T18:07:16.336570337-05:00 level=info msg="Update check succeeded" duration=92>
lines 2-19
 ```
 
### Run
```
http://192.168.64.2:3000/alerting/list
http://192.168.64.2:9090/targets?search=
http://192.168.64.2:9093/#/alerts
```

### Reset the password
```
grafana-cli admin reset-admin-password admin
```

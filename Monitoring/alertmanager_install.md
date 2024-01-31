### Guide
```
https://hippogrammer.tistory.com/260
https://gist.github.com/Tumar/cd1ef5ecd88086d49d04d9a4205f4763
```

### Docker Version
```
  alertmanager:
    image: prom/alertmanager
    container_name: alertmanager
    privileged: true
    volumes:
      - ./alertmanager/alertmanager.yml:/alertmanager.yml
      - ./alertmanager/slack.tmpl:/slack.tmpl
    command:
      - '--config.file=/alertmanager.yml'
      - "--web.external-url=http://localhost:9093"
    ports:
      - 9093:9093
```

### Create user
```
useradd --no-create-home --shell /bin/false alertmanager
```

### Download and unpack
```
wget https://github.com/prometheus/alertmanager/releases/download/v0.20.0/alertmanager-0.20.0.linux-amd64.tar.gz
tar -xvf alertmanager-0.20.0.linux-amd64.tar.gz
alertmanager-0.20.0.linux-amd64/
alertmanager-0.20.0.linux-amd64/LICENSE
alertmanager-0.20.0.linux-amd64/alertmanager
alertmanager-0.20.0.linux-amd64/amtool
alertmanager-0.20.0.linux-amd64/NOTICE
alertmanager-0.20.0.linux-amd64/alertmanager.yml

#mv alertmanager-0.20.0.linux-amd64/alertmanager /usr/local/bin/
#mv alertmanager-0.20.0.linux-amd64/amtool /usr/local/bin/

#chown alertmanager:alertmanager /usr/local/bin/alertmanager
#chown alertmanager:alertmanager /usr/local/bin/amtool

sudo cp /home/devuser/ES/alertmanager-0.20.0.linux-amd64/alertmanager /usr/local/bin/alertmanager
sudo chown devuser /usr/local/bin/alertmanager
```

### Cleanup
```
rm -rf /home/devuser/ES/alertmanager-0.20.0*
```

### Create configuration file
```
#mkdir /etc/alertmanager
#nano /etc/alertmanager/alertmanager.yml
vi /home/devuser/ES/alertmanager-0.20.0.linux-amd64/alertmanager.yml
```

### Test configuration file
```
/usr/local/bin/alertmanager --config.file=/home/devuser/ES/alertmanager-0.20.0.linux-amd64/alertmanager.yml
```

### Register the service for Alertmanager systemd 
```
sudo vi /etc/systemd/system/alertmanager.service

[Unit]
Description=Alertmanager
Wants=network-online.target
After=network-online.target

[Service]
User=devuser
Group=devuser
Type=simple
WorkingDirectory=/home/devuser/ES/alertmanager-0.20.0.linux-amd64
ExecStart=/usr/local/bin/alertmanager --config.file=/home/devuser/ES/alertmanager-0.20.0.linux-amd64/alertmanager.yml --web.external-url http://0.0.0.0:9093

[Install]
WantedBy=multi-user.target

# Run service
systemctl daemon-reload
# Autostart when rebooting
sudo systemctl enable alertmanager.service
systemctl start alertmanager
```


### alertmanager.service log
```
# systemctl status alertmanager.service

● alertmanager.service - Alertmanager
     Loaded: loaded (/etc/systemd/system/alertmanager.service; disabled; vendor preset: enabled)
     Active: active (running) since Wed 2023-09-27 22:11:50 CDT; 2s ago
   Main PID: 47930 (alertmanager)
      Tasks: 16 (limit: 976)
     Memory: 33.8M
        CPU: 700ms
     CGroup: /system.slice/alertmanager.service
             └─47930 /usr/libexec/qemu-binfmt/x86_64-binfmt-P /usr/local/bin/alertmanager /usr/local/bin/alertmanager --config.file=/home/devuser/ES/alertmanager-0.20.0.linux-amd64/ale>

Sep 27 22:11:50 ubuntu-master-1 systemd[1]: Started Alertmanager.
Sep 27 22:11:51 ubuntu-master-1 alertmanager[47930]: level=info ts=2023-09-28T03:11:51.104Z caller=main.go:231 msg="Starting Alertmanager" version="(version=0.20.0, branch=HEAD, revisi>
Sep 27 22:11:51 ubuntu-master-1 alertmanager[47930]: level=info ts=2023-09-28T03:11:51.107Z caller=main.go:232 build_context="(go=go1.13.5, user=root@00c3106655f8, date=20191211-14:13:>
Sep 27 22:11:51 ubuntu-master-1 alertmanager[47930]: level=info ts=2023-09-28T03:11:51.135Z caller=cluster.go:161 component=cluster msg="setting advertise address explicitly" addr=192.>
Sep 27 22:11:51 ubuntu-master-1 alertmanager[47930]: level=info ts=2023-09-28T03:11:51.162Z caller=cluster.go:623 component=cluster msg="Waiting for gossip to settle..." interval=2s
Sep 27 22:11:51 ubuntu-master-1 alertmanager[47930]: level=info ts=2023-09-28T03:11:51.325Z caller=coordinator.go:119 component=configuration msg="Loading configuration file" file=/hom>
Sep 27 22:11:51 ubuntu-master-1 alertmanager[47930]: level=info ts=2023-09-28T03:11:51.339Z caller=coordinator.go:131 component=configuration msg="Completed loading of configuration fi>
Sep 27 22:11:51 ubuntu-master-1 alertmanager[47930]: level=info ts=2023-09-28T03:11:51.363Z caller=main.go:497 msg=Listening address=:9093
Sep 27 22:11:53 ubuntu-master-1 alertmanager[47930]: level=info ts=2023-09-28T03:11:53.165Z caller=cluster.go:648 component=cluster msg="gossip not settled" polls=0 before=0 now=1 elap>
```
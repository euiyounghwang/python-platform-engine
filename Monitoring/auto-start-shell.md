
<i>
#### https://www.linuxbabe.com/linux-server/how-to-enable-etcrc-local-with-systemd

sudo firewall-cmd --zone=public --add-port=9101/tcp --permanent
sudo firewall-cmd --reload


```bash
sudo vi /etc/rc.d/rc.local

# Dev-Kibana
/home/devuser/monitoring/prometheus-run.sh start
/home/devuser/monitoring/grafana-run.sh start
/home/devuser/monitoring/elasticsearch-export-run.sh start

# Logstash
/home/devuser/monitoring/node-export-run.sh start

sudo vi /etc/systemd/system/rc-local.service

--
[Unit]
 Description=/etc/rc.local Compatibility
 ConditionPathExists=/etc/rc.local

[Service]
 Type=forking
 ExecStart=/etc/rc.local start
 TimeoutSec=0
 StandardOutput=tty
 RemainAfterExit=yes
 SysVStartPriority=99

[Install]
 WantedBy=multi-user.target
--
```

sudo chmod 755 /etc/rc.local

sudo systemctl enable rc-local
# stop the service all
sudo systemctl status rc-local.service
sudo service rc-local status

sudo systemctl start rc-local.service
sudo service rc-local start
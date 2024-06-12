
# Infrastructure
<i> Setup/Command

#### Boot Auto Script
```bash

sudo vi /etc/rc.d/rc.local

# Dev-Kibana
/home/devuser/monitoring/prometheus-run.sh start
/home/devuser/monitoring/grafana-run.sh start
/home/devuser/monitoring/elasticsearch-export-run.sh start
/home/devuser/monitoring/custom_export/standalone-es-service-export.sh start

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

# sudo systemctl disable rc-local

sudo chmod 755 /etc/rc.local && sudo systemctl enable rc-local

# stop the service all
sudo systemctl status rc-local.service
sudo service rc-local status

sudo systemctl start rc-local.service
sudo service rc-local start
```


#### Firewall
```bash
sudo firewall-cmd --zone=public --add-port=5901/tcp --permanent
sudo firewall-cmd --zone=public --add-port=9090/tcp --permanent
sudo firewall-cmd --zone=public --add-port=3000/tcp --permanent
sudo firewall-cmd --zone=public --add-port=8083/tcp --permanent
sudo firewall-cmd --zone=public --add-port=9092/tcp --permanent
sudo firewall-cmd --reload
```

#### Monitoring
```bash
#***************************************
#***************************************
# spacecheck.sh
#***************************************
#***************************************

#  /apps/devuser/UtilityScripts/spacecheck.sh on this node 
# -#### spacecheck.sh
CURRENT=$(df /apps | grep / | awk '{ print $5}' | sed 's/%//g')
THRESHOLD=85
echo $CURRENT
if [ "$CURRENT" -gt "$THRESHOLD" ] ; then
   echo here
    mailx -s 'Disk Space Alert' marieuig@gmail.com << EOF
Your localhost apps partition remaining free space is critically low. Used: $CURRENT%
EOF
fi

# ---
# #### Prometheus (URL : http://localhost:9090)
wget https://github.com/prometheus/prometheus/releases/download/v2.37.0/prometheus-2.37.0.linux-amd64.tar.gz
tar -zxvf prometheus-2.37.0.linux-amd64.tar.gz
cd prometheus-2.37.0.linux-amd64/

#/home/devuser/monitoring/prometheus-2.37.0.linux-amd64/prometheus --config.file=/home/devuser/monitoring/prometheus-2.37.0.linux-amd64/prometheus.yml --storage.tsdb.retention.time=14d --storage.tsdb.retention.size=2GB --web.enable-admin-api --storage.tsdb.path=/home/devuser/monitoring/prometheus-2.37.0.linux-amd64/
#nohup /home/devuser/monitoring/prometheus-2.37.0.linux-amd64/prometheus --config.file=/home/devuser/monitoring/prometheus-2.37.0.linux-amd64/prometheus.yml --storage.tsdb.retention.time=14d --storage.tsdb.retention.size=2GB --web.enable-admin-api --storage.tsdb.path=/home/devuser/monitoring/prometheus-2.37.0.linux-amd64/ &> /dev/null &

# -#### run prometheus shell
#nohup /home/devuser/monitoring/prometheus-run.sh &> /dev/null &

#-rw-rw-r-####  1 devuser devuser    20001 Apr 10 09:20 queries.active
#[devuser@localhost monitoring]$ ps -ef | grep prometheus
#devuser  27159 13306  0 11:00 pts/1    00:00:00 /bin/sh /home/devuser/monitoring/prometheus-run.sh
#devuser  27160 27159  1 11:00 pts/1    00:00:01 /home/devuser/monitoring/prometheus-2.37.0.linux-amd64/prometheus --config.file=/home/devuser/monitoring/prometheus-2.37.0.linux-amd64/prometheus.yml --storage.tsdb.retention.time=14d --storage.tsdb.retention.size=2GB --web.enable-admin-api --storage.tsdb.path=/home/devuser/monitoring/prometheus-2.37.0.linux-amd64/
#devuser  27580 13306  0 11:02 pts/1    00:00:00 grep --color=auto prometheus

./prometheus-run.sh status
./prometheus-run.sh stop
./prometheus-run.sh start
./prometheus-run.sh status

[devuser@localhost monitoring]$ ./prometheus-run.sh status
prometheus-service is not Running
[devuser@localhost monitoring]$ ./prometheus-run.sh start
Starting prometheus-service
[devuser@localhost monitoring]$ ./prometheus-run.sh status
prometheus-service is Running as PID: 56134
[devuser@localhost monitoring]$ ps -ef | grep pro
devuser  56134     1 51 14:35 pts/1    00:00:02 /home/devuser/monitoring/prometheus-2.37.0.linux-amd64//prometheus --config.file=/home/devuser/monitoring/prometheus-2.37.0.linux-amd64//prometheus.yml --storage.tsdb.retention.time=14d --storage.tsdb.retention.size=2GB --web.enable-admin-api --storage.tsdb.path=/home/devuser/monitoring/prometheus-2.37.0.linux-amd64/
devuser  56155 54053  0 14:35 pts/1    00:00:00 grep --color=auto pro
[devuser@localhost monitoring]$ ./prometheus-run.sh restart
Shutting down prometheus-service
Starting prometheus-service
[devuser@localhost monitoring]$ ./prometheus-run.sh status
prometheus-service is Running as PID: 56175

FYI)
$ sudo vim /usr/lib/systemd/system/prometheus.service
[Unit]
Description=Prometheus
Wants=network-online.target
After=network-online.target

[Service]
User=prometheus
Group=prometheus
Type=simple
ExecStart=/usr/local/bin/prometheus \
--config.file /etc/prometheus/prometheus.yml \
--storage.tsdb.path /var/lib/prometheus/ \
--web.console.templates=/var/lib/prometheus/consoles \
--web.console.libraries=/var/lib/prometheus/console_libraries \
--storage.tsdb.retention=90d 

[Install]
WantedBy=multi-user.target
# ---


# ---
# #### Grafana (URL : http://localhost:3000)
/home/devuser/monitoring/grafana-4.1.2-1486989747

#--
# vi ./conf/default.ini without login
[auth]
# Set to true to disable (hide) the login form, useful if you use OAuth
disable_login_form = true

#################################### Anonymous Auth ######################
[auth.anonymous]
# enable anonymous access
enabled = true

# specify organization name that should be used for unauthenticated users
org_name = Main Org.

# specify role for unauthenticated users
org_role = Viewer

hide_version = false

# set to true if you want to allow browsers to render Grafana in a <frame>, <iframe>, <embed> or <object>. default is false.
allow_embedding = true
#--

# #### run command
nohup /home/devuser/monitoring/grafana-4.1.2-1486989747/bin/grafana-server --homepath /home/devuser/monitoring/grafana-4.1.2-1486989747 --config=/home/devuser/monitoring/grafana-4.1.2-1486989747/conf/defaults.ini &> /dev/null &

# -#### run prometheus shell
# nohup /home/devuser/monitoring/grafana-run.sh &> /dev/null &

#[devuser@localhost monitoring]$ ps -ef | grep grafana
#devuser  28724 13306  0 11:10 pts/1    00:00:00 /bin/sh /home/devuser/monitoring/grafana-run.sh
#devuser  28726 28724  0 11:10 pts/1    00:00:00 /home/devuser/monitoring/grafana-4.1.2-1486989747/bin/grafana-server --homepath /home/devuser/monitoring/grafana-4.1.2-1486989747 --config=/home/devuser/monitoring/grafana-4.1.2-1486989747/conf/defaults.ini
#devuser  28742 13306  0 11:10 pts/1    00:00:00 grep --color=auto grafana
#[devuser@localhost monitoring]$ kill -9 28726
#[devuser@localhost monitoring]$
#[7]+  Exit 137                nohup /home/devuser/monitoring/grafana-run.sh &>/dev/null
#[devuser@localhost monitoring]$
#[devuser@localhost monitoring]$ ps -ef | grep grafana
#devuser  28765 13306  0 11:11 pts/1    00:00:00 grep --color=auto grafana
#[devuser@localhost monitoring]$ ps -ef | grep grafana
#devuser  28768 13306  0 11:11 pts/1    00:00:00 grep --color=auto grafana


 ./grafana-run.sh status
 ./grafana-run.sh stop
 ./grafana-run.sh start
 ./grafana-run.sh status

[devuser@localhost monitoring]$ ./grafana-run.sh status
grafana-service is Running as PID: 55941
[devuser@localhost monitoring]$ ./grafana-run.sh start
Starting grafana-service
[devuser@localhost monitoring]$ ./grafana-run.sh restart
Shutting down grafana-service
Starting grafana-service
[devuser@localhost monitoring]$ ./grafana-run.sh status
grafana-service is Running as PID: 55941

[devuser@localhost monitoring]$ ps -ef | grep grafana
devuser  55941     1  1 14:32 pts/1    00:00:00 /home/devuser/monitoring/grafana-4.1.2-1486989747//bin/grafana-server --homepath /home/devuser/monitoring/grafana-4.1.2-1486989747/ --config= /home/devuser/monitoring/grafana-4.1.2-1486989747//conf/defaults.ini
devuser  55959 54053  0 14:32 pts/1    00:00:00 grep --color=auto grafana
[devuser@localhost monitoring]$ ls

# ---


# ---
# #### Elasticsearch_Exporter (https://github.com/prometheus-community/elasticsearch_exporter)

[devuser@localhost monitoring]$ tar -zxvf elasticsearch_exporter-1.6.0.linux-386.tar.gz
elasticsearch_exporter-1.6.0.linux-386/
elasticsearch_exporter-1.6.0.linux-386/CHANGELOG.md
elasticsearch_exporter-1.6.0.linux-386/elasticsearch.rules
elasticsearch_exporter-1.6.0.linux-386/dashboard.json
elasticsearch_exporter-1.6.0.linux-386/deployment.yml
elasticsearch_exporter-1.6.0.linux-386/elasticsearch_exporter
elasticsearch_exporter-1.6.0.linux-386/README.md
elasticsearch_exporter-1.6.0.linux-386/LICENSE
[devuser@localhost monitoring]$ cd elasticsearch_exporter-1.6.0.linux-386

# #### run command (Dev)
# nohup /home/devuser/monitoring/elasticsearch_exporter-1.6.0.linux-386/elasticsearch_exporter --es.uri=http://localhost:9200 --es.all --es.indices --es.timeout 20s --es.snapshots  &> /dev/null &
# nohup /home/devuser/monitoring/elasticsearch-export-run.sh &> /dev/null &

 ./elasticsearch-export-run.sh status
 ./elasticsearch-export-run.sh stop
 ./elasticsearch-export-run.sh start
 ./elasticsearch-export-run.sh status


[devuser@localhost monitoring]$ pwd
/home/devuser/monitoring

[devuser@localhost monitoring]$ ./elasticsearch-export-run.sh status
elasticsearch-export-service is Running as PID: 35206
[devuser@localhost monitoring]$ ./elasticsearch-export-run.sh stop
Shutting down elasticsearch-export-service
[devuser@localhost monitoring]$ ./elasticsearch-export-run.sh start
Starting elasticsearch-export-service
[devuser@localhost monitoring]$ ps -ef | grep elastic
devuser  35425     1  3 12:34 pts/1    00:00:00 /home/devuser/monitoring/elasticsearch_exporter-1.6.0.linux-386//elasticsearch_exporter --es.uri=http://localhost:9200 --es.all --es.indices --es.timeout 20s --es.snapshots
devuser  35440 13306  0 12:34 pts/1    00:00:00 grep --color=auto elastic



# #### run command (QA1)
# /home/devuser/monitoring/elasticsearch_exporter-1.6.0.linux-386/elasticsearch_exporter --es.uri=http://localohost:9200 --es.all --es.indices --es.timeout 20s --es.snapshots
# nohup /home/devuser/monitoring/elasticsearch_exporter-1.6.0.linux-386/elasticsearch_exporter --es.uri=http://localohost:9200 --es.all --es.indices --es.timeout 20s --es.snapshots  &> /dev/null &

# -#### run prometheus shell
# nohup /home/devuser/monitoring/elasticsearch-export-run.sh &> /dev/null &

#[devuser@localhost monitoring]$ ps -ef | grep elastic
#devuser  50726 50353  0 10:32 pts/2    00:00:00 /bin/sh /home/devuser/monitoring/elasticsearch-export-run.sh
#devuser  50728 50726  0 10:32 pts/2    00:00:00 /home/devuser/monitoring/elasticsearch_exporter-1.6.0.linux-386/elasticsearch_exporter --es.uri=http://localohost:9200 --es.all --es.indices --es.timeout 20s --es.snapshots
#devuser  50743 50353  0 10:32 pts/2    00:00:00 grep --color=auto elastic


 ./elasticsearch-export-run.sh status
 ./elasticsearch-export-run.sh stop
 ./elasticsearch-export-run.sh start
 ./elasticsearch-export-run.sh status


[devuser@localhost monitoring]$ pwd
/home/devuser/monitoring

[devuser@localhost monitoring]$ ./elasticsearch-export-run.sh status
elasticsearch-export-service is Running as PID: 35206
[devuser@localhost monitoring]$ ./elasticsearch-export-run.sh stop
Shutting down elasticsearch-export-service
[devuser@localhost monitoring]$ ./elasticsearch-export-run.sh start
Starting elasticsearch-export-service
[devuser@localhost monitoring]$ ps -ef | grep elastic
devuser   5937     1  2 12:39 pts/2    00:00:00 /home/devuser/monitoring/elasticsearch_exporter-1.6.0.linux-386//elasticsearch_exporter --es.uri=http://localohost:9200 --es.all --es.indices --es.timeout 20s --es.snapshots
devuser   5955  5759  0 12:39 pts/2    00:00:00 grep --color=auto elastic
# ---
```


#### Service Stop/Start
```bash
1) Stop Services: 

Stop Spark custom job. 
#### http://localhost:8080/
#### http://localhost:8080/  (kill click for jobs)
Stop Spark Cluster. 
#### sudo su -l spark  
#### /apps/spark-2.2.0-bin-hadoop2.7/sbin/stop-all.sh
Pause OM/WM listeners. 
Stop Kafka Connect – all 3 nodes.
#### sudo utils/connectUtil.sh status
#### sudo utils/connectUtil.sh stop
#### sudo utils/status_kafka_connect.sh
#### sudo netstat -nlp | grep :8083
#### curl -XGET  'localhost:8083/connectors/source-postgres1/status' | jq 
#### curl -XGET  'localhost:8083/connectors/source-postgres1/status' | jq 
#### curl -XGET  'localhost:8083/connectors/source-postgres2/status' | jq
Stop Kafka/ZooKeeper – all 3 nodes. 
#### sudo utils/kafkaUtil.sh status
#### sudo utils/kafkaUtil.sh stop
Stop ElasticSearch – all 3 nodes. 
#### sudo service elasticsearch stop
#### ps -ef | grep elastic
Stop Logstash 
#### sudo service logstash stop
Stop Kibana : Get the pid for port 5601 using ‘netstat’ command and kill the process.
#### ps -ef | grep kibana
#### sudo kill -9 process_id 
#### sudo netstat -nlp | grep :5601

 

2) Start Services: 
Start ElasticSearch – all 3 nodes. 
#### sudo service elasticsearch start
#### ps -ef | grep elastic
#### curl http://localhost:9200
Start Logstash 
#### sudo service logstash start
Start Kibana 
#### sudo /apps/kibana/latest/bin/kibana & 
#### ps -ef | grep kibana
#### curl http://localhost:5601
#### sudo netstat -nlp | grep :5601
Start Kafka/ZooKeeper – all 3 nodes 
#### sudo utils/kafkaUtil.sh start
Start Kafka Connect – all 3 nodes. 
#### sudo utils/connectUtil.sh start
#### sudo utils/status_kafka_connect.sh
#### sudo netstat -nlp | grep :8083
#### curl -XGET  'localhost:8083/connectors/source-postgres1/status' | jq 
#### curl -XGET  'localhost:8083/connectors/source-postgres2/status' | jq 
#### curl -XGET  'localhost:8083/connectors' | jq 
Resume/Restart OM/WM listeners. 
Start Spark Cluster 
#### sudo su -l spark
#### /apps/spark-2.2.0-bin-hadoop2.7/sbin/start-all.sh
#### http://localhost:8080/
Start Spark custom jobs. 
#### sudo su -l spark
#### utils/sparkSubmit.sh start
#### http://localhost:8080/
#### http://localhost:8080/
```


#### VirtualBox Install
```bash
[devuser@localhost ~]$ exit
logout
Connection to 192.168.1.243 closed.
(base) PS C:\Users\euiyoung.hwang> ssh devuser@192.168.1.243 -p25022
ssh: connect to host 192.168.1.243 port 25022: Connection refused
(base) PS C:\Users\euiyoung.hwang> ssh devuser@192.168.1.243 -p25022
ssh: connect to host 192.168.1.243 port 25022: Connection refused
(base) PS C:\Users\euiyoung.hwang> ssh devuser@192.168.1.243 -p25022
ssh: connect to host 192.168.1.243 port 25022: Connection refused
(base) PS C:\Users\euiyoung.hwang> ssh devuser@192.168.1.243 -p25022
ssh: connect to host 192.168.1.243 port 25022: Connection refused
(base) PS C:\Users\euiyoung.hwang> ssh devuser@192.168.1.243 -p25022
The authenticity of host '[192.168.1.243]:25022 ([192.168.1.243]:25022)' can't be established.
ECDSA key fingerprint is SHA256:olOtLfUDWM/7+zMt+PFK1ijNuplDFT/7bDAyo7JxoOw.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '[192.168.1.243]:25022' (ECDSA) to the list of known hosts.
devuser@192.168.1.243's password:
Last login: Thu Mar 28 21:42:53 2024


su root

vi /etc/sudoers
## Allow root to run any commands anywhere
root    ALL=(ALL)       ALL
devuser ALL=(ALL)       ALL
#devsuer ALL=(ALL:ALL) ALL


This system is not registered with an entitlement server. You can use subscription-manager to register.


(base) PS C:\Users\euiyoung.hwang\.ssh> ssh devuser@192.168.1.243 -p15022


#***************************************
#***************************************
# Python3.9.X Install
#***************************************
#***************************************

# ssh-key for GIT
sudo yum install git -y
ssh-keygen -t rsa
eval $(ssh-agent -s)
cat ~/.ssh/id_rsa.pub

sudo yum groupinstall 'development tools' -y 
sudo yum install wget openssl-devel bzip2-devel libffi-devel xz-devel sqlite-devel  -y

wget https://www.python.org/ftp/python/3.9.6/Python-3.9.6.tgz
tar xvf Python-3.9.6.tgz
cd Python-3.9.6 && ./configure --enable-optimizations
./configure --libdir=/usr/lib64 
sudo make
sudo make altinstall
sudo ln -s /usr/lib64/python3.9/lib-dynload/ /usr/local/lib/python3.9/lib-dynload

python3.9 -m pip install --upgrade pip



#***************************************
#***************************************
# Docker Install
#***************************************
#***************************************

sudo yum update
sudo yum install -y yum-utils

# -#### Docker Repo
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

#-#### Docker Install
sudo yum install docker-ce docker-ce-cli containerd.io -y

#-#### Docker compose install (no ssl certification with k param)
sudo curl -k -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
docker-compose -v


# Version
docker -v

sudo systemctl enable docker
sudo systemctl start docker
sudo systemctl status docker


# -#### run docker-compose
docker-compose up -d
docker-compose -f <finlename.yml> up -d


#***************************************
#***************************************
# Node/NPM Install
#***************************************
#***************************************
$ sudo yum -y update
# Node.js 16.x Version
$ curl -sL https://rpm.nodesource.com/setup_16.x | sudo bash -

$ yum install -y nodejs

or

$ wget https://nodejs.org/download/release/v15.14.0/node-v15.14.0.tar.gz
$ sudo yum install gcc gcc-c++

$ make
$ sudo make install

$ node -v
# v16.18.1

$ npm -v
# 8.19.2
```


#### Python V3.9 Install
```bash
sudo yum install gcc openssl-devel bzip2-devel libffi-devel zlib-devel git 
wget https://www.python.org/ftp/python/3.9.0/Python-3.9.0.tgz 
tar –zxvf Python-3.9.0.tgz or tar -xvf Python-3.9.0.tgz 
cd Python-3.9.0 
./configure --libdir=/usr/lib64 
sudo make 
Sudo make altinstall 

# python3 -m venv .venv --without-pip
sudo yum install python3-pip

sudo ln -s /usr/lib64/python3.9/lib-dynload/ /usr/local/lib/python3.9/lib-dynload

python3 -m venv .venv
source .venv/bin/activate

# pip install -r ./requirement.txt
pip install prometheus-client
pip install requests

# when error occur like this
# ImportError: urllib3 v2 only supports OpenSSL 1.1.1+, currently the 'ssl' module is compiled with 'OpenSSL 1.0.2k-fips  26 Jan 2017'. See: https://github.com/urllib3/urllib3/issues/2168
pip install urllib3==1.26.18 
pip install pytz
```


#### Create Virtual Environment with Poetry/PIP -r
```bash
#!/bin/bash
set -e

export PYTHONDONTWRITEBYTECODE=1

SCRIPTDIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

VENV=".venv"


function activate_virtual_env() {
    # Create virtualenv
    python3.9 -m venv $SCRIPTDIR/$VENV

     # Python 3.11.7 with Window
    if [ -d "$VENV/bin" ]; then
        source $SCRIPTDIR/$VENV/bin/activate
    else
        source $SCRIPTDIR/$VENV/Scripts/activate
    fi

    echo "Created virtual enviroment >>" + $SCRIPTDIR/$VENV/bin/activate

    #echo "Create Poetry Environment"
    # Python 3.11.7 with Window
    #pip install poetry
    #poetry install
    #echo "Finish Poetry Environment Completely.."

    echo "Install requirements.txt"
    pip install --upgrade pip
    pip install -r $SCRIPTDIR/dev-requirement.txt
    echo "Install Completely.."
}

if [ -d $SCRIPTDIR/$VENV ]; then
  echo "VirtualEnv exists."
  rm -rf $SCRIPTDIR/$VENV
fi

activate_virtual_env
```


#### CentOS Yum Error
```bash
cd /etc/yum.repos.d/
ls
rm -rf epel.repo 
rm -rf epel-testing.repo 
sudo yum clean all
sudo yum install -y code
```

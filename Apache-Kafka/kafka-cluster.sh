
#!/bin/sh

JAVA_HOME=/usr/bin/java
JMX_PATH=/home/devuser/monitoring/jmx-exporter
KAFKA_PATH=/home/devuser/kafka_cluster/kafka_2.13-3.7.0
PATH=$PATH:$KAFKA_PATH/bin
PATH=$PATH:$JAVA_HOME/bin
#KAFKA_OPTS=" -javaagent:$JMX_PATH/jmx_prometheus_javaagent-0.15.0.jar=7075:$JMX_PATH/kafka_config.yml"

export  KAFKA_HEAP_OPTS="-Xmx4G -Xms4G"

# See how we were called.
case "$1" in
  start)
        # Start daemon.
        echo "Starting Zookeeper";
        nohup $KAFKA_PATH/bin/zookeeper-server-start.sh /$KAFKA_PATH/config/zookeeper.properties &> /dev/null &
        echo "Starting Kafka";
 	      #export KAFKA_OPTS
        nohup $KAFKA_PATH/bin/kafka-server-start.sh /$KAFKA_PATH/config/server.properties  &> /dev/null &
        ;;
  stop)
        # Stop daemons.
        echo "Shutting down Zookeeper";
        pid=`ps ax | grep -i 'org.apache.zookeeper.server' | grep -v grep | awk '{print $1}'`
        if [ -n "$pid" ]
          then
          kill -9 $pid
        else
          echo "Zookeeper was not Running"
        fi
        echo "Shutting down Kafka";
        pid=`ps ax | grep -i 'kafka.Kafka' | grep -v grep | awk '{print $1}'`
        if [ -n "$pid" ]
          then
          kill -9 $pid
        else
          echo "Kafka was not Running"
        fi
        sh /home/devuser/utils/diag.sh stop
        ;;
  restart)
        $0 stop
        sleep 2
        $0 start
        ;;
  status)
        pid=`ps ax | grep -i 'org.apache.zookeeper.server' | grep -v grep | awk '{print $1}'`
        if [ -n "$pid" ]
          then
          echo "Zookeeper is Running as PID: $pid"
        else
          echo "Zookeeper is not Running"
        fi
        pid=`ps ax | grep -i 'kafka.Kafka' | grep -v grep | awk '{print $1}'`
        if [ -n "$pid" ]
          then
          echo "Kafka is Running as PID: $pid"
        else
          echo "Kafka is not Running"
        fi
	      #pid=`ps ax | grep -i 'jmx-exporter' | grep -v grep | awk '{print $1}'`
        #if [ -n "$pid" ]
        #  then
        #  echo "Jmx-Exporter is Running as PID: $pid"
        #else
        #  echo "Jmx-Exporter is not Running"
        #fi

        ;;
  *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
esac

exit 0

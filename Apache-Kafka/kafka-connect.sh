#!/bin/sh
KAFKA_PATH=/home/devuser/kafka_cluster/kafka_2.13-3.7.0
KAFKA_CONNECT_LIB_PATH=/home/devuser/kafka_cluster/confluent_lib/confluentinc-kafka-connect-jdbc-10.7.6
PATH=$PATH:$KAFKA_PATH/bin

# See how we were called.
case "$1" in
  start)
        # Start daemon.
        export CLASSPATH=:$KAFKA_PATH/libs/*:$KAFKA_CONNECT_LIB_PATH/lib/kafka-connect-jdbc-10.7.6.jar:$KAFKA_CONNECT_LIB_PATH/lib/postgresql-42.4.4.jar:$KAFKA_CONNECT_LIB_PATH/lib/kafka-connect-elasticsearch-4.0.0.jar:$CLASSPATH
        echo "Starting Connect(Distributed)";
        nohup $KAFKA_PATH/bin/connect-distributed.sh /$KAFKA_PATH/config/connect-distributed.properties &> /dev/null &
        ;;
  stop)
        # Stop daemons.
        echo "Shutting down Connect(Distributed)";
        pid=`ps ax | grep -i 'distributed' | grep -v grep | awk '{print $1}'`
        if [ -n "$pid" ]
          then
          kill -9 $pid
        else
          echo "Connect was not Running"
        fi
        ;;
  restart)
        $0 stop
        sleep 2
        $0 start
        ;;
  status)
        pid=`ps ax | grep -i 'distributed' | grep -v grep | awk '{print $1}'`
        if [ -n "$pid" ]
          then
          echo "Connect Running as PID: $pid"
        else
          echo "Connect is not Running"
        fi
        ;;
  *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
esac

exit 0

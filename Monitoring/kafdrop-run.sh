#!/bin/sh
KAFDROP_TOOL_EXPORT_PATH=/home/biadmin/monitoring/
JAVA_HOME=/home/biadmin/monitoring/jdk-22.0.1/
SERVICE_NAME=kafdrop-service
KAFKA_HOST=localhost:9092,test:9092

# See how we were called.
case "$1" in
  start)
        # Start daemon.
        echo "Starting $SERVICE_NAME";
        nohup  $JAVA_HOME/bin/java -jar $KAFDROP_TOOL_EXPORT_PATH/kafdrop-4.0.1.jar --kafka.brokerconnect=$KAFKA_HOST &> /dev/null &
        ;;
  stop)
        # Stop daemons.
        echo "Shutting down $SERVICE_NAME";
        pid=`ps ax | grep -i 'kafdrop-4.0.1.jar' | grep -v grep | awk '{print $1}'`
        if [ -n "$pid" ]
          then
          kill -9 $pid
         else
          echo "$SERVICE_NAME[$KAFKA_HOST] was not Running"
        fi
        ;;
  restart)
        $0 stop
        sleep 2
        $0 start
        ;;
  status)
        pid=`ps ax | grep -i 'kafdrop-4.0.1.jar' | grep -v grep | awk '{print $1}'`
        if [ -n "$pid" ]
          then
          echo "$SERVICE_NAME[$KAFKA_HOST] is Running as PID: $pid"
        else
          echo "$SERVICE_NAME[$KAFKA_HOST] is not Running"
        fi
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
esac


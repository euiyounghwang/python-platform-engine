from kafka import KafkaConsumer
from threading import Thread
import time
import logging
import sys
import queue
import argparse


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


Q = queue.Queue()  # limit concurrent threads to 2

# poetry add kafka-python
def work(topic, kafka_broker):
    # brokers = ['localhost:29092', 'localhost:39092']
    brokers = kafka_broker.split(",")
    # topic = 'test-topic'
    print('--', topic, brokers)

    # https://taptorestart.tistory.com/entry/Q-kafka%EC%97%90%EC%84%9C-groupid%EB%A5%BC-%EC%84%A4%EC%A0%95%ED%95%98%EB%A9%B4-%EC%96%B4%EB%96%BB%EA%B2%8C-%EB%90%A0%EA%B9%8C
    # https://firststep-de.tistory.com/38
    
    # consumer = KafkaConsumer(topic, group_id="Python_Kafka_Consumer_App_Job", bootstrap_servers=brokers)
    #consumer = KafkaConsumer(topic, bootstrap_servers=brokers, auto_offset_reset='earliest', enable_auto_commit=True, auto_commit_interval_ms=1000, group_id='Python_Kafka_Consumer_App_Job')
    #consumer = KafkaConsumer(topic, bootstrap_servers=brokers, auto_offset_reset='earliest', enable_auto_commit=True, auto_commit_interval_ms=1000)

    consumer = KafkaConsumer(topic, bootstrap_servers=brokers)

    for message in consumer:
        # logging.info(f'{message, message.value, message.value.decode("utf-8")}')
        logging.info(f'{message.value.decode("utf-8")}')
        Q.put(message.value.decode("utf-8"))
        logging.info("-- consumer checking..--")
    logging.info("-- job finished..--")
    
    
def thread_background(topic, brokers):
    while True:
        try:
            # print('create --', type(read_config_yaml()))
            print('--thread_background--')
            work(topic, brokers)
        except Exception as e:
            pass
        # time.sleep(1)  # TODO poll other things


def queue_background():
    while True:
        try:
            # print('create --', type(read_config_yaml()))
            consumer_json = Q.get()
            print(f"\nQ receiving -- {consumer_json}, type : {type(consumer_json)}")
        except Exception as e:
            print(e)
            pass
        # time.sleep(1)  # TODO poll other things

        
if __name__ == "__main__":

    ''' 
    python ./cluster-consumer.py --topic users_tb_topic --brokers localhost:9092
    ./cluster-consumer-job.sh
    '''
    parser = argparse.ArgumentParser(description="Running Kafka-Consumer using this script")
    parser.add_argument('-e', '--topic', dest='topic', default="test", help='the name of topic')
    parser.add_argument('-i', '--brokers', dest='brokers', default="localhost:9092,localhost:9093", help='kafka brokers')
    args = parser.parse_args()
    
    if args.topic:
        topic = args.topic
    
    if args.brokers:
        brokers = args.brokers

    try:
        T = []

        th1 = Thread(target=queue_background)
        th1.daemon = True
        th1.start()
        T.append(th1)
        
        #for topic in ['users_tb_topic']:
        for topic in [topic]:
            # Create thread as background
            th2 = Thread(target=thread_background, args=(topic, brokers))
            th2.daemon = True
            th2.start()
            T.append(th2)

        [t.join() for t in T] # wait for all threads to terminate

    except (KeyboardInterrupt, SystemExit):
        print('Interrupted')
        sys.exit(0) 
from kafka import KafkaConsumer
from threading import Thread
import time
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


# poetry add kafka-python
def consumer_kafka(topic):
    brokers = ['localhost:29092', 'localhost:39092']
    # topic = 'test-topic'
    print('--', topic)
    consumer = KafkaConsumer(topic, group_id="Python_Kafka_Consumer_App_Job", bootstrap_servers=brokers)

    for message in consumer:
        logging.info(f'{message, message.value, message.value.decode("utf-8")}')
    logging.info("-- job finished..--")
    
    
def thread_background(topic):
    
    while True:
        try:
            # print('create --', type(read_config_yaml()))
            print('--thread_background--')
            consumer_kafka(topic)
        except Exception as e:
            # listen_kill_server()
            print(e)
            pass
        time.sleep(5)  # TODO poll other things
        
        
        
if __name__ == "__main__":
    for topic in ['test-topic','test1-topic']:
        # Create thread as background
        Thread(target=thread_background, args=(topic,)).start()
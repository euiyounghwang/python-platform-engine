from kafka import KafkaConsumer
from threading import Thread
import time


# poetry add kafka-python
def consumer_kafka(topic):
    brokers = ['localhost:29092', 'localhost:39092']
    # topic = 'test-topic'
    print('--', topic)
    consumer = KafkaConsumer(topic, group_id="Python_Kafka_Consumer_Job", bootstrap_servers=brokers)

    for message in consumer:
        print(message, message.value, message.value.decode("utf-8"))
    
    
def thread_background(topic):
    while True:
        try:
            # print('create --', type(read_config_yaml()))
            print('--thread_background--')
            consumer_kafka(topic)
        except Exception as e:
            # listen_kill_server()
            pass
        time.sleep(5)  # TODO poll other things
        
        
        
if __name__ == "__main__":
    for topic in ['test-topic', 'test1-topic']:
        # Create thread as background
        Thread(target=thread_background, args=(topic,)).start()
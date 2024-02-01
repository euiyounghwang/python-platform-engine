from kafka import KafkaProducer
from datetime import datetime
import json
# from kafka_schema_registry import prepare_producer
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# poetry add kafka-schema-registry
SAMPLE_SCHEMA = {
    "type": "record",
    "name": "TestType",
    "fields" : [
        {"name": "author", "type": ["null", "string"]},
        {"name": "content", "type": ["null", "string"]},
        {"name": "created_at", "type":["null", "string"]},
    ]
}


# poetry add kafka-python
def produce_kafka():
    brokers = ['localhost:29092', 'localhost:39092']
    topics = ['test-topic', 'test1-topic']

    producer = KafkaProducer(bootstrap_servers=brokers,
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    for _ in range(3):
        for each_topic in topics:
            '''
            producer.send(each_topic, b'Hello, World!')
            producer = prepare_producer(
                brokers,
                f'http://localhost:28081',
                each_topic,
                1,
                1,
                value_schema=SAMPLE_SCHEMA,
            )
            '''
            producer.send(each_topic, {'author': 'choyiny', 'content': 'Kafka is cool!', 'created_at': datetime.now().isoformat()})
            producer.flush()
    
    logging.info('--#$Send..#$--')
    
    
if __name__ == "__main__":
    produce_kafka()
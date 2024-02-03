import json
# from injector import RABBIT_HOST
import pika, socket
import uuid
import argparse
from dotenv import load_dotenv
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def start_rmq_handler(q_name, id, password, json_msg, hosts="localhost"):

    try:
        credentials = pika.PlainCredentials(id, password)
        hostname = socket.gethostname()
        parameters = pika.ConnectionParameters(host=hosts,
        port=5672, virtual_host='/', credentials=credentials)

        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()

        msg_props = pika.BasicProperties()
        msg_props.content_type = "application/json"
       
        msg = json.dumps(json_msg)
        # channel.queue_declare(queue=q_name, durable=True)
        channel.queue_declare(queue=q_name)
        channel.basic_publish(exchange='', routing_key=q_name, body=msg , properties=msg_props)

        logging.info("#$@Q$@ -> [{}] Sent..'".format(msg))

    finally:
        connection.close()


if __name__ == '__main__':
    # load_dotenv()
    parser = argparse.ArgumentParser(description="create message into rabbitmq")
    parser.add_argument('-e', '--es', dest='es', default="localhost", required=False, help='host target')
    args = parser.parse_args()

    if args.es:
        host = args.es

    # logging.info('host - ', host)
    json_msg = {
            "entity_id" : "kraken_document-289857"
    }
    login = ['guest', 'guest']
    start_rmq_handler('fastapi_publish_queue', login[0], login[1], json_msg, hosts=host)

import json
from datetime import datetime

import pika

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='hw8 exchange', exchange_type='direct')
channel.queue_declare(queue='hw8_queue', durable=True)
channel.queue_bind(exchange='hw8 exchange', queue='hw8_queue')


def create_task(nums: int):
    for i in range(nums):
        message = {
            'id': i,
            'payload': f'Date: {datetime.now().isoformat()}'
        }

        channel.basic_publish(exchange='hw8 exchange', routing_key='hw8_queue', body=json.dumps(message).encode())

    connection.close()


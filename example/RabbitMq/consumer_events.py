import json

import pika
import sys


def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    q = channel.queue_declare(queue='', exclusive=True)
    name_q = q.method.queue
    channel.queue_bind(exchange='hw8 events message', queue=name_q)

    def callback(ch, method, properties, body):
        message = json.loads(body.decode())
        print(f" [x] Received {message}")

    channel.basic_consume(queue=name_q, on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)

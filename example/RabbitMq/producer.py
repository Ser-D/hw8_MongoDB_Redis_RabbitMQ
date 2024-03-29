import pika

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='hello_world')

message = 'Hello world!!'
channel.basic_publish(exchange='', routing_key='hello_world', body=message.encode())
print(f" [x] Sent {message}")
connection.close()

# if __name__ == '__main__':
#     main()

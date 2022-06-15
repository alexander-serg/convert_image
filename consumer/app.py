import pika
from grayscale import convert


try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
except pika.exceptions.AMQPConnectionError as exc:
    print("Failed to connect to RabbitMQ service.")

channel = connection.channel()
channel.queue_declare(queue='task_queue', durable=True)

print(' Waiting for messages...')


def callback(ch, method, properties, body):
    convert(body.decode())
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)
channel.start_consuming()


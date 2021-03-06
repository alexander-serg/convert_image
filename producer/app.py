import json

import pika
from flask import Flask, request, Response
from marshmallow import Schema, fields

app = Flask(__name__)


class ImagesSchema(Schema):
    file = fields.Str()
    file_name = fields.Str()
    
    
schema = ImagesSchema()


@app.route('/', methods=['POST'])
def image_json():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        request_data = request.get_json()
        result = schema.dumps(request_data)
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host="rabbitmq")
            )
        except pika.exceptions.AMQPConnectionError as exc:
            print("Failed to connect to RabbitMQ service.")

        channel = connection.channel()
        channel.queue_declare(queue='task_queue', durable=True)
        channel.basic_publish(
            exchange='',
            routing_key='task_queue',
            body=result,
            properties=pika.BasicProperties(
                delivery_mode=2,
            ))

        connection.close()
        return Response(status=202)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

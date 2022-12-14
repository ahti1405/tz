import json

import pika


def send(msg):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='task_queue', durable=True)

    message = msg
    channel.basic_publish(exchange='',
                        routing_key='task_queue',
                        body=json.dumps(message),
                        properties=pika.BasicProperties(
                            delivery_mode = pika.spec.PERSISTENT_DELIVERY_MODE
                        ))
    print(" [x] Sent %r" % message)

    connection.close()


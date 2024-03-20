import json

import pika

from app.settings import settings


def send_notification(task):
    connection = pika.BlockingConnection(pika.URLParameters(settings.amqp_url))
    channel = connection.channel()

    channel.exchange_declare(exchange='kabachkov_notification_exchange', exchange_type='direct', durable=True)
    queue = channel.queue_declare(queue='', exclusive=True, durable=True)
    channel.queue_bind(exchange="kabachkov_notification_exchange", queue=queue.method.queue)
    message_body = json.dumps(task)
    channel.basic_publish(exchange='kabachkov_notification_exchange', routing_key=task["user_id"],
                          body=message_body.encode('utf-8'))

    connection.close()

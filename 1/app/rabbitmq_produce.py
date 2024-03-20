import json

import pika

from app.models.delivery import DeliveryStatuses
from app.settings import settings


def send_notification(delivery):
    connection = pika.BlockingConnection(pika.URLParameters(settings.amqp_url))
    channel = connection.channel()

    if delivery.status == DeliveryStatuses.ACTIVATE:
        message = f"New delivery created: {delivery.title}"
    else:
        message = f"Delivery done: {delivery.title}"

    new_notification = {
        "message": message,
        "user_id": str(delivery.user_id),
        "status": str(delivery.status)
    }

    channel.exchange_declare(exchange='kabachkov_notification_created_exchange', exchange_type='direct', durable=True)
    message_body = json.dumps(new_notification)
    channel.basic_publish(exchange='kabachkov_notification_created_exchange', routing_key="notification_service",
                          body=message_body.encode('utf-8'))

    connection.close()

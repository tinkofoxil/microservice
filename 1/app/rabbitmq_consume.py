import json
import traceback
from asyncio import AbstractEventLoop
from uuid import UUID

from aio_pika import connect_robust, IncomingMessage
from aio_pika.abc import AbstractRobustConnection

from app.services.task_service import DeliveryService
from app.settings import settings


async def process_created_task(msg: IncomingMessage):
    try:
        data = json.loads(msg.body.decode())
        DeliveryService().create_task(data['title'], data['description'], UUID(data['user_id']))
        await msg.ack()
    except:
        traceback.print_exc()
        await msg.ack()


async def consume(loop: AbstractEventLoop) -> AbstractRobustConnection:
    connection = await connect_robust(settings.amqp_url, loop=loop)
    channel = await connection.channel()

    task_created_queue = await channel.declare_queue('orlov_task_created_queue', durable=True)

    await task_created_queue.consume(process_created_task)
    print('Started RabbitMQ consuming...')

    return connection

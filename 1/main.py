import asyncio
from fastapi import FastAPI
from app import rabbitmq_consume
from app.endpoints.delivery_router import delivery_router

app = FastAPI(title='Delivery service')


@app.on_event('startup')
async def startup():
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(rabbitmq_consume.consume(loop))


app.include_router(delivery_router, prefix='/api')

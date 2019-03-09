import json

import asyncio
from aioredis import Channel
from websockets import WebSocketCommonProtocol

from app.queue.pubsub import ConsumerHandler, ProducerHandler
from app.queue.redis import queue_conn_sub, queue_conn_pub

CONNECTED = set()

async def web_socket_chat(_, websocket: WebSocketCommonProtocol):
    CONNECTED.add(websocket)
    channel_name = await websocket.recv()
    channel_data = json.loads(channel_name)
    channel = Channel(channel_data['room_id'], is_pattern=False)
    consumer_handler = await ConsumerHandler.initialize(channel,
                                                        queue_conn_pub)
    producer_handler = await ProducerHandler.initialize(channel,
                                                        queue_conn_sub)

    consumer_task = asyncio.ensure_future(consumer_handler.handle(websocket))
    producer_task = asyncio.ensure_future(
        producer_handler.broadcast(websocket))
    done, pending = await asyncio.wait(
        [consumer_task, producer_task],
        return_when=asyncio.FIRST_COMPLETED,
    )

    for task in pending:
        task.cancel()

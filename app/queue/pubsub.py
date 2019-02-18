import json
from abc import ABC

import websockets
from aioredis import ConnectionsPool, Channel
from sanic.log import logger
from websockets import WebSocketCommonProtocol


class Handler(ABC):
    _pub: ConnectionsPool = None
    _channel: Channel = None

    @classmethod
    async def initialize(cls, channel, queue_conn):
        handler = cls()
        redis = await queue_conn.get_redis()
        handler._pub = redis
        handler._channel = channel
        return handler


class ProducerHandler(Handler):

    async def broadcast(self, websocket: WebSocketCommonProtocol):
        with await self._pub as conn:
            await conn.execute_pubsub('subscribe', self._channel)
            try:
                while True:
                    message = await self._channel.get(encoding="utf-8")
                    await websocket.send(message)
            except websockets.ConnectionClosed as e:
                print(f"<ProducerHandler:broadcast>[error] {e}")


class ConsumerHandler(Handler):

    async def handle(self, websocket: websockets.WebSocketCommonProtocol):
        try:
            while True:
                msg = await websocket.recv()
                loaded_msg = json.loads(msg)
                try:
                    await self._chat(loaded_msg)
                except AttributeError:
                    logger.warn(f"Invalid action requested full msg: {msg}")

        except websockets.ConnectionClosed as e:
            print(f"<ConsumerHandler:handle>[error] {e}")

    async def _chat(self, msg):
        dumped_msg = json.dumps(msg)
        with await self._pub as conn:
            await conn.execute("publish", self._channel.name, dumped_msg)
import aioredis

import config


class RedisConnection:
    def __init__(self):
        self._pool = None
        self._connections = {}

    def qsize(self):
        return self._pool.size

    def empty(self):
        return self.qsize() == 0

    async def get_redis(self):
        if not self._pool:
            await self.connect()

        return self._pool

    async def connect(self):
        self._pool = await aioredis.create_pool(
            (config.REDIS_HOSTNAME, config.REDIS_PORT),
            minsize=5,
            maxsize=10
        )

    async def close(self):
        self._pool.close()
        await self._pool.wait_closed()


queue_conn_pub = RedisConnection()
queue_conn_sub = RedisConnection()

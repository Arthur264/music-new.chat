PROJECT_ID = 'music-new.chat'

SANIC_SETTINGS = {
    'project_id': PROJECT_ID,
    'WEBSOCKET_MAX_SIZE': 2 ** 20,
    'WEBSOCKET_MAX_QUEUE': 32,
    'WEBSOCKET_READ_LIMIT': 2 ** 16,
    'WEBSOCKET_WRITE_LIMIT': 2 ** 16,
    'KEEP_ALIVE': False,
}

DATE_TIME_FORMAT = None
REDIS_PORT = 6379
REDIS_HOSTNAME = 'localhost'

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

DEBUG_LEVEL = 'ERROR'

CLUSTER_KEY_SPACE = 'music_new_messages'
CLUSTER_NAME = 'music_new'
CLUSTER_HOST = '127.0.0.1'
LOGGER_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"

API_URL = 'http://music-artyr264.c9users.io:8081/api/v1/'

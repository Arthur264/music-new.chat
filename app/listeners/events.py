import logging

import aiohttp
from aiocassandra import aiosession
from cassandra.cluster import Cluster
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import create_keyspace_simple

from app.listeners.db import setup_db
from config import CLUSTER_HOST, CLUSTER_KEY_SPACE, CLUSTER_NAME, \
    LOGGER_FORMAT, DEBUG_LEVEL


def before_server_start(app, loop):
    app.aiohttp_session = aiohttp.ClientSession(loop=loop)

    cluster = Cluster([CLUSTER_HOST])
    session = cluster.connect()
    session.execute(
        """
        CREATE KEYSPACE IF NOT EXISTS %s 
        WITH REPLICATION = { 
            'class' : 'SimpleStrategy', 
            'replication_factor' : 1,
        };
        """ % CLUSTER_KEY_SPACE)
    session = cluster.connect(keyspace=CLUSTER_KEY_SPACE)
    aiosession(session)
    # session.execute(f"DROP KEYSPACE {CLUSTER_KEY_SPACE}")

    connection.register_connection(CLUSTER_NAME, session=session)
    create_keyspace_simple(CLUSTER_KEY_SPACE, 1, connections=[CLUSTER_NAME])

    connection.setup([CLUSTER_HOST], CLUSTER_KEY_SPACE)

    setup_db()
    app.db_session = session

    logger = logging.getLogger()
    logger.setLevel(DEBUG_LEVEL)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(LOGGER_FORMAT))
    logger.addHandler(handler)
    app.log = logger


def after_server_stop(app, loop):
    app.db_sesion.shutdown()
    loop.run_until_complete(app.session.close())
    loop.close()

import aiomysql
from config import *
import asyncio


loop = asyncio.get_event_loop()

async def connect():
    return await aiomysql.create_pool(
        host=HOST_DB,
        port=PORT_DB,
        user=USER_DB,
        password=PASS_DB,
        db=NAME_DB,
        autocommit=True,
        pool_recycle=100,
        loop=loop
    )

db_connect = loop.run_until_complete(connect())

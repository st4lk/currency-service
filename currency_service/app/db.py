import logging
import asyncio

import asyncpg
from gino.ext.aiohttp import Gino as BaseGino

from settings import DB_PARAMS, DB_CONNECT_RETRY

logger = logging.getLogger(__name__)


class Gino(BaseGino):

    async def set_bind(self, *args, **kwargs):
        return await _init_db(super().set_bind, *args, **kwargs)


db = Gino()


async def init_db():
    params = dict(DB_PARAMS)
    dsn = params.pop('dsn')
    min_size = params.pop('pool_min_size')
    max_size = params.pop('pool_max_size')
    db_kwargs = params.pop('kwargs')
    return await _init_db(
        db.set_bind,
        dsn,
        min_size=min_size,
        max_size=max_size,
        **params,
        **db_kwargs
    )


async def close_db():
    logger.debug('Trying to close postgres connection, waiting...')
    await asyncio.wait_for(db.pop_bind().close(), timeout=3)
    logger.debug('Postgres connection closed successfully')


async def _init_db(set_bind, dsn, *args, **kwargs):
    result = None
    for retry_cnt in range(DB_CONNECT_RETRY):
        try:
            result = await set_bind(dsn, *args, **kwargs)
        except (
            ConnectionError,
            asyncpg.OperatorInterventionError,
            asyncpg.PostgresConnectionError,
        ):
            if retry_cnt >= DB_CONNECT_RETRY - 1:
                raise
            else:
                logger.debug('Retry postgres connection #%s', retry_cnt)
                await asyncio.sleep(3)
    return result

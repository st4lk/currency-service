import logging

import argparse
import asyncio

from db import init_db, close_db
from models import db  # Need to use models module so models will be imported

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(
    description='Very basic migration script. Just runs SQL statements from hardcoded list.',
)


async def run_migrations() -> None:
    logger.info('Creating GINO tables')
    await init_db()
    try:
        await db.gino.create_all()
    finally:
        await close_db()
    logger.info('Migrations were applied successfully.')


if __name__ == '__main__':
    args = parser.parse_args()
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(run_migrations())

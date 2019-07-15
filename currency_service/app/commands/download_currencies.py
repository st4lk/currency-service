import argparse
import asyncio
import logging
from datetime import datetime
from typing import List, Optional

import aiohttp
import aiojobs
from async_timeout import timeout as async_timeout

from db import init_db, close_db
from models import Currency, Rate

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description='Download currencies and save to database.')
parser.add_argument(
    '-c', '--currencies', nargs='+', default=['BTC', 'ETH', 'XRP', 'LTC', 'AIO'],
    help='List of ids',
)

BASE_URL = (
    'https://api-pub.bitfinex.com/v2/candles/trade:{period}:t{currency_code}USD/hist'
    '?limit={limit}'
)
MAX_CONCURRENT_REQUEST = 5
MAX_TOTAL_TIMEOUT = 60 * 10  # in seconds

PERIOD = '1D'
LIMIT = 10


async def fetch_url(url: str) -> Optional[List]:
    # TODO: possible performance improvements:
    # install cchardet
    # install aiodns

    response_data = None
    timeout = aiohttp.ClientTimeout(connect=10, total=30)  # in seconds
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(url) as response:
            response_data = await response.json()
    response.raise_for_status()
    return response_data


async def fetch_currency(currency_code: str, period: str, limit: int) -> None:
    url = BASE_URL.format(period=period, currency_code=currency_code, limit=limit)
    logger.info('Fetching URL %s', url)
    results = await fetch_url(url)
    currency = await Currency.get_or_create(name=currency_code)
    for result in results:
        mts = result[0]
        close = str(result[2])
        volume = str(result[5])
        mts_dt = datetime.utcfromtimestamp(mts / 1000.0)
        await Rate.update_or_create(
            currency_id=currency.id, date=mts_dt, rate=close, volume=volume
        )
        logger.info('Updated %s; %s; %s; %s', currency_code, mts_dt, close, volume)


async def fetch_currencies(currency_codes: List[str], period: str, limit: int) -> None:
    fetch_jobs = []
    scheduler = await aiojobs.create_scheduler(limit=MAX_CONCURRENT_REQUEST, close_timeout=1.0)
    for currency_code in currency_codes:
        coro = fetch_currency(currency_code, period, limit)
        job = await scheduler.spawn(coro)
        fetch_jobs.append(job)
    try:
        with async_timeout(MAX_TOTAL_TIMEOUT):
            await asyncio.gather(*(job.wait() for job in fetch_jobs))
    except asyncio.TimeoutError:
        logger.error(
            'The entire task took more than %s seconds to finish, cancelling', MAX_TOTAL_TIMEOUT,
        )
    await scheduler.close()


async def run_currency_download(currencies) -> None:
    logger.info('Running download')
    await init_db()
    try:
        await fetch_currencies(currencies, PERIOD, LIMIT)
    finally:
        await close_db()
    logger.info('Data was updated successfully.')


if __name__ == '__main__':
    args = parser.parse_args()
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(run_currency_download(args.currencies))

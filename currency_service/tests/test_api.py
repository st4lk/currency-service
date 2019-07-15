from datetime import datetime, timedelta

from aiohttp import BasicAuth

from models import Currency, Rate
from settings import BASIC_AUTH_LOGIN

TEST_AUTH = BasicAuth(BASIC_AUTH_LOGIN, 'password')


async def test_currencies(web_client):
    url = web_client.app.router['currencies_list'].url_for()

    await Currency.create(name='BTC')
    await Currency.create(name='ETH')
    resp = await web_client.get(url, auth=TEST_AUTH)
    assert resp.status == 200
    resp_data = await resp.json()
    assert len(resp_data) == 2


async def test_currencies_pagination(web_client):

    await Currency.create(name='C1')
    await Currency.create(name='C2')

    url = web_client.app.router['currencies_list'].url_for().with_query({
        'page': '2',
        'page_size': '1',
    })
    resp = await web_client.get(url, auth=TEST_AUTH)
    assert resp.status == 200
    resp_data = await resp.json()
    assert len(resp_data) == 1
    assert resp_data[0]['name'] == 'C2'


async def test_rate(web_client):
    currency = await Currency.create(name='BTC')
    now = datetime.utcnow()
    for i in range(15):
        dt = now - timedelta(days=i)
        await Rate.create(rate=100 - i, volume=i, date=dt, currency_id=currency.id)

    url = web_client.app.router['rate_detail'].url_for(currency_id=str(currency.id))
    resp = await web_client.get(url, auth=TEST_AUTH)
    assert resp.status == 200
    resp_data = await resp.json()
    assert resp_data['last_rate'] == 100
    assert resp_data['avg_volume'] == 4.5

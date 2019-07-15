import logging

from aiohttp import web
import aiohttp_jinja2
import simplejson as json

from middlewares import auth
from models import Currency, Rate
from parsers import DEFAULT_PAGE_SIZE, PaginationSchema

logger = logging.getLogger(__name__)


@aiohttp_jinja2.template('home.html')
async def handle_home(request):
    return {'default_page_size': DEFAULT_PAGE_SIZE}


@auth.required
async def handle_currency_list(request):
    params = PaginationSchema().load(request.query).data
    offset = params['page_size'] * (params['page'] - 1)
    query = Currency.query.order_by(Currency.id).offset(offset).limit(params['page_size'])
    currencies = await query.gino.all()
    currencies_data = [currency.to_dict() for currency in currencies]
    return web.json_response(currencies_data, dumps=json.dumps)


@auth.required
async def handle_rate_detail(request):
    currency_id = int(request.match_info['currency_id'])
    last_rate_instance = await Rate.get_last_rate(currency_id)
    if not last_rate_instance:
        raise web.HTTPNotFound()
    avg_volume = await Rate.get_avg_volume(currency_id, last_days=10)
    data = {'last_rate': last_rate_instance.rate, 'avg_volume': avg_volume}
    return web.json_response(data, dumps=json.dumps)

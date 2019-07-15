import logging

import aiohttp_jinja2
import jinja2
from aiohttp import web

from db import db
from handlers import (
    handle_home,
    handle_currency_list,
    handle_rate_detail,
)
from settings import APP_HOST, APP_PORT, DB_PARAMS, TEMPLATE_DIR
from middlewares import auth


logger = logging.getLogger(__name__)


async def log_ready(app):
    logger.info('App is ready and listening on %s:%s', APP_HOST, APP_PORT)


def setup_templates(app):
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(TEMPLATE_DIR))


def create_app() -> web.Application:
    app = web.Application(middlewares=[db, auth])
    app['config'] = {'gino': DB_PARAMS}
    db.init_app(app)
    setup_templates(app)
    app.on_startup.append(log_ready)
    app.add_routes([
        web.get('/', handle_home, name='home'),
        web.get('/api/currencies', handle_currency_list, name='currencies_list'),
        web.get(r'/api/rate/{currency_id:\d+}', handle_rate_detail, name='rate_detail'),
    ])
    return app


if __name__ == '__main__':
    app = create_app()
    web.run_app(app, host=APP_HOST, port=APP_PORT)

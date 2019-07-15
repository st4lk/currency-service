import pytest
from sqlalchemy.sql import text

from models import db
from server import create_app


@pytest.fixture
def web_client(loop, aiohttp_client):
    app = create_app()
    return loop.run_until_complete(aiohttp_client(app))


@pytest.fixture(scope='function', autouse=True)
async def trunc_tables(request, web_client, loop):

    async def afin():
        async with db.transaction() as tx:
            for table in db.sorted_tables:
                await tx.connection.scalar(text(f'TRUNCATE {table.name} CASCADE;'))

    def fin():
        loop.run_until_complete(afin())

    request.addfinalizer(fin)

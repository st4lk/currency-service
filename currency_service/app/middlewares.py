import hashlib

from aiohttp_basicauth import BasicAuthMiddleware

from settings import BASIC_AUTH_LOGIN, BASIC_AUTH_PWD_HASH


class BasicAuthMD5Middleware(BasicAuthMiddleware):

    async def check_credentials(self, username, password):
        return (
            username == BASIC_AUTH_LOGIN and
            hashlib.md5(bytes(password, encoding='utf-8')).hexdigest() == BASIC_AUTH_PWD_HASH
        )


auth = BasicAuthMD5Middleware(
    username=BASIC_AUTH_LOGIN,
    password=BASIC_AUTH_PWD_HASH,
    force=False,
)

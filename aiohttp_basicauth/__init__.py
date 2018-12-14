# -*- coding: utf-8 -*-
import functools
from aiohttp import BasicAuth, web, hdrs
from aiohttp.web import middleware

__version__ = '0.1.2'


@middleware
class BasicAuthMiddleware(object):
    def __init__(self, username=None, password=None, force=True, realm=''):
        self.username = username
        self.password = password
        self.force = force
        self.realm = realm

    # noinspection PyMethodMayBeStatic
    def parse_auth_header(self, request):
        auth_header = request.headers.get(hdrs.AUTHORIZATION)
        if not auth_header:
            return None
        try:
            auth = BasicAuth.decode(auth_header=auth_header)
        except ValueError:  # pragma: no cover
            auth = None
        return auth

    async def authenticate(self, request):
        auth = self.parse_auth_header(request)
        return (auth is not None
                and await self.check_credentials(auth.login, auth.password))

    async def check_credentials(self, username, password):
        if username is None:
            raise ValueError('username is None')  # pragma: no cover

        if password is None:
            raise ValueError('password is None')  # pragma: no cover

        return username == self.username and password == self.password

    def challenge(self):
        return web.Response(
            body=b'', status=401, reason='UNAUTHORIZED',
            headers={
                hdrs.WWW_AUTHENTICATE: 'Basic realm="%s"' % self.realm,
                hdrs.CONTENT_TYPE: 'text/html; charset=utf-8',
                hdrs.CONNECTION: 'keep-alive'
            }
        )

    async def check_auth(self, request, handler):
        if await self.authenticate(request):
            return await handler(request)
        else:
            return self.challenge()

    def required(self, handler):
        @functools.wraps(handler)
        async def wrapper(request):
            return await self.check_auth(request, handler)

        return wrapper

    async def __call__(self, request, handler):
        if not self.force:
            return await handler(request)
        else:
            return await self.check_auth(request, handler)

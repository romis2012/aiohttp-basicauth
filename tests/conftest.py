from aiohttp import web
import pytest
from aiohttp.pytest_plugin import *  # noqa

from aiohttp_basicauth import BasicAuthMiddleware

USERNAME = 'user'
PASSWORD = 'password'


@pytest.fixture
def auth_factory():
    def factory(force, realm=''):
        return BasicAuthMiddleware(
            username=USERNAME,
            password=PASSWORD,
            force=force,
            realm=realm,
        )

    return factory


@pytest.fixture
def app_factory(auth_factory, loop):
    def factory(auth_force, realm=''):
        auth = auth_factory(force=auth_force, realm=realm)

        async def public_view(request):
            return web.Response(text='Public view')

        @auth.required
        async def secret_view(request):
            return web.Response(text='Secret view')

        app = web.Application(middlewares=[auth], loop=loop)
        app.router.add_get('/', public_view)
        app.router.add_get('/secret', secret_view)
        return app

    return factory

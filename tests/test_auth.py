from aiohttp import hdrs, BasicAuth

from tests.conftest import USERNAME, PASSWORD


async def test_any_views_respond_401_when_auth_forced(aiohttp_client, app_factory):
    app = app_factory(auth_force=True)
    client = await aiohttp_client(app)
    resp = await client.get('/')

    assert resp.status == 401


async def test_public_views_respond_200_when_auth_not_forced(aiohttp_client, app_factory):
    app = app_factory(auth_force=False)
    client = await aiohttp_client(app)
    resp = await client.get('/')

    assert resp.status == 200


async def test_ignored_views_respond_200_when_auth_forced(aiohttp_client, app_factory):
    app = app_factory(auth_force=True)
    client = await aiohttp_client(app)
    resp = await client.get('/ignored')

    assert resp.status == 200


async def test_protected_views_respond_401_when_auth_not_forced(aiohttp_client, app_factory):
    app = app_factory(auth_force=False)
    client = await aiohttp_client(app)
    resp = await client.get('/secret')

    assert resp.status == 401


async def test_server_asks_for_auth(aiohttp_client, app_factory):
    app = app_factory(auth_force=True)
    client = await aiohttp_client(app)
    resp = await client.get('/')

    assert resp.status == 401
    assert resp.headers[hdrs.WWW_AUTHENTICATE] == 'Basic realm=""'


async def test_server_asks_for_auth_custom_realm(aiohttp_client, app_factory):
    realm = 'Protected Area'
    app = app_factory(auth_force=True, realm=realm)
    client = await aiohttp_client(app)
    resp = await client.get('/')

    assert resp.status == 401
    assert resp.headers[hdrs.WWW_AUTHENTICATE] == 'Basic realm="%s"' % realm


async def test_protected_views_respond_200_when_passing_auth_headers(aiohttp_client, app_factory):
    app = app_factory(auth_force=True)
    client = await aiohttp_client(app)
    resp = await client.get('/secret', auth=BasicAuth(USERNAME, PASSWORD))

    assert resp.status == 200


async def test_protected_views_respond_401_when_passing_invalid_credentials(
    aiohttp_client,
    app_factory,
):
    app = app_factory(auth_force=True)
    client = await aiohttp_client(app)
    resp = await client.get('/secret', auth=BasicAuth(USERNAME, PASSWORD + 'aaa'))

    assert resp.status == 401

## aiohttp-basicauth

[![CI](https://github.com/romis2012/aiohttp-basicauth/actions/workflows/ci.yml/badge.svg)](https://github.com/romis2012/aiohttp-basicauth/actions/workflows/ci.yml)
[![Coverage Status](https://codecov.io/gh/romis2012/aiohttp-basicauth/branch/master/graph/badge.svg)](https://codecov.io/gh/romis2012/aiohttp-basicauth)
[![PyPI version](https://badge.fury.io/py/aiohttp-basicauth.svg?_=a)](https://badge.fury.io/py/aiohttp-basicauth)

HTTP basic authentication middleware for aiohttp 3.0+. 
Inspired by [Flask-BasicAuth](https://github.com/jpvanhal/flask-basicauth).

## Requirements
- Python >= 3.7
- aiohttp >= 3.0

## Installation
```
pip install aiohttp_basicauth
```

## Simple usage

```python
from aiohttp import web
from aiohttp_basicauth import BasicAuthMiddleware


auth = BasicAuthMiddleware(username='user', password='password')
app = web.Application(middlewares=[auth])

web.run_app(app, host='127.0.0.1', port=80)
```

## Protect specific view(s)
```python
from aiohttp import web
from aiohttp_basicauth import BasicAuthMiddleware

auth = BasicAuthMiddleware(username='user', password='password', force=False)


async def public_view(request):
    return web.Response(text='Public view')


@auth.required
async def secret_view(request):
    return web.Response(text='Secret view')


app = web.Application(middlewares=[auth])

app.router.add_route('GET', '/public', public_view)
app.router.add_route('GET', '/secret', secret_view)

web.run_app(app, host='127.0.0.1', port=80)
```

## Advanced usage

You can override ```check_credentials``` method to implement more complex user verification logic:

```python
from aiohttp import web
from aiohttp_basicauth import BasicAuthMiddleware


class CustomBasicAuth(BasicAuthMiddleware):
    async def check_credentials(self, username, password, request):
        # here, for example, you can search user in the database by passed `username` and `password`, etc.
        return username == 'user' and password == 'password'


auth = CustomBasicAuth()
app = web.Application(middlewares=[auth])

web.run_app(app, host='127.0.0.1', port=80)
```

## aiohttp-basicauth

[![Build Status](https://travis-ci.org/romis2012/aiohttp-basicauth.svg?branch=master)](https://travis-ci.org/romis2012/aiohttp-basicauth)
[![Coverage Status](https://coveralls.io/repos/github/romis2012/aiohttp-basicauth/badge.svg?branch=master)](https://coveralls.io/github/romis2012/aiohttp-basicauth?branch=master)
[![PyPI version](https://badge.fury.io/py/aiohttp-basicauth.svg)](https://badge.fury.io/py/aiohttp-basicauth)

HTTP basic authentication middleware for aiohttp 3.0+. 
Inspired by [Flask-BasicAuth](https://github.com/jpvanhal/flask-basicauth).

## Requirements
- Python >= 3.5.3
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

You can override ```check_credentials``` method to implement specific user verification logic:

```python
from aiohttp import web
from aiohttp_basicauth import BasicAuthMiddleware


class CustomBasicAuth(BasicAuthMiddleware):
    async def check_credentials(self, username, password):
        return username == 'user' and password == 'password'


auth = CustomBasicAuth()
app = web.Application(middlewares=[auth])

web.run_app(app, host='127.0.0.1', port=80)
```

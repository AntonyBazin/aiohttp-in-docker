from aiohttp import web
from app.routes import setup_routes
from app.settings import config

app = web.Application()
app['config'] = config
setup_routes(app)

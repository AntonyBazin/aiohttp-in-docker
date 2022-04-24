from aiohttp import web
from app.routes import setup_routes
from app.settings import config
from app.db import pg_context

app = web.Application()
app['config'] = config
app.cleanup_ctx.append(pg_context)
setup_routes(app)

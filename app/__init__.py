from aiohttp import web
from app.routes import setup_routes

app = web.Application()
setup_routes(app)

from aiohttp import web
import asyncio

routes = web.RouteTableDef()


@routes.get('/')
async def hello(request):
    return web.Response(text='Hello, world')


app = web.Application()
app.add_routes(routes)
web.run_app(app)

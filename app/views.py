from aiohttp import web
import app.db


async def handler(request):
    async with request.app['db'].acquire() as conn:
        cursor = await conn.execute(app.db.requests.select())
        records = await cursor.fetchall()
        req = [dict(q) for q in records]
        return web.Response(text=str(req))

from aiohttp import web
from app.db import requests
from datetime import datetime
import uuid


async def handler(request):
    uuidv4 = uuid.uuid4()
    if request.rel_url.query:
        attachment_depth = request.rel_url.query['attachment_depth']
    async with request.app['db'].acquire() as conn:
        cursor = await conn.execute(requests.insert().values({'request_uuid': uuidv4,
                                                              'request_date': datetime.today().isoformat(),
                                                              'attachment': {'entity': {'entity': {}}}}))
        inserted_id = await cursor.fetchone()
        a = await conn.execute(requests.select().where(requests.c.id == inserted_id[0]))
        data = await a.fetchone()
        return web.Response(text=str(data))

from aiohttp import web
from app.db import requests
from datetime import datetime
import uuid
import json


def get_layers(record, counter):
    if counter > 0:
        return {'entity': get_layers(record, counter - 1)}
    return {'entity': ''}


async def handler(request):
    uuidv4 = uuid.uuid4()
    dtime = datetime.today().isoformat()
    attachment_depth = request.rel_url.query['attachment_depth'] if request.rel_url.query else '0'
    attachment_depth = int(attachment_depth) if attachment_depth.isdigit() else 0
    attachment = get_layers({'entity': ''}, attachment_depth)

    async with request.app['db'].acquire() as conn:
        cursor = await conn.execute(requests.insert().values({'request_uuid': uuidv4,
                                                              'request_date': dtime,
                                                              'attachment': attachment}))
        inserted_id = await cursor.fetchone()
        data = dict(zip(('request_uuid', 'request_date', 'attachment'), map(str, (uuidv4, dtime, attachment))))
        return web.json_response(data)

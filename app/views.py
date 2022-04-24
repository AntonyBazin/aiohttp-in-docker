from aiohttp.web import json_response


async def handler(request):
    data = {'some': 'data'}
    return json_response(data)

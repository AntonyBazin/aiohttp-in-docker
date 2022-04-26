"""The tester script is part 3 of the task. It was intended to be completely independent from the server."""
import getopt
import sys
import json
import yaml
import pathlib

import aiohttp
import asyncio
from aiopg.sa import create_engine
from sqlalchemy import (
    MetaData, Table, Column,
    Integer, String, JSON, DateTime, select
)
import tqdm

meta = MetaData()
requests = Table(
    'requests', meta,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('request_uuid', String(36), unique=True, nullable=False),
    Column('request_date', DateTime, nullable=False),
    Column('attachment', JSON, nullable=False),
)

options = 'hn:d:'
long_options = ['hide', 'help', 'N=', 'depth=']
target_url = 'http://127.0.0.1:8080'


def set_params():
    n, d, hide_output = 0, 0, 0
    try:
        arguments, values = getopt.getopt(sys.argv[1:], options, long_options)
        for opt, arg in arguments:
            if opt in ('-h', '--help'):
                print('N(n) - number of HTTP requests; depth(d) - the nested JSON attachment depth.')
            elif opt in ('-n', '--N'):
                n = int(arg) if arg.isdigit() else 0
            elif opt in ('-d', '--depth'):
                d = int(arg) if arg.isdigit() else 0
            elif opt == '--hide':
                hide_output = 1
        print(f'Set N={n}, depth={d}, hide output = {bool(hide_output)}')
    except getopt.error as err:
        print(str(err))
    return n, d, hide_output


def get_config(path):
    with open(path / 'config' / 'config.yaml') as f:
        parsed_config = yaml.safe_load(f)
        return parsed_config


async def make_request(url, session, d, engine, hide_output):
    params = {'attachment_depth': d}
    outputs = []
    try:
        async with session.get(url, params=params) as resp:
            req_uuid = json.loads(await resp.text())['request_uuid']
            async with engine.acquire() as conn:
                cursor = await conn.execute(select([requests.c.request_uuid, requests.c.id])
                                            .where(requests.c.request_uuid.like(req_uuid)))
                res = await cursor.fetchone()
                if not hide_output:
                    print('\n', res)
    except Exception as e:
        print(f'Unable to get {url} due to {e.__class__}: {e.args}.')
    finally:
        return outputs


async def make_all_requests(target, n, d, h):
    ret = []
    config = get_config(pathlib.Path(__file__).parent)
    async with aiohttp.ClientSession() as session:
        async with create_engine(**config['postgres']) as engine:
            for f in tqdm.tqdm(asyncio.as_completed(
                    [make_request(target, session, d, engine, h) for _ in range(n)]),
                    total=n):
                ret.append(await f)
    print(f'Finalized all. Got a list of {len(ret)} outputs.')
    return ret


if __name__ == '__main__':
    number, depth, hide = set_params()
    asyncio.run(make_all_requests(target_url, number, depth, hide))

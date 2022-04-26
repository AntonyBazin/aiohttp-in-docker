import getopt
import sys

import aiohttp
import asyncio
import tqdm

options = 'hvn:d:'
long_options = ['help', 'verbose', 'N=', 'depth=']
target_url = 'http://127.0.0.1:8080'


def set_params():
    n, d, v = 0, 0, 0
    try:
        arguments, values = getopt.getopt(sys.argv[1:], options, long_options)
        for opt, arg in arguments:
            if opt in ('-h', '--help'):
                print('N(n) - number of HTTP requests; depth(d) - the nested JSON attachment depth.'
                      ' With verbose arg, prints all responses')
            elif opt in ('-n', '--N'):
                n = int(arg) if arg.isdigit() else 0
            elif opt in ('-d', '--depth'):
                d = int(arg) if arg.isdigit() else 0
            elif opt in ('-v', '--verbose'):
                v = 1
        print(f'Set N={n}, depth={d}')
        if v:
            print('Verbose mode')
    except getopt.error as err:
        print(str(err))
    return n, d, v


async def make_request(url, session, d, v):
    params = {'attachment_depth': d}
    outputs = []
    try:
        async with session.get(url, params=params) as resp:
            if v:
                print(await resp.text())
    except Exception as e:
        print(f'Unable to get {url} due to {e.__class__}.')
    finally:
        return outputs


async def make_all_requests(target, n, d, v):
    ret = []
    async with aiohttp.ClientSession() as session:
        for f in tqdm.tqdm(asyncio.as_completed([make_request(target, session, d, v) for _ in range(n)]), total=n):
            ret.append(await f)
    print(f'Finalized all. Got a list of {len(ret)} outputs.')
    return ret

if __name__ == '__main__':
    number, depth, verbose = set_params()
    asyncio.run(make_all_requests(target_url, number, depth, verbose))

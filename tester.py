import getopt
import sys

import aiohttp

options = 'hn:d:'
long_options = ['help', 'N=', 'depth=']


def set_params():
    n, d = 0, 0
    try:
        arguments, values = getopt.getopt(sys.argv[1:], options, long_options)
        for opt, arg in arguments:
            if opt in ('-h', '--help'):
                print('N(n) - number of HTTP requests; depth(d) - the nested JSON attachment depth')
            elif opt in ('-n', '--N'):
                n = int(arg) if arg.isdigit() else 0
            elif opt in ('-d', '--depth'):
                d = int(arg) if arg.isdigit() else 0
        print(f'Set N={n}, depth={d}')
    except getopt.error as err:
        print(str(err))
    return n, d


# def make_request(n, d):
#     params = {'attachment_depth': d}
#     async with aiohttp.ClientSession() as session:
#         async with session.get('http://localhost:8080/get', params=params) as resp:
#             print(resp.json())


if __name__ == '__main__':
    number, depth = set_params()

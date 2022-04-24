from sqlalchemy import create_engine

from app.settings import config
from db import requests

DSN = 'postgresql://{user}:{password}@{host}:{port}/{database}'


def fill_data(engine):
    conn = engine.connect()
    conn.execute(requests.insert(), [
        {'id': 0,
         'request_uuid': '12345',
         'request_date': 'January 8 04:05:06 1999 MSK',
         'attachment': {'entity': {}}},
    ])
    conn.execute(requests.insert(), [
        {'id': 1,
         'request_uuid': '0',
         'request_date': 'January 8 09:07:01 2001 MSK',
         'attachment': {'entity': {'entity': {}}}},
    ])
    conn.execute(requests.insert(), [
        {'id': 2,
         'request_uuid': '1',
         'request_date': 'May 12 12:11:11 2012 MSK',
         'attachment': {'entity': {}}},
    ])
    conn.close()


if __name__ == '__main__':
    db_url = DSN.format(**config['postgres'])
    engine = create_engine(db_url)
    fill_data(engine)
    print('Mock data: Finished')

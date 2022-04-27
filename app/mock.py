from datetime import datetime
import uuid

from sqlalchemy import create_engine

from settings import config
from db import requests

DSN = 'postgresql://{user}:{password}@{host}:{port}/{database}'


def fill_data(engine):
    conn = engine.connect()
    engine.execute(requests.delete())
    conn.execute(requests.insert(), [
        {'request_uuid': uuid.uuid4(),
         'request_date': datetime(2000, 1, 2, 4, 7, 57).isoformat(),
         'attachment': {'entity': {}}},
    ])
    conn.execute(requests.insert(), [
        {'request_uuid': uuid.uuid4(),
         'request_date': datetime(2007, 2, 2, 2, 2, 22).isoformat(),
         'attachment': {'entity': {'entity': {}}}},
    ])
    conn.execute(requests.insert(), [
        {'request_uuid': uuid.uuid4(),
         'request_date': datetime(2022, 6, 20, 13, 0, 3).isoformat(),
         'attachment': {'entity': {}}},
    ])
    conn.close()


if __name__ == '__main__':
    db_url = DSN.format(**config['postgres'])
    engine = create_engine(db_url)
    fill_data(engine)
    print('Mock data: Finished')

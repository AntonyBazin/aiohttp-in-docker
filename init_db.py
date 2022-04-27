from sqlalchemy import create_engine, MetaData

from app.settings import config
from app.db import requests

DSN = 'postgresql://{user}:{password}@{host}:{port}/{database}'


def create_tables(engine):
    meta = MetaData()
    meta.create_all(bind=engine, tables=[requests])


if __name__ == '__main__':
    db_url = DSN.format(**config['postgres'])
    print(db_url)
    engine = create_engine(db_url)
    create_tables(engine)

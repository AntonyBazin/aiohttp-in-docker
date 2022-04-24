import aiopg.sa
from sqlalchemy import (
    MetaData, Table, Column,
    Integer, String, JSON, DateTime
)

__all__ = ['requests']

meta = MetaData()

requests = Table(
    'requests', meta,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('request_uuid', String(36), nullable=False),
    Column('request_date', DateTime, nullable=False),
    Column('attachment', JSON, nullable=False),
)


async def pg_context(app):
    conf = app['config']['postgres']
    engine = await aiopg.sa.create_engine(
        database=conf['database'],
        user=conf['user'],
        password=conf['password'],
        host=conf['host'],
        port=conf['port'],
        minsize=conf['minsize'],
        maxsize=conf['maxsize'],
    )
    app['db'] = engine

    yield

    app['db'].close()
    await app['db'].wait_closed()

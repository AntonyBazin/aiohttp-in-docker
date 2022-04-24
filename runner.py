from aiohttp import web
from app import app
import logging


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    web.run_app(app)

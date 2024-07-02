from logging import basicConfig
from os import environ
basicConfig(
    format="%(asctime)s - [%(levelname)s] - %(name)s : %(message)s",
    **({'filename':environ['LOGGING_FILE']}  if environ.get('LOGGING_FILE') else {})
)

from . import client, down, server, utils

__all__ = [
    'client',
   'down',
   'server',
   'utils'
]
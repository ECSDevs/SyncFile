from . import client, mixed, server
from logging import basicConfig

basicConfig(
    format="%(asctime)s - [%(levelname)s] - %(name)s : %(message)s"
)

__all__ = [
    'client',
   'mixed',
   'server'
]
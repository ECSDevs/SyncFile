from logging import getLogger
from logging.handlers import FileHandler

# init logger
logger = getLogger(__name__)
logger.propagate = False

# init log handler
logHandler = FileHandler(f"MCSMT.log")
logHandler.setLevel("DEBUG")  # always debug before stable release
logger.setLevel("DEBUG")  # ditto
logger.addHandler(logHandler)
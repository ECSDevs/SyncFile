from logging import getLogger, FileHandler, Formatter

# init logger
logger = getLogger(__name__)
logger.propagate = False

# init log handler
logHandler = FileHandler(f"MCSMT.log")
logHandler.setLevel("DEBUG")  # always debug before stable release

# init log formatter
logFormatter = Formatter("%(asctime)s [%(levelname)s] %(message)s")
logHandler.setFormatter(logFormatter)

# add log handler
logger.setLevel("DEBUG")  # ditto
logger.addHandler(logHandler)


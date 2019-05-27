import logging.config

logging.config.fileConfig("./lib/logconf.ini")
logger = logging.getLogger(__name__)

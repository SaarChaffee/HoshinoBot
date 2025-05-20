import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler

os.makedirs('./log', exist_ok=True)
log_dir = os.path.expanduser('./log')

formatter = logging.Formatter('[%(asctime)s %(name)s] %(levelname)s: %(message)s')

default_handler = logging.StreamHandler(sys.stdout)
default_handler.setFormatter(formatter)

full_handler = TimedRotatingFileHandler(
    filename=os.path.join(log_dir, 'full.log'),
    when='midnight',
    interval=1,
    backupCount=7,
    encoding='utf8'
)
full_handler.setLevel(logging.DEBUG)
full_handler.setFormatter(formatter)
full_handler.suffix = "%Y-%m-%d.log"

error_handler = TimedRotatingFileHandler(
    filename=os.path.join(log_dir, 'error.log'),
    when='midnight',
    interval=1,
    backupCount=30,
    encoding='utf8'
)
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(formatter)
error_handler.suffix = "%Y-%m-%d.log"

def new_logger(name, debug=True):
    logger = logging.getLogger(name)
    logger.addHandler(default_handler)
    logger.addHandler(full_handler)
    logger.addHandler(error_handler)
    logger.setLevel(logging.DEBUG if debug else logging.INFO)
    return logger

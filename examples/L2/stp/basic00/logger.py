from logging import getLogger, StreamHandler, DEBUG
import sys

def start_log(lib: str):
  logger = getLogger(lib)
  logger.addHandler(StreamHandler(stream=sys.stdout))
  logger.setLevel(DEBUG)
  return logger
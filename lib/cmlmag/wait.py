import time
from tools import flprint

def retry(count: int, result, sleep_time: int):
  def _retry(func):
    def wrapper(*args, **kwargs):
      flag = False
      for i in range(count):
        flprint(f"retry: #{i+1}")
        res = func(*args, **kwargs)
        if res == result:
          flag = True
          flprint("next..")
          break
        else:
          flprint("fail. wait for retry...")
          time.sleep(sleep_time)
      return flag
    return wrapper
  return _retry
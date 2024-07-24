import time
def retry(count: int, result, sleep_time: int):
  def _retry(func):
    def wrapper(*args, **kwargs):
      flag = False
      for i in range(count):
        print(f"retry: #{i+1}")
        res = func(*args, **kwargs)
        print(f"actual: {res}, expected: {result}")
        if res == result:
          flag = True
          print("next..")
          break
        else:
          print(f"fail. wait for retry {sleep_time}[s]")
          time.sleep(sleep_time)
      return flag
    return wrapper
  return _retry

def bretry(count: int, sleep_time: int):
  def _retry(func):
    def wrapper(*args, **kwargs):
      flag = False
      for i in range(count):
        print(f"retry: #{i+1}")
        res = func(*args, **kwargs)
        if res == True:
          flag = True
          print("next..")
          break
        else:
          print(f"fail. wait for retry {sleep_time}[s]")
          time.sleep(sleep_time)
      return flag
    return wrapper
  return _retry
from cmlmag.device import Device
import time
from cmlmag import wait
import sys

# populate
def populate_server_ping(device: Device, target_ip: str, count=5):
  @wait.retry(count=30, result=0, sleep_time=3)
  def _server_ping(device: Device):
    return device.server_ping(target_ip, count)
  return _server_ping(device)

def seconds(secs):
  print(f"wait for {secs}[s]")
  sys.stdout.flush()
  time.sleep(secs)
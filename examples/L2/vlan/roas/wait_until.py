from lib.device import Device
from lib import wait
import time
import calc

# retry


# populate
def populate_vlan(device: Device, count: int):
  @wait.retry(count=50, result=count, sleep_time=5)
  def _populate_vlan(device: Device):
    return calc.count_vlan(device)
  return _populate_vlan(device)

def populate_up(device: Device, count: int):
  @wait.retry(count=30, result=count, sleep_time=3)
  def _populate_up(device: Device):
    return calc.count_up_interfaces(device)
  
  return _populate_up(device)

@wait.retry(count=30, result=1, sleep_time=5)
def populate_rip(device: Device):
  return calc.count_route_code(device, 'rip')

@wait.retry(count=30, result=1, sleep_time=5)
def populate_static(device: Device):
  return calc.count_route_code(device, 'static')

def populate_router_ping(device: Device, target_ip: str):
  @wait.retry(count=30, result=0, sleep_time=3)
  def _populate_router_ping(device: Device):
    return calc.router_ping(device, target_ip)
  return _populate_router_ping(device)

def populate_server_ping(device: Device, target_ip: str, count=5):
  @wait.retry(count=30, result=0, sleep_time=3)
  def _server_ping(device: Device):
    return calc.server_ping(device, target_ip, count)
  return _server_ping(device)

def seconds(secs):
  print(f"wait for {secs}[s]")
  time.sleep(secs)
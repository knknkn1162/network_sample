from lib.device import Device
from lib import wait

# wait until
def count_route_code(device: Device, code):
  # if `show ip route rip`, SchemaEmptyParserError occurs
  res = device.parse("show ip route")
  routes = res.get('vrf', {}).get('default', {}).get('address_family', {}).get('ipv4', {}).get('routes', {})
  cnt = 0
  for key, val in routes.items():
    cnt += (val.get('source_protocol') == code)
  return cnt

def count_up_interfaces(device: Device):
  res = device.parse("show ip interface brief")
  cnt = 0
  for key, value in res['interface'].items():
    flag = True
    if value['status'] != 'up':
      flag = False
    if value['protocol'] != 'up':
      flag = False
    cnt = cnt + flag
  return cnt


def server_ping(device: Device, target_ip: str, count):
  res: list[str] = device.execs([
    f"ping {target_ip} -c {count}",
    f"echo $?",
  ])
  return int(res[1].strip())

def router_ping(device: Device, target_ip):
  res = device.parse(f"ping {target_ip}")
  count = res.get('ping', {}).get('repeat', {})
  received = res.get('ping', {}).get('statistics', {}).get('received', {})
  return not (count == received)

# populates
def populate_up(device: Device, count: int):
  @wait.retry(count=30, result=count, sleep_time=3)
  def _populate_up(device: Device):
    return count_up_interfaces(device)
  
  return _populate_up(device)

@wait.retry(count=30, result=1, sleep_time=5)
def populate_rip(device: Device):
  return count_route_code(device, 'rip')

@wait.retry(count=30, result=1, sleep_time=5)
def populate_static(device: Device):
  return count_route_code(device, 'static')

def populate_server_ping(device: Device, target_ip: str, count=5):
  @wait.retry(count=30, result=0, sleep_time=3)
  def _server_ping(device: Device):
    return server_ping(device, target_ip, count)
  return _server_ping(device)

def populate_router_ping(device: Device, target_ip: str):
  @wait.retry(count=30, result=0, sleep_time=3)
  def _populate_router_ping(device: Device):
    return router_ping(device, target_ip)
  return _populate_router_ping(device)
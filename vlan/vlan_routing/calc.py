from lib.device import Device
from lib import wait
import time

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

def count_vlan(device: Device):
  res = device.parse(f"show vlan")
  cnt = 0
  # {'vlans': {'1': {'vlan_id': '1', 'name': 'default', 'shutdown': False, 'state': 'active' ...
  for key, value in res['vlans'].items():
    if "default" in value['name']:
      continue
    if value['state'] != "active":
      continue
    cnt += 1
  return cnt
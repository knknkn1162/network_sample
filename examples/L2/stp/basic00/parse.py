from lib.device import Device
from lib import wait
import time
from structure.stp_info import StpInfo

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

def count_trunk(device: Device):
  res = device.parse(f"show interfaces trunk")
  cnt = 0
  for key, value in res['interface'].items():
    if value['status'] == "trunking":
      cnt += 1
  return cnt

def count_stp_status(device: Device, vlan_num: int, status: str):
  res = device.parse(f"show spanning-tree vlan {vlan_num}")
  count = 0
  for key1, value in res['pvst']['vlans'].items():
    for key2, value2 in value.get('interfaces', {}).items():
      if value2.get('port_state') == status:
        count += 1
  return count

def get_stp_info(device: Device, vlan_num: int, interface: str):
  res = device.parse(f"show spanning-tree vlan {vlan_num}")
  count = 0
  for key1, value in res['pvst']['vlans'].items():
    for key2, value2 in value.get('interfaces', {}).items():
      if key2 != interface:
        continue
      return StpInfo(
        cost=value2['cost'],
        port_priority=value2['port_priority'],
        port_num=value2['port_num'],
        role=value2['role'],
        port_state=value2['port_state'],
        type=value2['type'],
      )

def count_stp_status(device: Device, vlan_num: int, status: str, key: str):
  res = device.parse(f"show spanning-tree vlan {vlan_num}")
  count = 0
  for key1, value in res['pvst']['vlans'].items():
    for key2, value2 in value.get('interfaces', {}).items():
      if value2.get(key1) == status:
        count += 1

def count_etherchannel(device: Device, status:str, protocol: str=None):
  res = device.parse("show etherchannel summary")
  count = 0
  for _, value in res['interfaces'].items():
    proto: str = value.get('protocol')
    if (proto is not None) and (proto.lower() != protocol.lower()):
      return -1
    for _, value2 in value['members'].items():
      if value2['flags'] == status:
        count += 1
  return count

def count_eigrp_neighbors(device: Device, group: int):
  res = device.parse("show ip eigrp neighbors")
  count = 0
  for _, value in res['eigrp_instance'][str(group)]['vrf']['default']['address_family']['ipv4']['eigrp_interface'].items():
    count += 1
  return count


def _interface(device: Device, interface: str, item: str):
  res = device.parse("show ip interface brief")
  data = res.get('interface', {})
  interface0 = interface.lower().replace(' ', '')
  for key, value in data.items():
    if str(key).lower().replace(' ', '') == interface0:
      return value.get(item)
    
def ip_addr(device: Device, interface: str):
  return _interface(device, interface, item="ip_address")
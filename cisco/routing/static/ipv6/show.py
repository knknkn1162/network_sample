from lib.device import Device

def server_ping(device: Device, target_ip: str, count: int=5):
  res: list[str] = device.execs([
    f"ping {target_ip} -c {count}",
    f"echo $?",
  ])
  return int(res[1].strip())

def router_ping(device: Device, target_ip: str, count: int=5):
  res = device.execs([
    f"ping {target_ip} repeat {count}",
  ])
  return res[0]

def mac_ip(device: Device):
  return device.execs([
    f"show interfaces | i (.* line protocol is )|(.* address is)",
  ])

def ospf_neighbor(device: Device):
  return device.execs([
    f"show ip ospf neighbor"
  ])

# type: link_layer
def get_link_layer_ipv6(device: Device, interface: str):
  res = device.parse(
    f"show ipv6 interface {interface}",
  )
  data = res.get(interface, {}).get("ipv6", {})
  for key, value in data.items():
    origin = value.get("origin")
    if origin == "link_layer":
      return key
    
def get_global_ipv6(device: Device, interface: str):
  res = device.parse(
    f"show ipv6 interface {interface}",
  )
  data = res.get(interface, {}).get("ipv6", {})
  for key, value in data.items():
    if value.get("origin") is not None:
      continue
    return value.get("ip")
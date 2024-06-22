from lib.device import Device

def server_ping(device: Device, target_ip: str, count):
  res: list[str] = device.execs([
    f"ping {target_ip} -c {count}",
    f"echo $?",
  ])
  return int(res[1].strip())

def mac_ip(device: Device):
  return device.execs([
    f"show interfaces | i (.* line protocol is )|(.* address is)",
  ])

def ospf_neighbor(device: Device):
  return device.execs([
    f"show ip ospf neighbor"
  ])
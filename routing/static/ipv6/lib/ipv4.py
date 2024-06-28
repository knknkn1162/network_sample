import ipaddress

def get_network(ipv4_addr: str, subnet_mask: str, idx: int):
  return ipaddress.ip_interface(f"{ipv4_addr}/{subnet_mask}").network[idx]

def get_network0(ipv4_addr: str, subnet_mask: str):
  return get_network(ipv4_addr, subnet_mask, idx=0)

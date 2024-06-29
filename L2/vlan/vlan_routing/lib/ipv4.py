import ipaddress

def get_network0(ipv4_addr: str, subnet_mask: str):
  return ipaddress.ip_interface(f"{ipv4_addr}/{subnet_mask}").network[0]

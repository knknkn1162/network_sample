import ipaddress

def get_network0(ipv6_addr: str, prefixlen):
  return ipaddress.ip_interface(f"{ipv6_addr}/{prefixlen}").network[0]
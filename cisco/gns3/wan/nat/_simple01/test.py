from genie import testbed
from cmlmag.cml import CONFIG_YAML, Cml
from cmlmag.device import Device
from cmlmag import wait, ipv4
import cmlmag.parse as parse
import cmlmag.wait_until as wait_until
import ini

def main():
  tb = testbed.load(CONFIG_YAML)
  # switch
  r1 = Device(tb, ini.r1.name)
  pc1 = Device(tb, ini.pc1.__name__)
  pc2 = Device(tb, ini.pc2.__name__)
  print("####### exec #######")

  # router setup
  r1.execs([
    [
      f"interface {ini.r1.f0_0.name}",
      f"ip addr {ini.r1.f0_0.ip_addr.ip} {ini.r1.f0_0.ip_addr.netmask}",
      f"no shutdown",
    ],
    [
      f"interface {ini.r1.f0_1.name}",
      f"ip addr dhcp",
      f"no shutdown",
    ],
    [
      f"ip domain-lookup",
    ],
  ])

  pc1.execs([
    f"ip {ini.pc1.eth0.ip_addr.ip} {ini.pc1.eth0.ip_addr.netmask} {ini.r1.f0_0.ip_addr.ip}",
    f"ip dns {ini.dns_server_addr}",
    f"show",
    f"show ip",
  ])

  pc2.execs([
    f"ip {ini.pc2.eth0.ip_addr.ip} {ini.pc2.eth0.ip_addr.netmask} {ini.r1.f0_0.ip_addr.ip}",
    f"ip dns {ini.dns_server_addr}",
    f"show",
    f"show ip",
  ])

  # pat settings
  # see https://www.infraexpert.com/study/dhcpz3.html
  r1.execs([
    [
      f"interface {ini.r1.f0_0.name}",
      f"ip nat inside",
    ],
    [
      f"interface {ini.r1.f0_1.name}",
      f"ip nat outside",
    ],
    [
      f"access-list {ini.acl_num} permit {ini.r1.f0_0.ip_addr.network.network_address} {ini.r1.f0_0.ip_addr.hostmask}",
      f"ip nat inside source list {ini.acl_num} interface {ini.r1.f0_1.name} overload",
    ],
    [
      f"ip route 0.0.0.0 0.0.0.0 dhcp"
    ],
  ])

  wait.seconds(5)
  pc1.vpcs_ping("8.8.4.4")
  r1.router_ping(ini.target_fqdn)
  pc1.vpcs_ping(ini.target_fqdn)
  pc2.vpcs_ping(ini.target_fqdn)
  r1.execs([
    f"show ip interface {ini.r1.f0_0.name}",
    f"show ip interface {ini.r1.f0_1.name}",
    f"show ip nat translations",
    f"show ip nat statistics",
  ])

if __name__ == '__main__':
  main()
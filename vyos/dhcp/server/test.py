from genie import testbed
from cmlmag.cml import CONFIG_YAML, Cml
from cmlmag.device import Device
from cmlmag import wait, ipv4
import cmlmag.parse as parse
import cmlmag.wait_until as wait_until
import ini
from cmlmag.structure.stp_info import (
  Role as StpRole,
  State as StpState
)

def main():

  tb = testbed.load(CONFIG_YAML)
  # switch
  vyos0 = Device(tb, 'vyos0')
  pc1 = Device(tb, 'pc1')

  vyos0.vyos_execs([
    [
      f"set interfaces ethernet {ini.vyos0.eth0.__name__} address {ini.vyos0.eth0.ip_addr}",
    ],
  ])

  # dhcp server settings
  vyos0.vyos_execs([
    [
      f"set service dhcp-server shared-network-name {ini.vyos0.eth0.dhcp.label} subnet {ini.vyos0.eth0.ip_addr.network} option default-router {ini.vyos0.eth0.ip_addr.ip}",
      #f"set service dhcp-server shared-network-name LAN subnet 192.168.0.0/24 option name-server 192.168.0.2",
      #f"set service dhcp-server shared-network-name LAN subnet 192.168.0.0/24 option domain-name vyos.net",
      f"set service dhcp-server shared-network-name {ini.vyos0.eth0.dhcp.label} subnet {ini.vyos0.eth0.ip_addr.network} lease 86400",
      f"set service dhcp-server shared-network-name {ini.vyos0.eth0.dhcp.label} subnet {ini.vyos0.eth0.ip_addr.network} range 0 start {ini.vyos0.eth0.dhcp.start.ip}",
      f"set service dhcp-server shared-network-name {ini.vyos0.eth0.dhcp.label} subnet {ini.vyos0.eth0.ip_addr.network} range 0 stop {ini.vyos0.eth0.dhcp.end.ip}",
      f"set service dhcp-server shared-network-name {ini.vyos0.eth0.dhcp.label} subnet {ini.vyos0.eth0.ip_addr.network} subnet-id 1",
      f"set service dhcp-server shared-network-name {ini.vyos0.eth0.dhcp.label} subnet {ini.vyos0.eth0.ip_addr.network} exclude {ini.vyos0.eth0.dhcp.exclude_address.ip}",
    ],
  ])

  pc1.execs([
    f"dhcp",
  ])

  wait_until.seconds(5)
  pc1.execs([
    f"show",
  ])

  vyos0.vyos_execs([
    f"show dhcp server leases",
    [
      f"show service dhcp-server shared-network-name {ini.vyos0.eth0.dhcp.label}",
    ]
  ])

  # it works
  for val in ini.pc1.eth0.expected_ip_addrs:
    pc1.vpcs_ping(val.ip)

if __name__ == '__main__':
  main()
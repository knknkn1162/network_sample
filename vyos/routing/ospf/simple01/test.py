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
  vyos1 = Device(tb, 'vyos1')
  vyos2 = Device(tb, 'vyos2')

  pc1 = Device(tb, 'pc1')
  pc2 = Device(tb, 'pc2')

  # ip
  pc1.execs([
    f"ip {ini.pc1.eth0.ip_addr.ip} {ini.pc1.eth0.ip_addr.netmask} {ini.vyos0.eth1.ip_addr.ip}",
    f"show",
  ])

  pc2.execs([
    f"ip {ini.pc2.eth0.ip_addr} {ini.pc2.eth0.ip_addr.netmask} {ini.vyos2.eth1.ip_addr.ip}",
    f"show",
  ])

  # ip setting
  vyos0.vyos_execs([
    [
      f"set interfaces ethernet eth0 address {ini.vyos0.eth0.ip_addr}",
      f"set interfaces ethernet eth1 address {ini.vyos0.eth1.ip_addr}",
      f"set interfaces loopback lo address {ini.vyos0.loop.ip_addr}",
    ],
  ])

  vyos1.vyos_execs([
    [
      f"set interfaces ethernet eth0 address {ini.vyos1.eth0.ip_addr}",
      f"set interfaces ethernet eth1 address {ini.vyos1.eth1.ip_addr}",
      f"set interfaces loopback lo address {ini.vyos1.loop.ip_addr}",
    ],
  ])

  vyos2.vyos_execs([
    [
      f"set interfaces ethernet eth0 address {ini.vyos2.eth0.ip_addr}",
      f"set interfaces ethernet eth1 address {ini.vyos2.eth1.ip_addr}",
      f"set interfaces loopback lo address {ini.vyos2.loop.ip_addr}",
    ],
  ])

  # ospf
  vyos0.vyos_execs([
    [
      f"set protocols ospf area 0 network {ini.vyos0.eth0.ip_addr.network}",
      f"set protocols ospf area 0 network {ini.vyos0.eth1.ip_addr.network}",
    ],
  ])

  vyos1.vyos_execs([
    [
      f"set protocols ospf area 0 network {ini.vyos1.eth0.ip_addr.network}",
      f"set protocols ospf area 0 network {ini.vyos1.eth1.ip_addr.network}",
    ],
  ])

  vyos2.vyos_execs([
    [
      f"set protocols ospf area 0 network {ini.vyos2.eth0.ip_addr.network}",
      f"set protocols ospf area 0 network {ini.vyos2.eth1.ip_addr.network}",
    ],
  ])

  wait_until.seconds(40)

  vyos0.vyos_execs([
    f"show ip route",
    f"show ip ospf route",
    f"show ip ospf neighbor",
    f"show ip ospf database",
  ])

  vyos1.vyos_execs([
    f"show ip route",
    f"show ip ospf route",
    f"show ip ospf neighbor",
    f"show ip ospf database",
  ])
  vyos2.vyos_execs([
    f"show ip route",
    f"show ip ospf route",
    f"show ip ospf neighbor",
    f"show ip ospf database",
  ])

  pc1.vpcs_ping(ini.pc2.eth0.ip_addr.ip)

if __name__ == '__main__':
  main()
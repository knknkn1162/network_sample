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
  r1 = Device(tb, 'R1')
  r2 = Device(tb, 'R2')
  r3 = Device(tb, 'R3')
  pc1 = Device(tb, 'pc1')
  pc2 = Device(tb, 'pc2')
  pc3 = Device(tb, 'pc3')

  # ip
  pc1.execs([
    f"ip {ini.pc1.eth0.ip_addr} {ini.pc1.eth0.subnet_mask} {ini.r1.f0_0.ip_addr}",
    f"show",
  ])

  pc2.execs([
    f"ip {ini.pc2.eth0.ip_addr} {ini.pc2.eth0.subnet_mask} {ini.r2.f0_0.ip_addr}",
    f"show",
  ])

  pc3.execs([
    f"ip {ini.pc3.eth0.ip_addr} {ini.pc3.eth0.subnet_mask} {ini.r3.f0_0.ip_addr}",
    f"show",
  ])

  # router setting
  r1_network0 = ipv4.get_network0(ini.r1.f0_0.ip_addr, ini.r1.f0_0.subnet_mask)
  r2_network0 = ipv4.get_network0(ini.r2.f0_0.ip_addr, ini.r2.f0_0.subnet_mask)
  r3_network0 = ipv4.get_network0(ini.r3.f0_0.ip_addr, ini.r3.f0_0.subnet_mask)

  r1.execs([
    [
      f"interface {ini.r1.f0_0.name}",
      f"ip addr {ini.r1.f0_0.ip_addr} {ini.r1.f0_0.subnet_mask}",
      f"no shutdown",
    ],
    [
      f"interface {ini.r1.s1_0.name}",
      f"ip addr {ini.r1.s1_0.ip_addr} {ini.r1.s1_0.subnet_mask}",
      f"encapsulation frame-relay",
      f"no frame-relay inverse-arp",
      f"frame-relay map ip {ini.r1.s1_0.dlci0.peer_ip_addr} {ini.r1.s1_0.dlci0.dlci.dlci_num}",
      f"frame-relay map ip {ini.r1.s1_0.dlci1.peer_ip_addr} {ini.r1.s1_0.dlci1.dlci.dlci_num}",
      f"no shutdown",
    ],
    [
      f"ip route {r2_network0} {ini.r2.f0_0.subnet_mask} {ini.r2.s1_0.ip_addr}",
      f"ip route {r3_network0} {ini.r3.f0_0.subnet_mask} {ini.r3.s1_0.ip_addr}",
    ],
  ])

  r2.execs([
    [
      f"interface {ini.r2.f0_0.name}",
      f"ip addr {ini.r2.f0_0.ip_addr} {ini.r2.f0_0.subnet_mask}",
      f"no shutdown",
    ],
    [
      f"interface {ini.r2.s1_0.name}",
      f"ip addr {ini.r2.s1_0.ip_addr} {ini.r2.s1_0.subnet_mask}",
      f"encapsulation frame-relay",
      f"no frame-relay inverse-arp",
      f"frame-relay map ip {ini.r2.s1_0.dlci0.peer_ip_addr} {ini.r2.s1_0.dlci0.dlci.dlci_num}",
      f"no shutdown",
    ],
    [
      f"ip route 0.0.0.0 0.0.0.0 {ini.r1.s1_0.ip_addr}",
    ],
  ])
  
  r3.execs([
    [
      f"interface {ini.r3.f0_0.name}",
      f"ip addr {ini.r3.f0_0.ip_addr} {ini.r3.f0_0.subnet_mask}",
      f"no shutdown",
    ],
    [
      f"interface {ini.r3.s1_0.name}",
      f"ip addr {ini.r3.s1_0.ip_addr} {ini.r3.s1_0.subnet_mask}",
      f"encapsulation frame-relay",
      f"no frame-relay inverse-arp",
      f"frame-relay map ip {ini.r3.s1_0.dlci0.peer_ip_addr} {ini.r3.s1_0.dlci0.dlci.dlci_num}",
      f"no shutdown",
    ],
    [
      f"ip route 0.0.0.0 0.0.0.0 {ini.r1.s1_0.ip_addr}",
    ],
  ])

  wait_until.seconds(60)

  # show result
  r1.execs([
    f"show frame-relay map",
  ])
  r2.execs([
    f"show frame-relay map",
  ])
  r3.execs([
    f"show frame-relay map",
  ])

  pc2.vpcs_ping(ini.pc1.eth0.ip_addr)
  pc2.vpcs_ping(ini.pc3.eth0.ip_addr)
  pc1.vpcs_ping(ini.pc3.eth0.ip_addr)

  # show result
  r1.execs([
    f"show frame-relay map",
  ])
  r2.execs([
    f"show frame-relay map",
  ])
  r3.execs([
    f"show frame-relay map",
  ])

if __name__ == '__main__':
  main()
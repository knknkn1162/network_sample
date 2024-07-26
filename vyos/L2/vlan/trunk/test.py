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
  pc1 = Device(tb, 'pc1')
  pc2 = Device(tb, 'pc2')
  pc3 = Device(tb, 'pc3')
  pc4 = Device(tb, 'pc4')

  # ip
  pc1.execs([
    f"ip {ini.pc1.eth0.ip_addr.ip} {ini.pc1.eth0.ip_addr.netmask}",
    f"show",
  ])

  pc2.execs([
    f"ip {ini.pc2.eth0.ip_addr.ip} {ini.pc2.eth0.ip_addr.netmask}",
    f"show",
  ])

  pc3.execs([
    f"ip {ini.pc3.eth0.ip_addr.ip} {ini.pc3.eth0.ip_addr.netmask}",
    f"show",
  ])

  pc4.execs([
    f"ip {ini.pc4.eth0.ip_addr.ip} {ini.pc4.eth0.ip_addr.netmask}",
    f"show",
  ])

  wait_until.seconds(5)
  # it should not work.
  pc1.vpcs_ping(ini.pc3.eth0.ip_addr.ip)
  pc1.vpcs_ping(ini.pc2.eth0.ip_addr.ip)
  pc2.vpcs_ping(ini.pc4.eth0.ip_addr.ip)


  vyos0.vyos_execs([
    [
      f"set interfaces bridge br0",
      f"set interfaces bridge br0 enable-vlan",
      # associate vlan to eth (access port)
      f"set interfaces bridge br0 member interface eth0 native-vlan {ini.vyos0.br0.eth0.vlan_num}",
      f"set interfaces bridge br0 member interface eth1 native-vlan {ini.vyos0.br0.eth1.vlan_num}",
      f"set interfaces bridge br0 member interface eth2 allowed-vlan {ini.vyos0.br0.eth2.allowed_vlan}",
    ],
  ])

  vyos1.vyos_execs([
    [
      f"set interfaces bridge br0",
      f"set interfaces bridge br0 enable-vlan",
      # associate vlan to eth (access port)
      f"set interfaces bridge br0 member interface eth0 native-vlan {ini.vyos1.br0.eth0.vlan_num}",
      f"set interfaces bridge br0 member interface eth1 native-vlan {ini.vyos1.br0.eth1.vlan_num}",
      f"set interfaces bridge br0 member interface eth2 allowed-vlan {ini.vyos1.br0.eth2.allowed_vlan}",
    ],
  ])

  wait_until.seconds(5)
  # it should work!
  pc1.vpcs_ping(ini.pc3.eth0.ip_addr.ip)
  # it should not work.
  pc1.vpcs_ping(ini.pc2.eth0.ip_addr.ip)
  pc2.vpcs_ping(ini.pc4.eth0.ip_addr.ip)

if __name__ == '__main__':
  main()
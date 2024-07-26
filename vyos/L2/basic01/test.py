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
  pc2 = Device(tb, 'pc2')

  # ip
  pc1.execs([
    f"ip {ini.pc1.eth0.ip_addr.ip} {ini.pc1.eth0.ip_addr.netmask}",
    f"show",
  ])

  pc2.execs([
    f"ip {ini.pc2.eth0.ip_addr.ip} {ini.pc2.eth0.ip_addr.netmask}",
    f"show",
  ])

  wait_until.seconds(5)
  # it does not work..
  pc1.vpcs_ping(ini.pc2.eth0.ip_addr.ip)


  vyos0.vyos_execs([
    [
      f"set interfaces bridge br0",
      f"set interfaces bridge br0 address {ini.vyos0.br0.ip_addr}",
      f"set interfaces bridge br0 member interface eth0",
      f"set interfaces bridge br0 member interface eth1",
    ],
  ])

  wait_until.seconds(5)
  pc1.vpcs_ping(ini.pc2.eth0.ip_addr.ip)

if __name__ == '__main__':
  main()
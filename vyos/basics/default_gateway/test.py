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

  # ip
  pc1.execs([
    f"ip {ini.pc1.eth0.ip_addr} {ini.pc1.eth0.subnet_mask} {ini.vyos0.eth0.ip_addr}",
    f"show",
  ])

  vyos0.execs([
    f"configure",
    f"set interfaces ethernet {ini.vyos0.eth0.__name__} address {ini.vyos0.eth0.ip_addr}/{ini.vyos0.eth0.prefix_len}",
    f"commit",
    f"exit",
  ])

  pc1.vpcs_ping(ini.vyos0.eth0.ip_addr)

if __name__ == '__main__':
  main()
from genie import testbed
from cmlmag.cml import CONFIG_YAML, Cml
from cmlmag.device import Device
from cmlmag import wait, ipv4
import cmlmag.parse as parse
import cmlmag.wait_until as wait_until
import ini
import time
from cmlmag.structure.stp_info import (
  Role as StpRole,
  State as StpState
)

def main():
  tb = testbed.load(CONFIG_YAML)
  iosv_0 = Device(tb, ini.iosv_0.__name__)

  iosv_0.execs([
    [
      f"interface {ini.iosv_0.g0_0.name}",
      f"ip addr dhcp",
      f"no shutdown",
    ]
  ])

  wait_until.seconds(5)

  iosv_0.execs([
    f"show ip interface brief",
  ])

if __name__ == '__main__':
  main()
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

  iosv_0 = Device(tb, 'iosv_0')
  iosv_1 = Device(tb, 'iosv_1')

  cml = Cml()
  pcap = cml.lab.create_pcap(iosv_0.name, iosv_0.name, auth_token=cml.auth_token)


  print("####### exec #######")

  # no need to setup ip addr
  # preparation; no cdp
  iosv_0.execs([
    [
      f"no cdp run",
    ]
  ])

  iosv_1.execs([
    [
      f"no cdp run",
    ]
  ])

  pcap.start(maxpackets=500)
  iosv_0.execs([
    [
      f"lldp run",
    ],
    [
      f"interface {ini.iosv_0.g0_0.name}",
      f"no shutdown",
    ],
  ])

  iosv_1.execs([
    [
      f"lldp run",
    ],
    [
      f"interface {ini.iosv_0.g0_0.name}",
      f"no shutdown",
    ],
  ])
  wait_until.seconds(45)
  pcap.download(file=ini.pcap_file)
  iosv_0.execs([
    f"show lldp",
    f"show lldp interface",
    f"show lldp neighbors",
    f"show lldp neighbors detail",
    f"show lldp entry *",
  ])

  iosv_1.execs([
    f"show lldp",
    f"show lldp interface",
    f"show lldp neighbors",
    f"show lldp neighbors detail",
    f"show lldp entry *",
  ])
if __name__ == '__main__':
  main()
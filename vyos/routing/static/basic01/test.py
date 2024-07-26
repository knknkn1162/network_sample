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

  # ip

  wait_until.seconds(5)

  vyos0.vyos_execs([
    [
      f"set interfaces ethernet eth0 address {ini.vyos0.eth0.ip_addr}",
      f"set interfaces loopback lo address {ini.vyos0.loop.ip_addr}",
    ],
  ])

  vyos1.vyos_execs([
    [
      f"set interfaces ethernet eth0 address {ini.vyos1.eth0.ip_addr}",
      f"set interfaces loopback eth1 address {ini.vyos1.eth1.ip_addr}",
    ],
  ])

  vyos2.vyos_execs([
    [
      f"set interfaces ethernet eth0 address {ini.vyos2.eth0.ip_addr}",
      f"set interfaces loopback lo address {ini.vyos2.loop.ip_addr}",
    ],
  ])

  # static routing
  vyos0.vyos_execs([
    [
      f"set protocols static route 0.0.0.0/0 next-hop {ini.vyos1.eth0.ip_addr}",
    ]
  ])

  vyos2.vyos_execs([
    [
      f"set protocols static route 0.0.0.0/0 next-hop {ini.vyos1.eth1.ip_addr}",
    ]
  ])

  vyos1.vyos_execs([
    [
      f"set protocols static route {ini.vyos0.loop.ip_addr} next-hop {ini.vyos0.eth0.ip_addr.ip}",
      f"set protocols static route {ini.vyos2.loop.ip_addr} next-hop {ini.vyos2.eth0.ip_addr.ip}",
    ]
  ])

  vyos0.vyos_execs([
    f"show ip route",
  ])

  vyos1.vyos_execs([
    f"show ip route",
  ])
  vyos2.vyos_execs([
    f"show ip route",
  ])

  vyos0.vyos_ping(ini.vyos2.loop.ip_addr.ip)

if __name__ == '__main__':
  main()
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

  cml0 = Cml()
  #pcap01 = Pcap(cml0, ini.iosv_0.__name__, ini.iosv_1.__name__)

  print("####### exec #######")

  # interface up
  iosv_0.execs([
    [
      f"interface {ini.iosv_0.g0_0.name}",
      f"ip addr {ini.iosv_0.g0_0.ip_addr} {ini.iosv_0.g0_0.subnet_mask}",
      f"no shutdown",
    ],
  ])

  iosv_1.execs([
    [
      f"interface {ini.iosv_1.g0_0.name}",
      f"ip addr {ini.iosv_1.g0_0.ip_addr} {ini.iosv_1.g0_0.subnet_mask}",
      f"no shutdown",
    ]
  ])

  iosv_0.show_mac_ip()
  iosv_1.show_mac_ip()

  # check hardware based time
  iosv_0.execs([
    f"show ntp status",
    f"show clock detail",
    f"show ntp associations",
  ])

  iosv_1.execs([
    f"show ntp status",
    f"show clock detail",
    f"show ntp associations",
  ])

  # server
  iosv_0.execs([
    f"clock set 00:00:00 1 Jan 2023",
    [
      f"clock timezone JST 9",
      f"ntp master",
      f"ntp authenticate",
      f"ntp authentication-key {ini.ntp_key_num} md5 {ini.ntp_key}",
      f"ntp trusted-key {ini.ntp_key_num}",
    ],
  ])
  # client
  iosv_1.execs([
    [
      f"clock timezone JST 9",
      f"ntp authenticate",
      f"ntp authentication-key {ini.ntp_key_num} md5 {ini.ntp_key}",
      f"ntp trusted-key {ini.ntp_key_num}",
      f"ntp server {ini.iosv_0.g0_0.ip_addr} key {ini.ntp_key_num}",
    ]
  ])

  wait_until.seconds(120)
  # it should work...
  iosv_0.execs([
    f"show ntp status",
    f"show clock detail",
    f"show ntp associations",
  ])

  # it should work...
  iosv_1.execs([
    f"show ntp status",
    f"show clock detail",
    f"show ntp associations",
  ])

if __name__ == '__main__':
  main()
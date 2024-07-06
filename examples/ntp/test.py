from genie import testbed
from cml import CONFIG_YAML, Cml, Pcap
from lib.device import Device
from lib import wait, ipv4
import ini
import time
import wait_until, calc
import show

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
    f"i {ini.iosv_0.g0_0.name}",
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

show.mac_ip(iosv_0)
show.mac_ip(iosv_1)

iosv_1.execs([
  [
    f"clock timezone JST 9",
    f"ntp master 7",
  ]
])

iosv_0.execs([
  [
    f"clock timezone JST 9",
    f"ntp server {ini.iosv_1.g0_0.ip_addr}",
  ]
])

wait_until.seconds(30)

iosv_0.execs([
  f"show ntp status",
  f"show ntp associations",
])

iosv_1.execs([
  f"show ntp status",
  f"show ntp associations",
])
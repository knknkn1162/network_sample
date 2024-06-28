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
iosv_2 = Device(tb, 'iosv_2')
iosv_3 = Device(tb, 'iosv_3')

cml0 = Cml()

print("####### exec #######")

# interface up
iosv_0.execs([
  [
    f"interface {ini.iosv_0.g0_0.name}",
    f"ip addr {ini.iosv_0.g0_0.ip_addr} {ini.iosv_0.g0_0.subnet_mask}",
    f"no shutdown",
  ],
  [
    f"interface {ini.iosv_0.g0_1.name}",
    f"ip addr {ini.iosv_0.g0_1.ip_addr} {ini.iosv_0.g0_1.subnet_mask}",
    f"no shutdown",
  ],
])

iosv_1.execs([
  [
    f"interface {ini.iosv_1.g0_0.name}",
    f"ip addr {ini.iosv_1.g0_0.ip_addr} {ini.iosv_1.g0_0.subnet_mask}",
    f"no shutdown",
  ],
  [
    f"interface {ini.iosv_1.g0_1.name}",
    f"ip addr {ini.iosv_1.g0_1.ip_addr} {ini.iosv_1.g0_1.subnet_mask}",
    f"no shutdown",
  ],
])

iosv_2.execs([
  [
    f"interface {ini.iosv_2.g0_0.name}",
    f"ip addr {ini.iosv_2.g0_0.ip_addr} {ini.iosv_2.g0_0.subnet_mask}",
    f"no shutdown",
  ],
  [
    f"interface {ini.iosv_2.g0_1.name}",
    f"ip addr {ini.iosv_2.g0_1.ip_addr} {ini.iosv_2.g0_1.subnet_mask}",
    f"no shutdown",
  ],
])

iosv_3.execs([
  [
    f"interface {ini.iosv_3.g0_0.name}",
    f"ip addr {ini.iosv_3.g0_0.ip_addr} {ini.iosv_3.g0_0.subnet_mask}",
    f"no shutdown",
  ],
  [
    f"interface {ini.iosv_3.g0_1.name}",
    f"ip addr {ini.iosv_3.g0_1.ip_addr} {ini.iosv_3.g0_1.subnet_mask}",
    f"no shutdown",
  ],
])

g0_0_net0 = ipv4.get_network0(ini.iosv_4.g0_0.ip_addr, ini.iosv_4.g0_0.subnet_mask)
administrative_distance = 2
iosv_0.execs([
  [
    # route#1
    f"ip route {g0_0_net0} {ini.iosv_4.g0_0.subnet_mask} {ini.iosv_1.g0_0.ip_addr}",
    # route#2
    f"ip route {g0_0_net0} {ini.iosv_4.g0_0.subnet_mask} {ini.iosv_2.g0_0.ip_addr} {administrative_distance}",
  ]
])

# route#1
iosv_0.execs([
  f"show ip route"
])

iosv_0.execs([
  [
    f"interface {ini.iosv_1.g0_0.name}",
    f"shutdown",
  ],
])

# route#2
iosv_0.execs([
  f"show ip route",
])
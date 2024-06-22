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
iosv_201 = Device(tb, 'iosv_201')
iosv_202 = Device(tb, 'iosv_202')


cml0 = Cml()
#pcap = Pcap(cml0, ini.iosv_0.__name__, ini.iosv_1.__name__)

print("####### exec #######")

# interface up
iosv_0.execs([
  [
    f"interface {ini.iosv_0.g0_0.name}",
    f"ip addr {ini.iosv_0.g0_0.ip_addr} {ini.iosv_0.g0_0.subnet_mask}",
    f"no shutdown",
  ]
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
  [
    f"interface {ini.iosv_1.g0_2.name}",
    f"ip addr {ini.iosv_1.g0_2.ip_addr} {ini.iosv_1.g0_2.subnet_mask}",
    f"no shutdown",
  ],
])

iosv_201.execs([
  [
    f"interface {ini.iosv_201.g0_0.name}",
    f"ip addr {ini.iosv_201.g0_0.ip_addr} {ini.iosv_201.g0_0.subnet_mask}",
    f"no shutdown",
  ],
])

iosv_202.execs([
  [
    f"interface {ini.iosv_202.g0_0.name}",
    f"ip addr {ini.iosv_202.g0_0.ip_addr} {ini.iosv_202.g0_0.subnet_mask}",
    f"no shutdown",
  ],
])

show.mac_ip(iosv_0)
show.mac_ip(iosv_1)
show.mac_ip(iosv_201)
show.mac_ip(iosv_202)

# rip
g0_0_network0 = ipv4.get_network0(ini.iosv_0.g0_0.ip_addr, ini.iosv_0.g0_0.subnet_mask)

iosv_0.execs([
  [
    f"router rip",
    f"version 2",
    f"network {g0_0_network0}",
    f"no auto-summary",
  ],
])

g0_0_network0 = ipv4.get_network0(ini.iosv_1.g0_0.ip_addr, ini.iosv_1.g0_0.subnet_mask)
g0_1_network0 = ipv4.get_network0(ini.iosv_1.g0_1.ip_addr, ini.iosv_1.g0_1.subnet_mask)
g0_2_network0 = ipv4.get_network0(ini.iosv_1.g0_2.ip_addr, ini.iosv_1.g0_2.subnet_mask)

iosv_1.execs([
  [
    f"router rip",
    f"version 2",
    f"network {g0_0_network0}",
    f"network {g0_1_network0}",
    f"network {g0_2_network0}",
    f"no auto-summary",
  ],
])

g0_0_network0 = ipv4.get_network0(ini.iosv_201.g0_0.ip_addr, ini.iosv_201.g0_0.subnet_mask)
iosv_201.execs([
  [
    f"router rip",
    f"version 2",
    f"network {g0_0_network0}",
    f"no auto-summary",
  ],
])

g0_0_network0 = ipv4.get_network0(ini.iosv_202.g0_0.ip_addr, ini.iosv_202.g0_0.subnet_mask)
iosv_202.execs([
  [
    f"router rip",
    f"version 2",
    f"network {g0_0_network0}",
    f"no auto-summary",
  ],
])

# test
wait_until.populate_router_ping(iosv_0, ini.iosv_201.g0_0.ip_addr)
wait_until.populate_router_ping(iosv_0, ini.iosv_202.g0_0.ip_addr)

iosv_0.execs([
  f"show ip protocols",
  f"show ip rip database",
  f"show ip route rip"
])

# summary address manually to iosv_1
g0_0_network0 = ipv4.get_network0(ini.iosv_201.g0_0.ip_addr, ini.iosv_201.g0_0.subnet_mask)
iosv_1.execs([
  [
    f"interface {ini.iosv_1.g0_0.name}",
    f"ip summary-address rip {g0_0_network0} {ini.SUBNET_MASK_23}"
  ]
])
# after 3min, possibly down
wait_until.populate_rip(iosv_0, count=1, sleep_time=20)

iosv_0.execs([
  #f"show ip protocols",
  f"show ip rip database",
  f"show ip route rip",
])
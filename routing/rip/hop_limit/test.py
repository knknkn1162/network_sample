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
#pcap = Pcap(cml0, ini.iosv_0.__name__, ini.iosv_1.__name__)

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
])

show.mac_ip(iosv_0)
show.mac_ip(iosv_1)
show.mac_ip(iosv_2)
show.mac_ip(iosv_3)

# RIP settings
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
iosv_1.execs([
  [
    f"router rip",
    f"version 2",
    f"network {g0_0_network0}",
    f"network {g0_1_network0}",
    f"no auto-summary",
  ],
])

g0_0_network0 = ipv4.get_network0(ini.iosv_2.g0_0.ip_addr, ini.iosv_2.g0_0.subnet_mask)
g0_1_network0 = ipv4.get_network0(ini.iosv_2.g0_1.ip_addr, ini.iosv_2.g0_1.subnet_mask)
iosv_2.execs([
  [
    f"router rip",
    f"version 2",
    f"network {g0_0_network0}",
    f"network {g0_1_network0}",
    f"no auto-summary",
  ],
])

g0_0_network0 = ipv4.get_network0(ini.iosv_3.g0_0.ip_addr, ini.iosv_3.g0_0.subnet_mask)
iosv_3.execs([
  [
    f"router rip",
    f"version 2",
    f"network {g0_0_network0}",
    f"no auto-summary",
  ],
])

wait_until.populate_rip(iosv_3, 2)
wait_until.populate_router_ping(iosv_0, ini.iosv_3.g0_0.ip_addr)


g0_0_network0 = ipv4.get_network0(ini.iosv_1.g0_0.ip_addr, ini.iosv_1.g0_0.subnet_mask)
access_num = 1
# change hop settings so that we can check reject the information (metrics >= 16)
iosv_1.execs([
  [
    f"access-list {access_num} permit {g0_0_network0} {ini.INVERSE_MASK_24}"
  ],
  [
    f"router rip",
    # The metric of gi 0/1 gets 15
    f"offset-list {access_num} out 14 {ini.iosv_1.g0_1.name}"
  ],
])

wait_until.populate_router_ping(iosv_0, ini.iosv_2.g0_1.ip_addr)
# it should fail
show.router_ping(iosv_0, ini.iosv_3.g0_0.ip_addr, count=10)

iosv_0.execs([
  f"show ip protocols",
  f"show ip rip database",
  f"show ip route rip",
])

iosv_1.execs([
  f"show ip protocols",
  f"show ip rip database",
  f"show ip route rip",
])

iosv_2.execs([
  f"show ip protocols",
  f"show ip rip database",
  f"show ip route rip",
])

iosv_3.execs([
  f"show ip protocols",
  f"show ip rip database",
  f"show ip route rip",
])
from genie import testbed
from cml import CONFIG_YAML, Cml, Pcap
from lib.device import Device
from lib import wait, ipv6
import ini
import time
import wait_until, calc
import show

tb = testbed.load(CONFIG_YAML)

# switch

iosv_0 = Device(tb, 'iosv_0')
iosv_1 = Device(tb, 'iosv_1')
iosv_2 = Device(tb, 'iosv_2')

cml0 = Cml()

print("####### exec #######")

# interface up
iosv_0.execs([
  [
    f"ipv6 unicast-routing",
  ],
  [
    f"interface {ini.iosv_0.g0_0.name}",
    f"ipv6 address {ini.iosv_0.g0_0.link_local_ipv6_addr} link-local",
    f"ipv6 address {ini.iosv_0.g0_0.global_ipv6_addr}/{ini.iosv_1.g0_0.prefixlen}",
    f"no shutdown",
  ],
])

iosv_1.execs([
  [
    f"ipv6 unicast-routing",
  ],
  [
    f"interface {ini.iosv_1.g0_0.name}",
    f"ipv6 address {ini.iosv_1.g0_0.link_local_ipv6_addr} link-local",
    f"ipv6 address {ini.iosv_1.g0_0.global_ipv6_addr}/{ini.iosv_1.g0_0.prefixlen}",
    f"no shutdown",
  ],
  [
    f"interface {ini.iosv_1.g0_1.name}",
    f"ipv6 address {ini.iosv_1.g0_1.link_local_ipv6_addr} link-local",
    f"ipv6 address {ini.iosv_1.g0_1.global_ipv6_addr}/{ini.iosv_1.g0_0.prefixlen}",
    f"no shutdown",
  ],
])

iosv_2.execs([
  [
    f"ipv6 unicast-routing",
  ],
  [
    f"interface {ini.iosv_2.g0_0.name}",
    f"ipv6 address {ini.iosv_2.g0_0.link_local_ipv6_addr} link-local",
    f"ipv6 address {ini.iosv_2.g0_0.global_ipv6_addr}/{ini.iosv_1.g0_0.prefixlen}",
    f"no shutdown",
  ],
])

# static route setttings
network0 = ipv6.get_network0(ini.iosv_2.g0_0.global_ipv6_addr, ini.iosv_2.g0_0.prefixlen)
iosv_0.execs([
  [
    f"ipv6 route {network0}/{ini.iosv_2.g0_0.prefixlen} {ini.iosv_1.g0_0.global_ipv6_addr}",
    f"ipv6 route ::/0 {ini.iosv_1.g0_0.global_ipv6_addr}"
  ],
])

network0 = ipv6.get_network0(ini.iosv_0.g0_0.global_ipv6_addr, ini.iosv_0.g0_0.prefixlen)
iosv_2.execs([
  [
    f"ipv6 route {network0}/{ini.iosv_0.g0_0.prefixlen} {ini.iosv_1.g0_1.global_ipv6_addr}"
  ],
])

iosv_0.execs([
  f"show ipv6 route",
])

show.router_ping(iosv_0, ini.iosv_2.g0_0.global_ipv6_addr)
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

print("####### exec #######")

# interface up
iosv_0.execs([
  [
    f"ipv6 unicast-routing",
  ],
  [
    f"interface {ini.iosv_0.g0_0.name}",
    f"ipv6 address {ini.iosv_0.g0_0.link_local_ipv6_addr} link-local",
    f"ipv6 address {ini.iosv_0.g0_0.global_ipv6_addr}/{ini.iosv_0.g0_0.prefix_length}",
    f"no shutdown",
  ]
])

iosv_1.execs([
  [
    f"ipv6 unicast-routing",
  ],
  [
    f"interface {ini.iosv_1.g0_0.name}",
    # stateless auto
    f"ipv6 address autoconfig",
    f"no shutdown",
  ],
])


iosv_0.execs([
  f"show ipv6 interface {ini.iosv_0.g0_0.name}",
  #f"ping ipv6 "
])

iosv_1.execs([
  f"show ipv6 interface {ini.iosv_1.g0_0.name}",
])

# check ping
global_ipv6 = show.get_global_ipv6(iosv_1, ini.iosv_1.g0_0.name)
link_layer_ipv6 = show.get_link_layer_ipv6(iosv_1, ini.iosv_1.g0_0.name)
print(f"global: {global_ipv6}, link_layer: {link_layer_ipv6}")
iosv_0.execs([
  f"ping ipv6 {global_ipv6}",
  # interactive "Output interface", so disable
  # f"ping ipv6 {link_layer_ipv6}", 
])
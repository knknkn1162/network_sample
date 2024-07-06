

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


cml0 = Cml()
#pcap01 = Pcap(cml0, ini.iosv_0.__name__, ini.iosv_1.__name__)
#pcap12 = Pcap(cml0, ini.iosv_1.__name__, ini.iosv_2.__name__)


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
])

iosv_2.execs([
  [
    f"interface {ini.iosv_2.g0_0.name}",
    f"ip addr {ini.iosv_2.g0_0.ip_addr} {ini.iosv_2.g0_0.subnet_mask}",
    f"no shutdown",
  ],
])

# bgp settings
#pcap01.start(maxpackets=500)
#pcap12.start(maxpackets=500)
loopback0_network0 = ipv4.get_network0(ini.iosv_0.loopback0.ip_addr, ini.iosv_0.loopback0.subnet_mask)
iosv_0.execs([
  [
    f"router bgp {ini.iosv_0.as_num}",
    f"no auto-summary",
    f"no synchronization",
    # eBGP
    f"neighbor {ini.iosv_1.g0_0.ip_addr} remote-as {ini.iosv_1.as_num}",
    #advertise
    f"network {loopback0_network0} mask {ini.iosv_0.loopback0.subnet_mask}",
  ],
])

iosv_1.execs([
  [
    f"router bgp {ini.iosv_1.as_num}",
    f"no auto-summary",
    f"no synchronization",
    # eBGP
    f"neighbor {ini.iosv_0.g0_0.ip_addr} remote-as {ini.iosv_0.as_num}",
    f"neighbor {ini.iosv_2.g0_0.ip_addr} remote-as {ini.iosv_2.as_num}",
  ],
])

loopback0_network0 = ipv4.get_network0(ini.iosv_2.loopback0.ip_addr, ini.iosv_2.loopback0.subnet_mask)
iosv_2.execs([
  [
    f"router bgp {ini.iosv_2.as_num}",
    f"no auto-summary",
    f"no synchronization",
    # eBGP
    f"neighbor {ini.iosv_1.g0_1.ip_addr} remote-as {ini.iosv_1.as_num}",
    #advertise
    f"network {loopback0_network0} mask {ini.iosv_2.loopback0.subnet_mask}",
  ],
])

wait_until.seconds(30)

for dev in [iosv_0, iosv_1, iosv_2]:
  dev.execs([
    # bgp table
    f"show ip bgp",
    f"show ip bgp detail",
    f"show ip bgp summary",
    f"show ip route bgp",
    f"show ip bgp neighbors",
    f"show ip bgp neighbors | include BGP state",
  ])


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
#pcap01 = Pcap(cml0, ini.ospf0.iosv_0.__name__, ini.bgp0.iosv_1.__name__)
#pcap12 = Pcap(cml0, ini.bgp0.iosv_1.__name__, ini.bgp0.iosv_2.__name__)


print("####### exec #######")

# interface up
as01_network0 = ipv4.get_network0(ini.bgp0.iosv_1.g0_1.ip_addr, ini.bgp0.iosv_1.g0_1.subnet_mask)
iosv_0.execs([
  [
    f"interface {ini.ospf0.iosv_0.g0_0.name}",
    f"ip addr {ini.ospf0.iosv_0.g0_0.ip_addr} {ini.ospf0.iosv_0.g0_0.subnet_mask}",
    f"no shutdown",
  ],
  [
    f"interface {ini.ospf0.iosv_0.loopback0.name}",
    f"ip addr {ini.ospf0.iosv_0.loopback0.ip_addr} {ini.ospf0.iosv_0.loopback0.subnet_mask}",
    #f"no shutdown",
  ],
  [
    f"interface {ini.ospf0.iosv_0.loopback1.name}",
    f"ip addr {ini.ospf0.iosv_0.loopback1.ip_addr} {ini.ospf0.iosv_0.loopback1.subnet_mask}",
    #f"no shutdown",
  ],
  [
    f"interface {ini.ospf0.iosv_0.loopback2.name}",
    f"ip addr {ini.ospf0.iosv_0.loopback2.ip_addr} {ini.ospf0.iosv_0.loopback2.subnet_mask}",
    #f"no shutdown",
  ],
])

iosv_1.execs([
  [
    f"interface {ini.ospf0.iosv_1.g0_0.name}",
    f"ip addr {ini.ospf0.iosv_1.g0_0.ip_addr} {ini.ospf0.iosv_1.g0_0.subnet_mask}",
    f"no shutdown",
  ],
  [
    f"interface {ini.bgp0.iosv_1.g0_1.name}",
    f"ip addr {ini.bgp0.iosv_1.g0_1.ip_addr} {ini.bgp0.iosv_1.g0_1.subnet_mask}",
    f"no shutdown",
  ],
])

iosv_2.execs([
  [
    f"interface {ini.bgp0.iosv_2.g0_0.name}",
    f"ip addr {ini.bgp0.iosv_2.g0_0.ip_addr} {ini.bgp0.iosv_2.g0_0.subnet_mask}",
    f"no shutdown",
  ],
  [
    f"ip route 0.0.0.0 0.0.0.0 {ini.bgp0.iosv_1.g0_1.ip_addr}"
  ],
])

# bgp settings
#pcap01.start(maxpackets=500)
#pcap12.start(maxpackets=500)

g0_0_network0 = ipv4.get_network0(ini.ospf0.iosv_0.g0_0.ip_addr, ini.ospf0.iosv_0.g0_0.subnet_mask)
area_num = 0 
iosv_0.execs([
  [
    f"router ospf {ini.ospf0.num}",
    f"network {g0_0_network0} {ini.INVERSE_MASK_24} area {area_num}",
    f"network {ini.ospf0.iosv_0.loopback0.ip_addr} {ini.INVERSE_MASK_32} area {area_num}",
    f"network {ini.ospf0.iosv_0.loopback1.ip_addr} {ini.INVERSE_MASK_32} area {area_num}",
    f"network {ini.ospf0.iosv_0.loopback2.ip_addr} {ini.INVERSE_MASK_32} area {area_num}",
  ],
])

g0_0_network0 = ipv4.get_network0(ini.ospf0.iosv_1.g0_0.ip_addr, ini.ospf0.iosv_1.g0_0.subnet_mask)
iosv_1.execs([
  [
    f"router ospf {ini.ospf0.num}",
    f"network {g0_0_network0} {ini.INVERSE_MASK_24} area {area_num}",
  ],
  [
    f"router bgp {ini.bgp0.as_num}",
    f"no auto-summary",
    f"no synchronization",
    f"neighbor {ini.bgp0.iosv_2.g0_0.ip_addr} remote-as {ini.bgp0.as_num}",
    f"redistribute ospf {ini.ospf0.num}",
  ]
])

iosv_2.execs([
  [
    f"router bgp {ini.bgp0.as_num}",
    f"no auto-summary",
    f"no synchronization",
    f"neighbor {ini.bgp0.iosv_1.g0_1.ip_addr} remote-as {ini.bgp0.as_num}",
    f"redistribute ospf {ini.ospf0.num}",
  ]
])

wait_until.populate_router_ping(iosv_2, ini.ospf0.iosv_0.loopback0.ip_addr)
wait_until.populate_router_ping(iosv_2, ini.ospf0.iosv_0.loopback1.ip_addr)
wait_until.populate_router_ping(iosv_2, ini.ospf0.iosv_0.loopback2.ip_addr)

iosv_1.execs([
  # bgp table
  f"show ip ospf neighbor",
  f"show ip bgp summaryr"
])

iosv_2.execs([
  f"show ip bgp",
])

# route summary
loopback0_network0 = ipv4.get_network0(ini.ospf0.iosv_0.loopback0.ip_addr, ini.loopback_sumamry_mask)
iosv_1.execs([
  [
    f"router bgp {ini.bgp0.as_num}",
    f"aggregate-address {loopback0_network0} {ini.loopback_sumamry_mask} summary-only"
  ]
])

wait_until.seconds(30)
iosv_2.execs([
  f"show ip bgp"
])
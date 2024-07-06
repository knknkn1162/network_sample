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
iosv_0.execs([
  [
    f"interface {ini.iosv_0.g0_0.name}",
    f"ip addr {ini.iosv_0.g0_0.ip_addr} {ini.iosv_0.g0_0.subnet_mask}",
    f"no shutdown",
  ],
  [
    f"interface {ini.iosv_0.loopback0.name}",
    f"ip addr {ini.iosv_0.loopback0.ip_addr} {ini.iosv_0.loopback0.subnet_mask}",
    #f"no shutdown",
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
  [
    f"interface {ini.iosv_1.loopback0.name}",
    f"ip addr {ini.iosv_1.loopback0.ip_addr} {ini.iosv_1.loopback0.subnet_mask}",
    #f"no shutdown",
  ],
])

iosv_2.execs([
  [
    f"interface {ini.iosv_2.g0_0.name}",
    f"ip addr {ini.iosv_2.g0_0.ip_addr} {ini.iosv_2.g0_0.subnet_mask}",
    f"no shutdown",
  ],
  [
    f"interface {ini.iosv_2.loopback0.name}",
    f"ip addr {ini.iosv_2.loopback0.ip_addr} {ini.iosv_2.loopback0.subnet_mask}",
    #f"no shutdown",
  ],
])

show.mac_ip(iosv_0)
show.mac_ip(iosv_1)
show.mac_ip(iosv_2)

# bgp and ospf
## ospf settings
g0_0_network0 = ipv4.get_network0(ini.iosv_0.g0_0.ip_addr, ini.iosv_0.g0_0.subnet_mask)
area_num = 0
iosv_0.execs([
  [
    f"router ospf {ini.ospf_num}",
    f"network {g0_0_network0} {ini.INVERSE_MASK_24} area {area_num}",
    f"network {ini.iosv_0.loopback0.ip_addr} {ini.INVERSE_MASK_32} area {area_num}",
  ],
])

g0_0_network0 = ipv4.get_network0(ini.iosv_1.g0_0.ip_addr, ini.iosv_1.g0_0.subnet_mask)
g0_1_network0 = ipv4.get_network0(ini.iosv_1.g0_1.ip_addr, ini.iosv_1.g0_1.subnet_mask)
iosv_1.execs([
  [
    f"router ospf {ini.ospf_num}",
    f"network {g0_0_network0} {ini.INVERSE_MASK_24} area {area_num}",
    f"network {g0_1_network0} {ini.INVERSE_MASK_24} area {area_num}",
  ],
])

g0_0_network0 = ipv4.get_network0(ini.iosv_2.g0_0.ip_addr, ini.iosv_2.g0_0.subnet_mask)
iosv_2.execs([
  [
    f"router ospf {ini.ospf_num}",
    f"network {g0_0_network0} {ini.INVERSE_MASK_24} area {area_num}",
    f"network {ini.iosv_2.loopback0.ip_addr} {ini.INVERSE_MASK_32} area {area_num}",
  ],
])

wait_until.populate_ospf(iosv_0, count=2)
wait_until.populate_ospf(iosv_1, count=2)
wait_until.populate_ospf(iosv_2, count=2)

## bgp settings
iosv_0.execs([
  [
    f"router bgp {ini.bgp_num}",
    f"neighbor {ini.iosv_2.loopback0.ip_addr} remote-as {ini.bgp_num}",
    f"neighbor {ini.iosv_2.loopback0.ip_addr} update-source {ini.iosv_0.loopback0.name}",
  ],
])

iosv_2.execs([
  [
    f"router bgp {ini.bgp_num}",
    # logically fullmesh
    f"neighbor {ini.iosv_0.loopback0.ip_addr} remote-as {ini.bgp_num}",
    f"neighbor {ini.iosv_0.loopback0.ip_addr} update-source {ini.iosv_2.loopback0.name}",
  ],
])

wait_until.seconds(30)

for dev in [iosv_0, iosv_1, iosv_2]:
  dev.execs([
    f"show ip route",
    # bgp table
    f"show ip bgp",
    f"show ip bgp detail",
    f"show ip bgp summary",
    f"show ip route bgp",
    f"show ip bgp neighbors",
    f"show ip bgp neighbors | include BGP state",
  ])


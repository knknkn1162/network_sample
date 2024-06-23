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
pcap01 = Pcap(cml0, ini.bgp0.iosv_0.__name__, ini.bgp0.iosv_1.__name__)
pcap12 = Pcap(cml0, ini.bgp0.iosv_1.__name__, ini.bgp1.iosv_2.__name__)


print("####### exec #######")

# interface up
as01_network0 = ipv4.get_network0(ini.bgp0.iosv_1.g0_1.ip_addr, ini.bgp0.iosv_1.g0_1.subnet_mask)
iosv_0.execs([
  [
    f"interface {ini.bgp0.iosv_0.g0_0.name}",
    f"ip addr {ini.bgp0.iosv_0.g0_0.ip_addr} {ini.bgp0.iosv_0.g0_0.subnet_mask}",
    f"no shutdown",
  ],
  [
    # addr subnet_mask next_hop
    f"ip route {as01_network0} {ini.bgp0.iosv_1.g0_1.subnet_mask} {ini.bgp0.iosv_1.g0_0.ip_addr}"
  ]
])

iosv_1.execs([
  [
    f"interface {ini.bgp0.iosv_1.g0_0.name}",
    f"ip addr {ini.bgp0.iosv_1.g0_0.ip_addr} {ini.bgp0.iosv_1.g0_0.subnet_mask}",
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
    f"interface {ini.bgp1.iosv_2.g0_0.name}",
    f"ip addr {ini.bgp1.iosv_2.g0_0.ip_addr} {ini.bgp1.iosv_2.g0_0.subnet_mask}",
    f"no shutdown",
  ],
  [
    f"interface {ini.bgp1.iosv_2.loopback0.name}",
    f"ip addr {ini.bgp1.iosv_2.loopback0.ip_addr} {ini.bgp1.iosv_2.loopback0.subnet_mask}",
    #f"no shutdown",
  ],
  [
    f"ip route 0.0.0.0 0.0.0.0 {ini.bgp0.iosv_1.g0_1.ip_addr}"
  ],
])

# bgp settings
pcap01.start(maxpackets=500)
pcap12.start(maxpackets=500)

g0_1_network0 = ipv4.get_network0(ini.bgp0.iosv_1.g0_1.ip_addr, ini.bgp0.iosv_1.g0_1.subnet_mask)
iosv_0.execs([
  [
    f"router bgp {ini.bgp0.as_num}",
    f"no auto-summary",
    # no sync by default
    f"no synchronization",
    # iBGP
    f"neighbor {ini.bgp0.iosv_1.g0_0.ip_addr} remote-as {ini.bgp0.as_num}",
  ]
])

iosv_1.execs([
  [
    f"router bgp {ini.bgp0.as_num}",
    f"no auto-summary",
    # no sync by default
    f"no synchronization",
    # iBGP
    f"neighbor {ini.bgp0.iosv_0.g0_0.ip_addr} remote-as {ini.bgp0.as_num}",
    # eBGP
    f"neighbor {ini.bgp1.iosv_2.g0_0.ip_addr} remote-as {ini.bgp1.as_num}",
  ]
])

iosv_2.execs([
  [
    f"router bgp {ini.bgp1.as_num}",
    f"no auto-summary",
    # no sync by default
    f"no synchronization",
    # eBGP
    f"neighbor {ini.bgp0.iosv_1.g0_1.ip_addr} remote-as {ini.bgp0.as_num}",
    # advertize loopback(自分のAS内のルート情報をBGPルートとしてアドバタイズしたい)
    f"network {ini.bgp1.iosv_2.loopback0.ip_addr} mask {ini.SUBNET_MASK_32}",
  ]
])

wait_until.seconds(20)
iosv_0.execs([
  # bgp table
  f"show ip bgp",
  f"show ip bgp summary",
  f"show ip route bgp",
])

pcap01.stop(); pcap01.download(file=ini.pcap01_file)
pcap12.stop(); pcap12.download(file=ini.pcap12_file)

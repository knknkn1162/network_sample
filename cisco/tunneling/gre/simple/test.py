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
pcap = Pcap(cml0, ini.iosv_0.__name__, ini.iosv_1.__name__)

print("####### exec #######")

# interface up
iosv_0.execs([
  [
    f"interface {ini.iosv_0.g0_0.name}",
    f"ip addr {ini.iosv_0.g0_0.ip_addr} {ini.iosv_0.g0_0.subnet_mask}",
    f"no shutdown",
  ],
  [
    f"ip route 0.0.0.0 0.0.0.0 {ini.iosv_1.g0_0.ip_addr}",
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
  [
    f"ip route 0.0.0.0 0.0.0.0 {ini.iosv_1.g0_1.ip_addr}",
  ],
])
pcap.start(maxpackets=500)

iosv_0.execs([
  [
    f"interface {ini.tunnel0.name}",
    f"ip address {ini.tunnel0.v0.ip_addr} {ini.tunnel0.v0.subnet_mask}",
    # Note that routing exists between source_ip <-> dest_ip
    f"tunnel source {ini.tunnel0.v0.interface.ip_addr}",
    f"tunnel destination {ini.tunnel0.v1.interface.ip_addr}",
    #f"tunnel mode gre ip",
  ]
])

iosv_2.execs([
  [
    f"interface {ini.tunnel0.name}",
    f"ip address {ini.tunnel0.v1.ip_addr} {ini.tunnel0.v1.subnet_mask}",
    f"tunnel source {ini.tunnel0.v1.interface.ip_addr}",
    f"tunnel destination {ini.tunnel0.v0.interface.ip_addr}",
    #f"tunnel mode gre ip",
  ]
])

# ospf settings
tunnel0_v0_network0 = ipv4.get_network0(ini.tunnel0.v0.ip_addr, ini.tunnel0.v0.subnet_mask)
area_id = 0
iosv_0.execs([
  [
    f"router ospf {ini.ospf_id}",
    f"network {tunnel0_v0_network0} {ini.INVERSE_MASK_24} area {area_id}",
  ],
])

tunnel0_v1_network0 = ipv4.get_network0(ini.tunnel0.v1.ip_addr, ini.tunnel0.v1.subnet_mask)

iosv_2.execs([
  [
    f"router ospf {ini.ospf_id}",
    f"network {tunnel0_v1_network0} {ini.INVERSE_MASK_24} area {area_id}",
  ],
])

wait_until.seconds(10)

iosv_0.execs([
  "show ip ospf neighbor",
])

iosv_1.execs([
  "show ip ospf neighbor",
])

iosv_2.execs([
  "show ip ospf neighbor",
])

iosv_0.execs([
  f"show interfaces {ini.tunnel0.name}",
])

iosv_2.execs([
  f"show interfaces {ini.tunnel0.name}",
])

wait_until.populate_router_ping(iosv_0, ini.tunnel0.v1.ip_addr)
pcap.stop(); pcap.download(file=ini.pcap_file)

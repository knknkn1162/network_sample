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

server_0 = Device(tb, 'server_0')
server_1 = Device(tb, 'server_1')

cml0 = Cml()
#pcap01 = Pcap(cml0, ini.iosv_0.__name__, ini.iosv_1.__name__)

print("####### exec #######")

# server ip settings
server_0.execs([
  # eth0 setting
  ## disable DHCP
  f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
  f"sudo ifconfig eth0 {ini.server_0.eth0.ip_addr} netmask {ini.server_0.eth0.subnet_mask} up",
  f"sudo route add default gw {ini.server_0.eth0.default_gw}",
  f"ifconfig eth0",
  f"route -e",
])

server_1.execs([
  # eth0 setting
  ## disable DHCP
  f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
  f"sudo ifconfig eth0 {ini.server_1.eth0.ip_addr} netmask {ini.server_1.eth0.subnet_mask} up",
  f"sudo route add default gw {ini.server_1.eth0.default_gw}",
  f"ifconfig eth0",
  f"route -e",
])

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


show.mac_ip(iosv_0)
show.mac_ip(iosv_1)
show.mac_ip(iosv_2)

# EIGRP settings @ iosv_0, iosv_1
g0_0_network0 = ipv4.get_network0(ini.iosv_0.g0_0.ip_addr, ini.iosv_0.g0_0.subnet_mask)
g0_1_network0 = ipv4.get_network0(ini.iosv_0.g0_1.ip_addr, ini.iosv_0.g0_1.subnet_mask)
iosv_0.execs([
  [
    f"router eigrp {ini.eigrp_num}",
    f"network {g0_0_network0} {ini.INVERSE_MASK_24}",
    f"network {g0_1_network0} {ini.INVERSE_MASK_24}",
    f"no auto-summary",
    f"passive-interface {ini.iosv_0.g0_0.name}",
  ],
])

g0_0_network0 = ipv4.get_network0(ini.iosv_1.g0_0.ip_addr, ini.iosv_1.g0_0.subnet_mask)
iosv_1.execs([
  [
    f"router eigrp {ini.eigrp_num}",
    f"network {g0_0_network0} {ini.INVERSE_MASK_24}",
    f"no auto-summary",
  ],
])

# RIPv2 settings
g0_1_network0 = ipv4.get_network0(ini.iosv_1.g0_1.ip_addr, ini.iosv_1.g0_1.subnet_mask)
iosv_1.execs([
  [
    f"router rip",
    f"version 2",
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
    f"passive-interface {ini.iosv_2.g0_1.name}",
  ],
])

# check
wait_until.populate_server_ping(server_0, ini.iosv_1.g0_0.ip_addr)
wait_until.populate_server_ping(server_1, ini.iosv_1.g0_1.ip_addr)
show.server_ping(server_0, ini.server_1.eth0.ip_addr, count=10)

wait_until.populate_eigrp(iosv_0, ini.eigrp_num, 0)
wait_until.populate_eigrp(iosv_1, ini.eigrp_num, 1)
wait_until.populate_rip(iosv_1, 1)
wait_until.populate_rip(iosv_2, 0)

# check
iosv_0.execs([
  f"show ip route",
])
iosv_1.execs([
  f"show ip route",
])
iosv_2.execs([
  f"show ip route",
])

# redistribute
iosv_1.execs([
  [
    f"router rip",
    f"redistribute eigrp {ini.eigrp_num} metric 1",
  ],
  [
    f"router eigrp {ini.eigrp_num}",
    # 帯域幅, 遅延、信頼性、負荷、MTU
    f"redistribute rip metric 100000 10 255 1 1500"
  ]
])

wait_until.populate_server_ping(server_0, ini.server_1.eth0.ip_addr)
wait_until.populate_eigrp(iosv_0, ini.eigrp_num, 2)
wait_until.populate_eigrp(iosv_1, ini.eigrp_num, 1)
wait_until.populate_rip(iosv_1, 1)
wait_until.populate_rip(iosv_2, 2)

# check
iosv_0.execs([
  f"show ip route",
])
iosv_1.execs([
  f"show ip route",
])
iosv_2.execs([
  f"show ip route",
])
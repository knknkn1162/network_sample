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
#iosvl2_0 = Device(tb, 'iosvl2_0')

cml0 = Cml()

print("####### exec #######")

# server setup
server_0.execs([
  # eth0 setting
  ## disable DHCP
  f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
  f"sudo ifconfig eth0 {ini.server_0.eth0.ip_addr} netmask {ini.server_0.eth0.subnet_mask} up",
  f"sudo route add default gw {ini.hsrp0.virtual_ip_addr}",
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
  [
    f"interface {ini.iosv_2.loopback0.name}",
    f"ip addr {ini.iosv_2.loopback0.ip_addr} {ini.iosv_2.loopback0.subnet_mask}",
    #f"no shutdown",
  ],
])

show.mac_ip(iosv_0)
show.mac_ip(iosv_1)
show.mac_ip(iosv_2)

# routing(RIP)
g0_0_network0 = ipv4.get_network0(ini.iosv_0.g0_0.ip_addr, ini.iosv_0.g0_0.subnet_mask)
g0_1_network0 = ipv4.get_network0(ini.iosv_0.g0_1.ip_addr, ini.iosv_0.g0_1.subnet_mask)
iosv_0.execs([
  [
    f"router rip",
    f"version 2",
    f"network {g0_0_network0}",
    f"network {g0_1_network0}",
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
loopback0_network0 = ipv4.get_network0(ini.iosv_2.loopback0.ip_addr, ini.iosv_2.loopback0.subnet_mask)
iosv_2.execs([
  [
    f"router rip",
    f"version 2",
    f"network {g0_0_network0}",
    f"network {g0_1_network0}",
    f"network {loopback0_network0}",
    f"no auto-summary",
  ],
])

# HSRP setting
iosv_0.execs([
  [
    f"track {ini.hsrp0.track_num} interface {ini.iosv_0.g0_1.name} line-protocol"
  ],
  [
    f"interface {ini.iosv_0.g0_0.name}",
    f"standby {ini.hsrp0.group_id} ip {ini.hsrp0.virtual_ip_addr}",
    f"standby {ini.hsrp0.group_id} priority {ini.iosv_0.g0_0.hsrp_priority}",
    # 設定後や起動時の時差がある場合でも、プライオリティ値が高いデバイスが必ずアクティブルータとなるようにできる機能
    f"standby {ini.hsrp0.group_id} preempt",
    # interface tracking
    f"standby {ini.hsrp0.group_id} track {ini.hsrp0.track_num} decrement {ini.iosv_0.g0_1.hsrp_penalty}",
  ],
])

iosv_1.execs([
  [
    f"track {ini.hsrp0.track_num} interface {ini.iosv_1.g0_1.name} line-protocol"
  ],
  [
    f"interface {ini.iosv_0.g0_0.name}",
    f"standby {ini.hsrp0.group_id} ip {ini.hsrp0.virtual_ip_addr}",
    f"standby {ini.hsrp0.group_id} priority {ini.iosv_1.g0_0.hsrp_priority}",
    f"standby {ini.hsrp0.group_id} preempt",
    f"standby {ini.hsrp0.group_id} track {ini.hsrp0.track_num} decrement {ini.iosv_1.g0_1.hsrp_penalty}"
  ],
])

wait_until.populate_server_ping(server_0, ini.iosv_2.loopback0.ip_addr)

iosv_0.execs([
  f"show standby brief",
  f"show standby",
  f"show standby all",
])

iosv_1.execs([
  f"show standby brief",
  f"show standby",
  f"show standby all",
])

server_0.execs([
  f"arp -a",
])

# down for test
iosv_0.execs([
  [
    f"interface {ini.iosv_0.g0_1.name}",
    f"shutdown",
  ],
])

wait_until.populate_server_ping(server_0, ini.iosv_2.loopback0.ip_addr)

iosv_0.execs([
  f"show standby brief",
])

iosv_1.execs([
  f"show standby brief",
])
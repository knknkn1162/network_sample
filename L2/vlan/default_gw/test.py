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
iosvl2_0 = Device(tb, 'iosvl2_0')

server_0 = Device(tb, 'server_0')
server_1 = Device(tb, 'server_1')

cml0 = Cml()
print("####### exec #######")

# server settings -> DHCP enable by default
server_0.execs([
  # eth0 setting
  ## disable DHCP
  f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
  f"sudo ifconfig eth0 {ini.server_0.eth0.ip_addr} netmask {ini.server_0.eth0.subnet_mask} up",
  f"sudo route add default gw {ini.iosv_0.g0_0.ip_addr}",
  f"ifconfig eth0",
  f"route -e",
])
# interface up
server_1.execs([
  # eth0 setting
  ## disable DHCP
  f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
  f"sudo ifconfig eth0 {ini.server_1.eth0.ip_addr} netmask {ini.server_1.eth0.subnet_mask} up",
  f"sudo route add default gw {ini.iosv_0.g0_1.ip_addr}",
  f"ifconfig eth0",
  f"route -e",
])

# interface up
iosv_0.execs([
  [
    f"interface {ini.iosv_0.g0_0.name}",
    f"ip addr {ini.iosv_0.g0_0.ip_addr} {ini.iosv_0.g0_0.subnet_mask}",
    f"no shutdown"
  ],
  [
    f"interface {ini.iosv_0.g0_1.name}",
    f"ip addr {ini.iosv_0.g0_1.ip_addr} {ini.iosv_0.g0_1.subnet_mask}",
    f"no shutdown"
  ],
])

iosvl2_0.execs([
  [
    f"interface {ini.iosvl2_0.vlan1}",
    f"ip address {ini.iosvl2_0.vlan1.ip_addr} {ini.iosvl2_0.vlan1.subnet_mask}",
    f"no shutdown"
  ]
])

wait_until.populate_up(iosv_0, 2)

show.server_ping(server_0, ini.server_1.eth0.ip_addr)

iosvl2_0.execs([
  [
    f"ip default-gateway {ini.iosv_0.g0_0.ip_addr}",
  ]
])
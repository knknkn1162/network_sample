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

iosvl2_0 = Device(tb, 'iosvl2_0')

server_0 = Device(tb, 'server_0')
server_1 = Device(tb, 'server_1')
server_2 = Device(tb, 'server_2')
server_3 = Device(tb, 'server_3')

cml0 = Cml()
print("####### exec #######")

# server settings -> DHCP enable by default
server_0.execs([
  # eth0 setting
  ## disable DHCP
  f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
  f"sudo ifconfig eth0 {ini.server_0.eth0.ip_addr} netmask {ini.server_0.eth0.subnet_mask} up",
  f"ifconfig eth0",
])

server_1.execs([
  # eth0 setting
  ## disable DHCP
  f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
  f"sudo ifconfig eth0 {ini.server_1.eth0.ip_addr} netmask {ini.server_1.eth0.subnet_mask} up",
  f"ifconfig eth0",
])

server_2.execs([
  # eth0 setting
  ## disable DHCP
  f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
  f"sudo ifconfig eth0 {ini.server_2.eth0.ip_addr} netmask {ini.server_2.eth0.subnet_mask} up",
  f"ifconfig eth0",
])

server_3.execs([
  # eth0 setting
  ## disable DHCP
  f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
  f"sudo ifconfig eth0 {ini.server_3.eth0.ip_addr} netmask {ini.server_3.eth0.subnet_mask} up",
  f"ifconfig eth0",
])

# set access port
iosvl2_0.execs([
  [
    f"vlan {ini.vlan1.num}",
    f"name {ini.vlan1.name}",
  ],
  [
    f"vlan {ini.vlan2.num}",
    f"name {ini.vlan2.name}",
  ]
])

iosvl2_0.execs([
  [
    f"interface {ini.iosvl2_0.g0_0.name}",
    f"switchport mode access",
    f"switchport access vlan {ini.iosvl2_0.g0_0.vlan.num}"
  ],
  [
    f"interface {ini.iosvl2_0.g0_1.name}",
    f"switchport mode access",
    f"switchport access vlan {ini.iosvl2_0.g0_1.vlan.num}"
  ],
  [
    f"interface {ini.iosvl2_0.g0_2.name}",
    f"switchport mode access",
    f"switchport access vlan {ini.iosvl2_0.g0_2.vlan.num}"
  ],
  [
    f"interface {ini.iosvl2_0.g0_3.name}",
    f"switchport mode access",
    f"switchport access vlan {ini.iosvl2_0.g0_3.vlan.num}"
  ],
])

wait_until.seconds(5)
iosvl2_0.execs([
  f"show vlan",
  f"show vlan brief",
  f"show vlan id {ini.vlan1.num}",
  f"show interfaces {ini.iosvl2_0.g0_0.name} switchport",
  f"show interfaces trunk",
  f"show interfaces status",
  #f"show mac address-table",
  # check there is no "vlan.dat" in iosvl2
  f"show flash:",
])

# test
wait_until.populate_server_ping(server_0, ini.server_2.eth0.ip_addr)
wait_until.populate_server_ping(server_1, ini.server_3.eth0.ip_addr)
# it should not work
show.server_ping(server_0, ini.server_1.eth0.ip_addr)
show.server_ping(server_2, ini.server_3.eth0.ip_addr)
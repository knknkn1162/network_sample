from genie import testbed
import cml
from lib.device import Device
import ini
import time

tb = testbed.load(cml.CONFIG_YAML)

# tinylinux
server_1 = Device(tb, 'server_1')
server_2 = Device(tb, 'server_2')
server_3 = Device(tb, 'server_3')
server_4 = Device(tb, 'server_4')
# switch
iosvl2_1 = Device(tb, 'iosvl2_1')
iosvl2_2 = Device(tb, 'iosvl2_2')

print("####### exec #######")
server_1.execs([
  # disable DHCP
  f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
  # eth0 setting
  f"sudo ifconfig eth0 {ini.server_1.eth0.ip_addr} netmask {ini.server_1.eth0.subnet_mask} up",
  f"ifconfig eth0"
])
server_2.execs([
  # disable DHCP
  f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
  # eth0 setting
  f"sudo ifconfig eth0 {ini.server_2.eth0.ip_addr} netmask {ini.server_2.eth0.subnet_mask} up",
  f"ifconfig eth0"
])
server_3.execs([
  # disable DHCP
  f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
  # eth0 setting
  f"sudo ifconfig eth0 {ini.server_3.eth0.ip_addr} netmask {ini.server_3.eth0.subnet_mask} up",
  f"ifconfig eth0"
])
server_4.execs([
  # disable DHCP
  f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
  # eth0 setting
  f"sudo ifconfig eth0 {ini.server_4.eth0.ip_addr} netmask {ini.server_4.eth0.subnet_mask} up",
  f"ifconfig eth0"
])
print("wait for sync....."); time.sleep(5)
vlan_list_str = ','.join(map(str,ini.iosvl2_1.vlan_list))

# DTP
iosvl2_1.execs([
  [
    f"interface {ini.iosvl2_1.g0_0.name}",
    # access
    f"switchport mode dynamic auto",
  ],
  [
    f"interface {ini.iosvl2_1.g0_1.name}",
    # access
    f"switchport mode dynamic auto",
  ],
  [
    f"interface {ini.iosvl2_1.g0_2.name}",
    f"switchport trunk encapsulation dot1q",
    # trunk
    f"switchport mode dynamic desirable"
  ],
])

iosvl2_2.execs([
  [
    f"interface {ini.iosvl2_2.g0_0.name}",
    f"switchport mode dynamic auto",
  ],
  [
    f"interface {ini.iosvl2_2.g0_1.name}",
    f"switchport mode access",
  ],
  [
    f"interface {ini.iosvl2_2.g0_2.name}",
    f"switchport trunk encapsulation dot1q",
    # trunk
    f"switchport mode dynamic desirable"
  ],
])

# set access and dot1q
iosvl2_1.execs([
  [
    f"vlan {vlan_list_str}"
  ],
  [
    f"interface {ini.iosvl2_1.g0_0.name}",
    # 1: default, so we will not use it
    f"switchport access vlan {ini.iosvl2_1.g0_0.vlan}"
  ],
  [
    f"interface {ini.iosvl2_1.g0_1.name}",
    f"switchport access vlan {ini.iosvl2_1.g0_1.vlan}"
  ],
])

iosvl2_2.execs([
  [
    f"vlan {vlan_list_str}"
  ],
  [
    f"interface {ini.iosvl2_2.g0_0.name}",
    f"switchport access vlan {ini.iosvl2_2.g0_0.vlan}"
  ],
  [
    f"interface {ini.iosvl2_2.g0_1.name}",
    f"switchport access vlan {ini.iosvl2_2.g0_1.vlan}"
  ],
])
time.sleep(10)

iosvl2_1.execs([
  f"show vlan",
  f"show vlan brief",
  f"show interfaces {ini.iosvl2_1.g0_0.name} switchport",
  f"show interfaces trunk",
  f"show interfaces status",
  #f"show mac address-table",
])

iosvl2_2.execs([
  f"show vlan",
  f"show vlan brief",
  f"show interfaces {ini.iosvl2_2.g0_0.name} switchport",
  f"show interfaces trunk",
  f"show interfaces status",
  #f"show mac address-table",
])

server_1.execs([
  # it works
  f"ping {ini.server_3.eth0.ip_addr} -c 5",
  # it fails
  f"ping {ini.server_2.eth0.ip_addr} -c 5",
  f"ping {ini.server_4.eth0.ip_addr} -c 5",
])
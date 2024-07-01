from genie import testbed
from cml import CONFIG_YAML, Cml, Pcap
from lib.device import Device
from lib import wait, ipv4
import ini
import time
import wait_until, calc
import show

tb = testbed.load(CONFIG_YAML)

# tinylinux
server_1 = Device(tb, 'server_1')
server_2 = Device(tb, 'server_2')
server_3 = Device(tb, 'server_3')
server_4 = Device(tb, 'server_4')
# switch
iosvl2_1 = Device(tb, 'iosvl2_1')
iosvl2_2 = Device(tb, 'iosvl2_2')

pcap = Pcap(Cml(), ini.iosvl2_1.__name__, ini.iosvl2_2.__name__)


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


# define vlan
iosvl2_1.execs([
  [
    f"vlan {ini.vlan1.num}",
    f"name {ini.vlan1.name}",
  ],
  [
    f"vlan {ini.vlan2.num}",
    f"name {ini.vlan2.name}",
  ]
])

iosvl2_2.execs([
  [
    f"vlan {ini.vlan1.num}",
    f"name {ini.vlan1.name}",
  ],
  [
    f"vlan {ini.vlan2.num}",
    f"name {ini.vlan2.name}",
  ]
])
pcap.start(maxpackets=500)
# set access/trunk port(dot1q)
iosvl2_1.execs([
  [
    f"interface {ini.iosvl2_1.g0_0.name}",
    f"switchport mode access",
    # 1: default, so we will not use it
    f"switchport access vlan {ini.iosvl2_1.g0_0.vlan.num}"
  ],
  [
    f"interface {ini.iosvl2_1.g0_1.name}",
    f"switchport mode access",
    f"switchport access vlan {ini.iosvl2_1.g0_1.vlan.num}"
  ],
  [
    f"interface {ini.iosvl2_1.g0_2.name}",
    f"switchport trunk encapsulation dot1q",
    f"switchport mode trunk"
  ]
])

iosvl2_2.execs([
  [
    f"interface {ini.iosvl2_2.g0_0.name}",
    f"switchport mode access",
    # 1: default, so we will not use it
    f"switchport access vlan {ini.iosvl2_2.g0_0.vlan.num}"
  ],
  [
    f"interface {ini.iosvl2_2.g0_1.name}",
    f"switchport mode access",
    f"switchport access vlan {ini.iosvl2_2.g0_1.vlan.num}"
  ],
  [
    f"interface {ini.iosvl2_2.g0_2.name}",
    f"switchport trunk encapsulation dot1q",
    f"switchport mode trunk"
  ]
])

iosvl2_1.execs([
  f"show vlan",
  f"show vlan brief",
  f"show vlan id {ini.vlan1.num}",
  f"show interfaces {ini.iosvl2_1.g0_0.name} switchport",
  f"show interfaces trunk",
  f"show interfaces status",
  #f"show mac address-table",
])

iosvl2_2.execs([
  f"show vlan",
  f"show vlan brief",
  f"show vlan id {ini.vlan1.num}",
  f"show interfaces {ini.iosvl2_2.g0_0.name} switchport",
  f"show interfaces trunk",
  f"show interfaces status",
  #f"show mac address-table",
])



wait_until.populate_server_ping(server_1, ini.server_3.eth0.ip_addr)
wait_until.populate_server_ping(server_2, ini.server_4.eth0.ip_addr)
# it fails
show.server_ping(server_1, ini.server_2.eth0.ip_addr)
show.server_ping(server_1, ini.server_4.eth0.ip_addr)

pcap.stop(); pcap.download(file=ini.pcap_file)

allowed_only_vlan_num = ini.vlan2.num
iosvl2_1.execs([
  [
    f"interface {ini.iosvl2_1.g0_2.name}",
    f"switchport trunk allowed vlan {allowed_only_vlan_num}",
  ]
])
iosvl2_2.execs([
  [
    f"interface {ini.iosvl2_2.g0_2.name}",
    f"switchport trunk allowed vlan {allowed_only_vlan_num}",
  ]
])

wait_until.seconds(20)
show.server_ping(server_1, ini.server_3.eth0.ip_addr)
wait_until.populate_server_ping(server_2, ini.server_4.eth0.ip_addr)

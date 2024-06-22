from genie import testbed
from cml import CONFIG_YAML, Cml, Pcap
from lib.device import Device
from lib import wait, ipv4
import ini
import time
import wait_until

tb = testbed.load(CONFIG_YAML)

# tinylinux
server_0 = Device(tb, 'server_0')
server_1 = Device(tb, 'server_1')
server_2 = Device(tb, 'server_2')
# switch
iosvl2_0 = Device(tb, 'iosvl2_0')
iosvl2_1 = Device(tb, 'iosvl2_1')
iosvl2_2 = Device(tb, 'iosvl2_2')



print("####### exec #######")

# setup server
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

# switch
## vlan settings
iosvl2_0.execs([
  [
    f"vlan {ini.iosvl2_0.g0_0.vlan.num}",
    f"name {ini.iosvl2_0.g0_0.vlan.name}"
  ],
  [
    f"vlan {ini.iosvl2_0.g0_1.vlan.num}",
    f"name {ini.iosvl2_0.g0_1.vlan.name}"
  ]
])
## switchport settings
iosvl2_0.execs([
  [
    f"interface {ini.iosvl2_0.g0_0.name}",
    f"switchport mode access",
    f"switchport access vlan {ini.iosvl2_0.g0_0.vlan.num}",
    # disable DTP(Dynamic Trunking Protocol)
    # f"switchport nonegotiate",
    f"no shutdown",
  ],
  [
    f"interface {ini.iosvl2_0.g0_1.name}",
    f"switchport mode access",
    f"switchport access vlan {ini.iosvl2_0.g0_1.vlan.num}",
    f"no shutdown",
  ],
  [
    f"interface {ini.iosvl2_0.g0_2.name}",
    f"switchport trunk encapsulation dot1q",
    f"switchport mode trunk",
    f"no shutdown",
  ]
])

vlan_list_str = ','.join(map(str,ini.vlan_list))
## settings on trunk links
iosvl2_1.execs([

  [
    # need to set by hand
    f"vlan {vlan_list_str}",
  ],
  [
    f"interface {ini.iosvl2_1.g0_0.name}",
    f"switchport trunk encapsulation dot1q",
    f"switchport mode trunk",
    f"switchport trunk allowed vlan add {vlan_list_str}",
    f"no shutdown",
  ],
  [
    f"interface {ini.iosvl2_1.g0_1.name}",
    f"switchport trunk encapsulation dot1q",
    f"switchport mode trunk",
    f"switchport trunk allowed vlan add {vlan_list_str}",
    f"no shutdown",
  ],
])

iosvl2_2.execs([
  # no need to create vlan because sync by vtp
  # f"vlan {vlan_list_str}"
  [
    f"interface {ini.iosvl2_2.g0_0.name}",
    f"switchport trunk encapsulation dot1q",
    f"switchport mode trunk",
    f"no shutdown",
  ],
  [
    f"interface {ini.iosvl2_2.g0_1.name}",
    f"switchport mode access",
    # Access VLAN does not exist. Creating vlan 10
    f"switchport access vlan {ini.iosvl2_2.g0_1.vlan.num}",
    f"no shutdown",
  ],
])

# check vlan up
wait_until.populate_vlan(iosvl2_0, 2)
wait_until.populate_vlan(iosvl2_1, 2)
# no advertisement yet
wait_until.populate_vlan(iosvl2_2, 1)


# check vlan
iosvl2_0.execs([
  f"show vlan brief",
  f"show interfaces trunk",
])
iosvl2_1.execs([
  f"show vlan brief",
  f"show interfaces trunk",
])
iosvl2_2.execs([
  f"show vlan brief",
  f"show interfaces trunk",
])

# set vtp
# リビジョン番号を一度 0 にしてからクライアントモードなどに戻して追加することが推奨。VTPモードはトランスペアレントにしておく
# このような問題があることからVTPはあまり利用されません。
pcap = Pcap(Cml(), ini.iosvl2_1.__name__, ini.iosvl2_2.__name__)
pcap.start(maxpackets=2000)
iosvl2_0.execs([
  [
    f"vtp domain {ini.vtp_domain}",
    # advertisement, sync, changeable
    f"vtp mode server",
    # f"vtp pruning disable",
    f"vtp password {ini.vtp_password}",
  ],
])

iosvl2_1.execs([
  [
    f"vtp domain {ini.vtp_domain}",
    # no-advertisement(only transfer), no-sync, changeable
    f"vtp mode transparent",
    f"vtp password {ini.vtp_password}",
  ],
])

iosvl2_2.execs([
  [
    f"vtp domain {ini.vtp_domain}",
    # no-advertisement(only transfer), sync, unchangeable
    # revisionはserver側の変更のない時更新されない(実証より)
    f"vtp mode client",
    f"vtp password {ini.vtp_password}",
  ],
])

# check advertisement in iosvl2_2
wait_until.populate_vlan(iosvl2_2, 2)

# check vlan again
iosvl2_0.execs([
  f"show vtp status",
  f"show vlan brief",
])
iosvl2_1.execs([
  f"show vtp status",
  f"show vlan brief",
])
iosvl2_2.execs([
  f"show vtp status",
  f"show vlan brief",
])

wait_until.seconds(350)
pcap.stop()

# show be worked
wait_until.server_ping(server_0, ini.server_2.eth0.ip_addr, count=5)

pcap.download(ini.pcap_file)
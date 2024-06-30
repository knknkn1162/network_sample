from genie import testbed
from cml import CONFIG_YAML, Cml, Pcap
from lib.device import Device
from lib import wait, ipv4
import ini
import time
import wait_until, calc

tb = testbed.load(CONFIG_YAML)

# tinylinux
server_0 = Device(tb, 'server_0')
server_1 = Device(tb, 'server_1')
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

# switch
## switchport settings
vlan_list_str = ','.join(map(str,ini.vlan_list))
iosvl2_0.execs([
  [
    f"vlan {vlan_list_str}",
  ],
  [
    f"interface {ini.iosvl2_0.g0_0.name}",
    f"switchport trunk encapsulation dot1q",
    f"switchport mode trunk",
    f"no shutdown",
  ],
  [
    f"interface {ini.iosvl2_0.g0_1.name}",
    f"switchport trunk encapsulation dot1q",
    f"switchport mode trunk",
    f"no shutdown",
  ]
])

iosvl2_1.execs([
  [
    f"vlan {vlan_list_str}",
  ],
  [
    f"interface {ini.iosvl2_1.g0_0.name}",
    f"switchport trunk encapsulation dot1q",
    f"switchport mode trunk",
    f"no shutdown",
  ],
  [
    f"interface {ini.iosvl2_1.g0_1.name}",
    f"switchport trunk encapsulation dot1q",
    f"switchport mode trunk",
    f"no shutdown",
  ]
])

iosvl2_2.execs([
  [
    f"vlan {vlan_list_str}",
  ],
  [
    f"interface {ini.iosvl2_2.g0_0.name}",
    f"switchport trunk encapsulation dot1q",
    f"switchport mode trunk",
    f"no shutdown",
  ],
  [
    f"interface {ini.iosvl2_2.g0_1.name}",
    f"switchport trunk encapsulation dot1q",
    f"switchport mode trunk",
    f"no shutdown",
  ],
  [
    f"interface {ini.iosvl2_2.g0_2.name}",
    f"switchport mode access",
    f"switchport access vlan {ini.iosvl2_2.g0_2.vlan.num}",
    f"no shutdown",
  ],
  [
    f"interface {ini.iosvl2_2.g0_3.name}",
    f"switchport mode access",
    f"switchport access vlan {ini.iosvl2_2.g0_3.vlan.num}",
    f"no shutdown",
  ],
])

# check vlan trunk
wait_until.populate_trunk(iosvl2_0, 2)
wait_until.populate_trunk(iosvl2_1, 2)
wait_until.populate_vlan(iosvl2_2, 2)
wait_until.populate_trunk(iosvl2_2, 2)

# spanning tree setting
iosvl2_0.execs([
  [
    f"spanning-tree vlan {ini.vlan_list[0]} priority {ini.iosvl2_0.stp_priority}",
    f"spanning-tree vlan {ini.vlan_list[1]} priority {ini.iosvl2_0.stp_priority}",
  ],
])
iosvl2_1.execs([
  [
    f"spanning-tree vlan {ini.vlan_list[0]} priority {ini.iosvl2_1.stp_priority}",
    f"spanning-tree vlan {ini.vlan_list[1]} priority {ini.iosvl2_1.stp_priority}",
  ],
])
iosvl2_2.execs([
  [
    f"spanning-tree vlan {ini.vlan_list[0]} priority {ini.iosvl2_2.stp_priority}",
    f"spanning-tree vlan {ini.vlan_list[1]} priority {ini.iosvl2_2.stp_priority}",
  ],
  # enable portfast in link(server <-> switch) to make more convergence faster
  [
    f"interface {ini.iosvl2_2.g0_2.name}",
    f"spanning-tree portfast",
  ],
  [
    f"interface {ini.iosvl2_2.g0_2.name}",
    f"spanning-tree portfast",
  ],
])

wait_until.populate_stp_forwarding(iosvl2_0, vlan_num=ini.vlan_list[0], count=2)
wait_until.populate_stp_forwarding(iosvl2_1, vlan_num=ini.vlan_list[0], count=2)
wait_until.populate_stp_forwarding(iosvl2_2, vlan_num=ini.vlan_list[0], count=2)
wait_until.populate_stp_blocking(iosvl2_2, vlan_num=ini.vlan_list[0], count=1)

# https://pubhub.devnetcloud.com/media/genie-feature-browser/docs/#/parsers/show%2520spanning-tree%2520vlan%2520%257Bvlan%257D
iosvl2_0.execs([
  f"show spanning-tree vlan {ini.vlan_list[0]}",
  f"show spanning-tree vlan {ini.vlan_list[1]}",
])
iosvl2_1.execs([
  f"show spanning-tree vlan {ini.vlan_list[0]}",
  f"show spanning-tree vlan {ini.vlan_list[1]}",
])
# g0_1(iosvl2_1 <-> iosvl2_2) is blocked
iosvl2_2.execs([
  f"show spanning-tree vlan {ini.vlan_list[0]}",
  f"show spanning-tree vlan {ini.vlan_list[1]}",
])

# change vlan cost(desg -> Altn)
iosvl2_1.execs([
  [
    f"interface {ini.iosvl2_1.g0_0.name}",
    # decrease cost so that FWD -> BLK
    f"spanning-tree vlan {ini.vlan_list[0]} cost 100",
  ]
])


wait_until.populate_stp_forwarding(iosvl2_0, vlan_num=ini.vlan_list[0], count=2)

wait_until.populate_stp_forwarding(iosvl2_1, vlan_num=ini.vlan_list[0], count=1)
wait_until.populate_stp_blocking(iosvl2_1, vlan_num=ini.vlan_list[0], count=1)

wait_until.populate_stp_forwarding(iosvl2_2, vlan_num=ini.vlan_list[0], count=3)
wait_until.populate_stp_blocking(iosvl2_2, vlan_num=ini.vlan_list[0], count=0)


iosvl2_0.execs([
  f"show spanning-tree vlan {ini.vlan_list[0]}",
  f"show spanning-tree vlan {ini.vlan_list[1]}",
])
iosvl2_1.execs([
  f"show spanning-tree vlan {ini.vlan_list[0]}",
  f"show spanning-tree vlan {ini.vlan_list[1]}",
])
iosvl2_2.execs([
  f"show spanning-tree vlan {ini.vlan_list[0]}",
  f"show spanning-tree vlan {ini.vlan_list[1]}",
])
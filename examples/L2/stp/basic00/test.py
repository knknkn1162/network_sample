from genie import testbed
from cml import CONFIG_YAML, Cml, Pcap
from lib.device import Device
from lib import wait, ipv4
import parse
import ini
import show
import time
import wait_until
from structure.stp_info import (
  State as StpState,
  Role as StpRole,
)

tb = testbed.load(CONFIG_YAML)

# switch
iosvl2_0 = Device(tb, 'iosvl2_0')
iosvl2_1 = Device(tb, 'iosvl2_1')
iosvl2_2 = Device(tb, 'iosvl2_2')

server_0 = Device(tb, 'server_0')
server_1 = Device(tb, 'server_1')

print("####### exec #######")
cml0 = Cml()
pcap01 = Pcap(cml0, ini.iosvl2_0.__name__, ini.iosvl2_1.__name__)
pcap12 = Pcap(cml0, ini.iosvl2_1.__name__, ini.iosvl2_2.__name__)
pcap20 = Pcap(cml0, ini.iosvl2_2.__name__, ini.iosvl2_0.__name__)


# switch
# server setting
server_0.execs([
  ## disable DHCP
  f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
  f"sudo ifconfig eth0 {ini.server_0.eth0.ip_addr} netmask {ini.server_0.eth0.subnet_mask} up",
  f"ifconfig eth0",
])

server_1.execs([
  ## disable DHCP
  f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
  f"sudo ifconfig eth0 {ini.server_1.eth0.ip_addr} netmask {ini.server_1.eth0.subnet_mask} up",
  f"ifconfig eth0",
])

show.mac_ip(iosvl2_0)
show.mac_ip(iosvl2_1)
show.mac_ip(iosvl2_2)

## switchport settings
iosvl2_0.execs([
  [
    f"interface {ini.iosvl2_0.g0_0.name}",
    f"switchport mode access",
    f"switchport access vlan {ini.vlan_num}",
  ],
  [
    f"interface {ini.iosvl2_0.g0_1.name}",
    f"switchport mode access",
    f"switchport access vlan {ini.vlan_num}",
  ],
  [
    f"interface {ini.iosvl2_0.g0_2.name}",
    f"switchport mode access",
    f"switchport access vlan {ini.vlan_num}",
  ],
])

iosvl2_1.execs([
  [
    f"interface {ini.iosvl2_1.g0_0.name}",
    f"switchport mode access",
    f"switchport access vlan {ini.vlan_num}",
  ],
  [
    f"interface {ini.iosvl2_1.g0_1.name}",
    f"switchport mode access",
    f"switchport access vlan {ini.vlan_num}",
  ],
])

iosvl2_2.execs([
  [
    f"interface {ini.iosvl2_2.g0_0.name}",
    f"switchport mode access",
    f"switchport access vlan {ini.vlan_num}",
  ],
  [
    f"interface {ini.iosvl2_2.g0_1.name}",
    f"switchport mode access",
    f"switchport access vlan {ini.vlan_num}",
  ],
  [
    f"interface {ini.iosvl2_2.g0_2.name}",
    f"switchport mode access",
    f"switchport access vlan {ini.vlan_num}",
  ],
])

# spanning tree settings
pcap01.start(maxpackets=200)
pcap12.start(maxpackets=200)
pcap20.start(maxpackets=200)

iosvl2_0.execs([
  [
    f"spanning-tree vlan {ini.vlan_num} priority {ini.iosvl2_0.stp_priority}",
  ]
])
iosvl2_1.execs([
  [
    f"spanning-tree vlan {ini.vlan_num} priority {ini.iosvl2_1.stp_priority}",
  ]
])
iosvl2_2.execs([
  [
    f"spanning-tree vlan {ini.vlan_num} priority {ini.iosvl2_2.stp_priority}",
  ]
])

wait_until.seconds(30)
result = parse.get_stp_info(iosvl2_0, ini.vlan_num, ini.iosvl2_0.g0_0.name)
assert (result.role, result.port_state) == (StpRole.designated, StpState.forwarding)
result = parse.get_stp_info(iosvl2_0, ini.vlan_num, ini.iosvl2_0.g0_1.name)
assert (result.role, result.port_state) == (StpRole.designated, StpState.forwarding)
result = parse.get_stp_info(iosvl2_0, ini.vlan_num, ini.iosvl2_0.g0_2.name)
assert (result.role, result.port_state) == (StpRole.designated, StpState.forwarding)

result = parse.get_stp_info(iosvl2_1, ini.vlan_num, ini.iosvl2_1.g0_0.name)
assert (result.role, result.port_state) == (StpRole.root, StpState.forwarding)
result = parse.get_stp_info(iosvl2_1, ini.vlan_num, ini.iosvl2_1.g0_1.name)
assert (result.role, result.port_state) == (StpRole.designated, StpState.forwarding)

result = parse.get_stp_info(iosvl2_2, ini.vlan_num, ini.iosvl2_2.g0_0.name)
assert (result.role, result.port_state) == (StpRole.alternate, StpState.blocking)
result = parse.get_stp_info(iosvl2_2, ini.vlan_num, ini.iosvl2_2.g0_1.name)
assert (result.role, result.port_state) == (StpRole.root, StpState.forwarding)
result = parse.get_stp_info(iosvl2_2, ini.vlan_num, ini.iosvl2_2.g0_2.name)
assert (result.role, result.type, result.port_state) == (StpRole.designated, StpState.forwarding)

pcap01.download(file=ini.pcap01_file)
pcap12.download(file=ini.pcap12_file)
pcap20.download(file=ini.pcap20_file)

iosvl2_0.execs([
  f"show spanning-tree vlan {ini.vlan_num}",
])

iosvl2_1.execs([
  f"show spanning-tree vlan {ini.vlan_num}",
])

iosvl2_2.execs([
  f"show spanning-tree vlan {ini.vlan_num}",
])
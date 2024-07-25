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
server_2 = Device(tb, 'server_2')
# switch
iosvl2_0 = Device(tb, 'iosvl2_0')
# router
iosv_0 = Device(tb, 'iosv_0')




print("####### exec #######")

# setup server
server_0.execs([
  # eth0 setting
  ## disable DHCP
  f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
  f"sudo ifconfig eth0 {ini.server_0.eth0.ip_addr} netmask {ini.server_0.eth0.subnet_mask} up",
  f"sudo route add default gw {ini.iosv_0.g0_0.sub0.ip_addr}",
  f"ifconfig eth0",
  f"route -e",
])

server_1.execs([
  # eth0 setting
  ## disable DHCP
  f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
  f"sudo ifconfig eth0 {ini.server_1.eth0.ip_addr} netmask {ini.server_1.eth0.subnet_mask} up",
  f"sudo route add default gw {ini.iosv_0.g0_0.sub1.ip_addr}",
  f"ifconfig eth0",
  f"route -e",
])

server_2.execs([
  # eth0 setting
  ## disable DHCP
  f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
  f"sudo ifconfig eth0 {ini.server_2.eth0.ip_addr} netmask {ini.server_2.eth0.subnet_mask} up",
  f"sudo route add default gw {ini.iosv_0.g0_0.sub1.ip_addr}",
  f"ifconfig eth0",
  f"route -e",
])


# switch
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

# check vlan up
wait_until.populate_vlan(iosvl2_0, 2)

# check vlan
iosvl2_0.execs([
  f"show vlan brief",
  f"show interfaces trunk",
])

# router vlan-routing
iosv_0.execs([
  [
    # create multiple virtual interface on a one physical interface
    f"interface {ini.iosv_0.g0_0.name}.{ini.iosv_0.g0_0.sub0.num}",
    f"encapsulation dot1q {ini.iosv_0.g0_0.sub0.vlan.num}",
    f"ip address {ini.iosv_0.g0_0.sub0.ip_addr} {ini.iosv_0.g0_0.sub0.subnet_mask}",
  ],
  [
    f"interface {ini.iosv_0.g0_0.name}.{ini.iosv_0.g0_0.sub1.num}",
    f"encapsulation dot1q {ini.iosv_0.g0_0.sub1.vlan.num}",
    f"ip address {ini.iosv_0.g0_0.sub1.ip_addr} {ini.iosv_0.g0_0.sub1.subnet_mask}",
  ],
  [
    f"interface {ini.iosv_0.g0_0.name}",
    f"no shutdown",
  ]
])

# assume GigabitEthernet0/0 and GigabitEthernet0/0.1 and GigabitEthernet0/0.2
wait_until.populate_up(iosv_0, 3)
# check different vlan, but ping works because of vlan routing in vios
wait_until.populate_server_ping(server_0, ini.server_1.eth0.ip_addr)
# should failed
calc.server_ping(server_0, ini.server_2.eth0.ip_addr, count=15)
calc.server_ping(server_1, ini.server_2.eth0.ip_addr, count=15)
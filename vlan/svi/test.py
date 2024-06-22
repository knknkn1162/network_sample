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
server_5 = Device(tb, 'server_5')
# switch
iosvl2 = Device(tb, 'iosvl2')

print("####### exec #######")
server_1.execs([
  # disable DHCP
  f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
  # eth0 setting
  f"sudo ifconfig eth0 {ini.server_1.eth0.ip_addr} netmask {ini.server_1.eth0.subnet_mask} up",
  f"sudo route add default gw {ini.iosvl2.vlan1.ip_addr}",
  f"ifconfig eth0"
])
server_2.execs([
  # disable DHCP
  f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
  # eth0 setting
  f"sudo ifconfig eth0 {ini.server_2.eth0.ip_addr} netmask {ini.server_2.eth0.subnet_mask} up",
  # set gateway
  f"sudo route add default gw {ini.iosvl2.vlan1.ip_addr}",
  f"ifconfig eth0"
])
server_3.execs([
  # disable DHCP
  f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
  # eth0 setting
  f"sudo ifconfig eth0 {ini.server_3.eth0.ip_addr} netmask {ini.server_3.eth0.subnet_mask} up",
  f"sudo route add default gw {ini.iosvl2.vlan2.ip_addr}",
  f"ifconfig eth0"
])
server_4.execs([
  # disable DHCP
  f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
  # eth0 setting
  f"sudo ifconfig eth0 {ini.server_4.eth0.ip_addr} netmask {ini.server_4.eth0.subnet_mask} up",
  f"sudo route add default gw {ini.iosvl2.vlan2.ip_addr}",
  f"ifconfig eth0"
])
server_5.execs([
  # disable DHCP
  f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
  # eth0 setting
  f"sudo ifconfig eth0 {ini.server_5.eth0.ip_addr} netmask {ini.server_5.eth0.subnet_mask} up",
  # routed port
  f"sudo route add default gw {ini.iosvl2.g0_4.ip_addr}",
  f"ifconfig eth0"
])
print("wait for sync....."); time.sleep(5)

vlan_list_str = ','.join(map(str,ini.iosvl2.vlan_list))
iosvl2.execs([
  [
    # enable routing
    f"ip routing",
    f"vlan {vlan_list_str}"
  ],
  # switchport (Don't forget to set this)
  [
    f"interface {ini.iosvl2.g0_0.name}",
    f"switchport access vlan {ini.iosvl2.g0_0.vlan}"
  ],
  [
    f"interface {ini.iosvl2.g0_1.name}",
    f"switchport access vlan {ini.iosvl2.g0_1.vlan}"
  ],
  [
    f"interface {ini.iosvl2.g0_2.name}",
    f"switchport access vlan {ini.iosvl2.g0_2.vlan}"
  ],
  [
    f"interface {ini.iosvl2.g0_3.name}",
    f"switchport access vlan {ini.iosvl2.g0_3.vlan}"
  ],
  # SVI @ vlan1
  [
    f"interface vlan {ini.iosvl2.vlan1.num}",
    f"ip address {ini.iosvl2.vlan1.ip_addr} {ini.iosvl2.vlan1.subnet_mask}",
    f"no shutdown"
  ],
  # SVI @ vlan2
  [
    f"interface vlan {ini.iosvl2.vlan2.num}",
    f"ip address {ini.iosvl2.vlan2.ip_addr} {ini.iosvl2.vlan2.subnet_mask}",
    f"no shutdown"
  ],
  # routed port @ g0/4
  [
    f"interface {ini.iosvl2.g0_4.name}",
    f"no switchport",
    f"ip address {ini.iosvl2.g0_4.ip_addr} {ini.iosvl2.g0_4.subnet_mask}"
  ]
])

# wait until vlan is up
for i in range(30):
  print(f"######{i} retry")
  res = iosvl2.parse("show ip interface brief")
  flag = True
  for key, value in res['interface'].items():
    if not key.lower().startswith("vlan"):
      continue
    if value['status'] != 'up':
      flag = False
    if value['protocol'] != 'up':
      flag = False
  if flag:
    print("next..")
    break
  print("wait for sync..."); time.sleep(3)

iosvl2.execs([
  # check all are up including vlan
  f"show ip interface brief",
  f"show vlan brief",
])

# ping test
server_1.execs([
  # VLAN1_ID
  f"ping {ini.server_2.eth0.ip_addr} -c 5",
  # VLAN2_ID
  f"ping {ini.server_3.eth0.ip_addr} -c 5",
  f"ping {ini.server_4.eth0.ip_addr} -c 5",
  # routed port
  f"ping {ini.server_5.eth0.ip_addr} -c 5",
])

iosvl2.execs([
  f"show ip route"
])
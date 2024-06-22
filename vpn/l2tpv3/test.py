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

server_0 = Device(tb, 'server_0')
server_1 = Device(tb, 'server_1')

cml0 = Cml()
pcap = Pcap(cml0, ini.iosv_0.__name__, ini.iosv_1.__name__)

print("####### exec #######")
# set ip
server_0.execs([
  # eth0 setting
  ## disable DHCP
  f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
  f"sudo ifconfig eth0 {ini.server_0.eth0.ip_addr} netmask {ini.server_0.eth0.subnet_mask} up",
  f"sudo route add default gw {ini.iosv_0.g0_0.ip_addr}",
  f"ifconfig eth0",
  f"route -e",
])

server_1.execs([
  # eth0 setting
  ## disable DHCP
  f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
  f"sudo ifconfig eth0 {ini.server_1.eth0.ip_addr} netmask {ini.server_1.eth0.subnet_mask} up",
  f"sudo route add default gw {ini.iosv_1.g0_0.ip_addr}",
  f"ifconfig eth0",
  f"route -e",
])

# interface up
iosv_0.execs([
  # g0_0 only
  [
    f"interface {ini.iosv_0.g0_1.name}",
    f"ip addr {ini.iosv_0.g0_1.ip_addr} {ini.iosv_0.g0_1.subnet_mask}",
    f"no shutdown",
  ],
  # [
  #   f"interface {ini.iosv_0.g0_1.name}",
  #   f"ip addr {ini.iosv_0.g0_1.ip_addr} {ini.iosv_0.g0_1.subnet_mask}",
  #   f"no shutdown",
  # ],
  # default gw
  # [
  #   f"ip route 0.0.0.0 0.0.0.0 {ini.iosv_1.g0_1.ip_addr}",
  # ]
])

iosv_1.execs([
  # g0_0 only
  [
    f"interface {ini.iosv_1.g0_1.name}",
    f"ip addr {ini.iosv_1.g0_1.ip_addr} {ini.iosv_1.g0_1.subnet_mask}",
    f"no shutdown"
  ],
  # [
  #   f"interface {ini.iosv_1.g0_1.name}",
  #   f"ip addr {ini.iosv_1.g0_1.ip_addr} {ini.iosv_1.g0_1.subnet_mask}",
  #   f"no shutdown",
  # ],
  # default gw
  # [
  #   f"ip route 0.0.0.0 0.0.0.0 {ini.iosv_0.g0_1.ip_addr}",
  # ]
])

# L2TPv3 settings
iosv_0.execs([
  [
    f"pseudowire-class {ini.pw_class}",
    f"encapsulation l2tpv3",
    # set interface name inside l2tpv3
    f"ip local interface {ini.iosv_0.g0_1.name}",
  ],
  # outside
  [
    f"interface {ini.iosv_0.g0_0.name}",
    f"no ip address",
    f"no shutdown",
    f"xconnect {ini.iosv_1.g0_1.ip_addr} {ini.vc_id} pw-class {ini.pw_class}"
  ]
])

iosv_1.execs([
  [
    f"pseudowire-class {ini.pw_class}",
    f"encapsulation l2tpv3",
    # set interface name inside l2tpv3
    f"ip local interface {ini.iosv_1.g0_1.name}",
  ],
  # outside
  [
    f"interface {ini.iosv_1.g0_0.name}",
    f"no ip address",
    f"no shutdown",
    f"xconnect {ini.iosv_0.g0_1.ip_addr} {ini.vc_id} pw-class {ini.pw_class}"
  ]
])

wait_until.seconds(15)

iosv_0.execs([
  f"show l2tp session",

])

iosv_1.execs([
  f"show l2tp session",
])

# test ping
wait_until.populate_server_ping(server_0, ini.server_1.eth0.ip_addr)
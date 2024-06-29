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
server_0 = Device(tb, 'server_0')
server_1 = Device(tb, 'server_1')

cml0 = Cml()

print("####### exec #######")

# server settings
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
  f"sudo route add default gw {ini.iosv_0.g0_1.ip_addr}",
  f"ifconfig eth0",
  f"route -e",
])

iosv_0.execs([
  [
    f"interface {ini.iosv_0.g0_0.name}",
    f"ip addr {ini.iosv_0.g0_0.ip_addr} {ini.iosv_0.g0_0.subnet_mask}",
    f"no shutdown",
  ],
  [
    f"interface {ini.iosv_0.g0_1.name}",
    f"ip addr {ini.iosv_0.g0_1.ip_addr} {ini.iosv_0.g0_1.subnet_mask}",
    f"no shutdown",
  ],
  [
    f"line vty 0 4",
    f"password {ini.password}",
    f"login",
    f"transport input telnet",
    f"enable secret {ini.enable_password}"
  ],
])

acl_num = 1
iosv_0.execs([
  [
    # ip access-list standard {acl_name}
    # permit host {ini.server_1.eth0.ip_addr}
    f"access-list {acl_num} permit host {ini.server_1.eth0.ip_addr}",
  ],
  [
    f"line vty 0 4",
    # access-class {acl_name} in
    f"access-class {acl_num} in",
  ],
  f"show access-lists {acl_num}",
])

#refused
server_0.execs([
  f"telnet {ini.iosv_0.g0_0.ip_addr}",
])

# Ctrl-C
server_1.execs([
  f"telnet {ini.iosv_0.g0_1.ip_addr}",
])
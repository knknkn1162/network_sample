from genie import testbed
import cml
from lib.device import Device
import ini
import time
import ipaddress

tb = testbed.load(cml.CONFIG_YAML)

# tinylinux
server_0 = Device(tb, 'server_0')
server_1 = Device(tb, 'server_1')
# router
iosv_0 = Device(tb, 'iosv_0')
iosv_1 = Device(tb, 'iosv_1')

print("####### exec #######")
server_0.execs([
  # eth0 setting
  ## disable DHCP
  f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
  f"sudo ifconfig eth0 {ini.server_0.eth0.ip_addr} netmask {ini.server_0.eth0.subnet_mask} up",
  f"sudo route add default gw {ini.iosv_0.g0_0.ip_addr}",
  f"ifconfig eth0"
])

server_1.execs([
  # eth0 setting
  ## disable DHCP
  f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
  f"sudo ifconfig eth0 {ini.server_1.eth0.ip_addr} netmask {ini.server_1.eth0.subnet_mask} up",
  f"sudo route add default gw {ini.iosv_1.g0_0.ip_addr}",
  f"ifconfig eth0"
])

print("wait for sync....."); time.sleep(5)

## setup ip address in routers and up
iosv_0.execs([
  [
    f"interface {ini.iosv_0.g0_0.name}",
    f"ip addr {ini.iosv_0.g0_0.ip_addr} {ini.iosv_0.g0_0.subnet_mask}",
    f"no shutdown"
  ],
  [
    f"interface {ini.iosv_0.g0_1.name}",
    f"ip addr {ini.iosv_0.g0_1.ip_addr} {ini.iosv_0.g0_1.subnet_mask}",
    f"no shutdown"
  ],
  f"show ip interface brief",
  #f"show interface"
])

iosv_1.execs([
  [
    f"interface {ini.iosv_1.g0_0.name}",
    f"ip addr {ini.iosv_1.g0_0.ip_addr} {ini.iosv_1.g0_0.subnet_mask}",
    f"no shutdown"
  ],
  [
    f"interface {ini.iosv_1.g0_1.name}",
    f"ip addr {ini.iosv_1.g0_1.ip_addr} {ini.iosv_1.g0_1.subnet_mask}",
    f"no shutdown"
  ],
  f"show ip interface brief",
  #f"show interface"
])

## static routing
ipv4 = ipaddress.ip_interface(f"{ini.server_1.eth0.ip_addr}/{ini.server_1.eth0.subnet_mask}")
iosv_0.execs([
  [
    # <network> <subnet_mask> <next-hop>
    f"ip route {ipv4.network[0]} {ini.server_1.eth0.subnet_mask} {ini.iosv_1.g0_1.ip_addr}"
  ],
  f"show ip route",
])

ipv4 = ipaddress.ip_interface(f"{ini.server_0.eth0.ip_addr}/{ini.server_0.eth0.subnet_mask}")
iosv_1.execs([
  [
    # <network> <subnet_mask> <next-hop>
    f"ip route {ipv4.network[0]} {ini.server_0.eth0.subnet_mask} {ini.iosv_0.g0_1.ip_addr}"
  ],
  f"show ip route",
])

# test
server_0.execs([
  f"ping {ini.server_1.eth0.ip_addr} -c 5"
])
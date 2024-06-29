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

cml0 = Cml()

print("####### exec #######")

# server setup
server_0.execs([
  # eth0 setting
  ## disable DHCP
  f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
  f"sudo ifconfig eth0 {ini.server_0.eth0.ip_addr} netmask {ini.server_0.eth0.subnet_mask} up",
  f"sudo route add default gw {ini.iosv_0.g0_0.ip_addr}",
  f"ifconfig eth0",
  f"route -e",
])

# interface up
iosv_0.execs([
  [
    f"interface {ini.iosv_0.g0_0.name}",
    f"ip addr {ini.iosv_0.g0_0.ip_addr} {ini.iosv_0.g0_0.subnet_mask}",
    f"no shutdown",
  ],
])

iosv_0.execs([
  [
    f"snmp-server view {ini.snmp_settings.viewname} {ini.snmp_settings.oid_system} include",
    f"snmp-server view {ini.snmp_settings.viewname} {ini.snmp_settings.oid_cisco} include",
    f"snmp-server group {ini.snmp_settings.group_name} v3 auth read {ini.snmp_settings.viewname}",
    f"snmp-server user {ini.snmp_settings.user_name} {ini.snmp_settings.group_name} v3 auth md5 {ini.snmp_settings.password}"
  ]
])

iosv_0.execs([
  f"show snmp view",
  f"show snmp group",
  f"show snmp user",
])
from genie import testbed
from cml import CONFIG_YAML, Cml
from lib.device import Device
from lib import wait
import ini
import ipaddress
import time

# wait until
def count_rip(device: Device):
  # if `show ip route rip`, SchemaEmptyParserError occurs
  res = device.parse("show ip route")
  routes = res.get('vrf', {}).get('default', {}).get('address_family', {}).get('ipv4', {}).get('routes', {})
  cnt = 0
  for key, val in routes.items():
    cnt += (val.get('source_protocol') == 'rip')
  return cnt

@wait.retry(count=30, val=6, sleep_time=5)
def test_rips(device1, device2, device3):
  return count_rip(device1) + count_rip(device2) + count_rip(device3)



tb = testbed.load(CONFIG_YAML)
cml = Cml()
lab = cml.lab

# tinylinux
server_0 = Device(tb, 'server_0')
server_1 = Device(tb, 'server_1')

# router
iosv_0 = Device(tb, 'iosv_0')
iosv_1 = Device(tb, 'iosv_1')
iosv_2 = Device(tb, 'iosv_2')



print("####### exec #######")
server_0.execs([
  # eth0 setting
  ## disable DHCP
  f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
  f"sudo ifconfig eth0 {ini.server_0.eth0.ip_addr} netmask {ini.server_0.eth0.subnet_mask} up",
  f"sudo route add default gw {ini.iosv_0.g0_0.ip_addr}",
  f"ifconfig eth0",
])

server_1.execs([
  # eth0 setting
  ## disable DHCP
  f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
  f"sudo ifconfig eth0 {ini.server_1.eth0.ip_addr} netmask {ini.server_1.eth0.subnet_mask} up",
  f"sudo route add default gw {ini.iosv_2.g0_1.ip_addr}",
  f"ifconfig eth0"
])

# up
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
])

iosv_2.execs([
  [
    f"interface {ini.iosv_2.g0_0.name}",
    f"ip addr {ini.iosv_2.g0_0.ip_addr} {ini.iosv_2.g0_0.subnet_mask}",
    f"no shutdown"
  ],
  [
    f"interface {ini.iosv_2.g0_1.name}",
    f"ip addr {ini.iosv_2.g0_1.ip_addr} {ini.iosv_2.g0_1.subnet_mask}",
    f"no shutdown"
  ],
])

# RIP settings
key = cml.start_pcap(ini.iosv_0.__name__, ini.iosv_1.__name__)
g0_0_ipv4 = ipaddress.ip_interface(f"{ini.iosv_0.g0_0.ip_addr}/{ini.iosv_0.g0_0.subnet_mask}")
g0_1_ipv4 = ipaddress.ip_interface(f"{ini.iosv_0.g0_1.ip_addr}/{ini.iosv_0.g0_1.subnet_mask}")
iosv_0.execs([
  [
    f"router rip",
    f"version 2",
    # error to set network {g0_0_ipv4.network[0]} {ini.INVERSE_MASK_24}
    f"network {g0_0_ipv4.network[0]}",
    f"network {g0_1_ipv4.network[0]}",
    f"no auto-summary",
    # supress RIP packet
    f"passive-interface {ini.iosv_0.g0_0.name}"
  ],
])

g0_0_ipv4 = ipaddress.ip_interface(f"{ini.iosv_1.g0_0.ip_addr}/{ini.iosv_1.g0_0.subnet_mask}")
g0_1_ipv4 = ipaddress.ip_interface(f"{ini.iosv_1.g0_1.ip_addr}/{ini.iosv_1.g0_1.subnet_mask}")
iosv_1.execs([
  [
    f"router rip",
    f"version 2",
    f"network {g0_0_ipv4.network[0]}",
    f"network {g0_1_ipv4.network[0]}",
    f"no auto-summary",
  ],
])

g0_0_ipv4 = ipaddress.ip_interface(f"{ini.iosv_2.g0_0.ip_addr}/{ini.iosv_2.g0_0.subnet_mask}")
g0_1_ipv4 = ipaddress.ip_interface(f"{ini.iosv_2.g0_1.ip_addr}/{ini.iosv_2.g0_1.subnet_mask}")
iosv_2.execs([
  [
    f"router rip",
    f"version 2",
    f"network {g0_0_ipv4.network[0]}",
    f"network {g0_1_ipv4.network[0]}",
    f"no auto-summary",
    # supress RIP packet
    f"passive-interface {ini.iosv_2.g0_1.name}"
  ],
])

test_rips(iosv_0, iosv_1, iosv_2)

cml.download_pcap(key, file=ini.pcap_file)
cml.stop_pcap(ini.iosv_0.__name__, ini.iosv_1.__name__)

# check ripv2 is set
iosv_0.execs([
  f"show ip protocols",
  f"show ip rip database",
  f"show ip route rip"
])
iosv_1.execs([
  f"show ip protocols",
  f"show ip rip database",
  f"show ip route rip"
])
iosv_2.execs([
  f"show ip protocols",
  f"show ip rip database",
  f"show ip route rip"
])

# test ping
server_0.execs([
  f"ping {ini.server_1.eth0.ip_addr} -c 5"
])
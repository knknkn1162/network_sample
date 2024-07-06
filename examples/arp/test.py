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

iosvl2_0 = Device(tb, 'iosvl2_0')
server_0 = Device(tb, 'server_0')
server_1 = Device(tb, 'server_1')

cml0 = Cml()
#pcap = Pcap(cml0, ini.iosv_0.__name__, ini.iosv_1.__name__)

print("####### exec #######")

# interface up
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

iosvl2_0.execs([
  f"show mac address-table",
  f"clear mac address-table dynamic",
])

server_0.execs([
  f"arp -a",
])

server_1.execs([
  f"arp -a",
])

# arp test
server_0.execs([
  f"ping {ini.server_1.eth0.ip_addr} -c 5"
])

# check if register MAC address or not(it should be true)
iosvl2_0.execs([
  f"show mac address-table",
])

server_0.execs([
  f"arp -a",
])

server_1.execs([
  f"arp -a",
])

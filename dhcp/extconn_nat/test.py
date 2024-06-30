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

cml0 = Cml()
print("####### exec #######")

# server settings -> DHCP enable by default

# interface up
iosv_0.execs([
  [
    f"interface {ini.iosv_0.g0_0.name}",
    f"ip address dhcp",
    f"no shutdown",
  ],
])

wait_until.populate_up(iosv_0, 1)

wait_until.seconds(10)
print(calc.ip_addr(iosv_0, ini.iosv_0.g0_0.name))
wait_until.populate_router_ping(iosv_0, ini.public0_ip)

iosv_0.execs([
  f"show ip interface brief",
  f"show interfaces {ini.iosv_0.g0_0.name}",
  f"show ip route",
])
from genie import testbed
from cml import CONFIG_YAML, Cml, Pcap
from lib.device import Device
from lib import wait, ipv4
import ini
import time
import wait_until, calc
import show

tb = testbed.load(CONFIG_YAML)

iosv_0 = Device(tb, 'iosv_0')
iosv_1 = Device(tb, 'iosv_1')

cml0 = Cml()
#pcap01 = Pcap(cml0, ini.iosv_0.__name__, ini.iosv_1.__name__)

print("####### exec #######")

# interface up
iosv_0.execs([
  [
    f"interface {ini.iosv_0.g0_0.name}",
    f"ip addr {ini.iosv_0.g0_0.ip_addr} {ini.iosv_0.g0_0.subnet_mask}",
    f"no shutdown"
  ],
])
iosv_1.execs([
  [
    f"interface {ini.iosv_1.g0_0.name}",
    f"ip addr {ini.iosv_1.g0_0.ip_addr} {ini.iosv_1.g0_0.subnet_mask}",
    f"no shutdown"
  ],
])

iosv_0.execs([
  [
    f"ip domain-name {ini.domain_name}",
    f"crypto key generate rsa modulus 1024",
    f"username {ini.username} password {ini.password}",
  ],
  [
    f"ip ssh version 2",
  ],
  [
    f"line vty 0 4",
    f"transport input ssh",
    f"login local",
  ],
])

# test
# iosv_1.execs([
#   f"ssh -l {ini.username} {ini.iosv_0.g0_0.ip_addr}"
# ])
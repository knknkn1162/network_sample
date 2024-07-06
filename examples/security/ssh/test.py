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
#pcap01 = Pcap(cml0, ini.iosv_0.__name__, ini.iosv_1.__name__)

print("####### exec #######")

# interface up
iosv_0.execs([
  [
    f"ip domain-name {ini.domain_name}",
    f"crypto key generate rsa modulus 1024",
    f"username {ini.username} password {ini.password}",
    f"line console 0",
    f"login local",
    # transport input ssh
    f"transport preferred ssh",
  ],
  [
    f"ip ssh version 2",
  ],
])
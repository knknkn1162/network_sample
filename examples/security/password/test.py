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

cml0 = Cml()
#pcap01 = Pcap(cml0, ini.iosv_0.__name__, ini.iosv_1.__name__)

print("####### exec #######")

# interface up
iosv_0.execs([
  # console or vty
  [
    f"service password-encryption",
    f"line console 0",
    f"password {ini.console_password}",
    f"login",
    f"no service password-encryption",
  ],
  # encrypt enable password
  [
    f"enable secret {ini.enable_password}",
    #f"enable password {ini.enable_password}",
  ],
  f"show running-config | include enable secret",
])

iosv_1.execs([
  [
    f"username {ini.username} password {ini.console_password}",
    f"line console 0",
    f"login local",
  ],
])

iosv_0.execs([
  f"exit",
])
iosv_1.execs([
  f"exit",
])
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

print("####### exec #######")

# no need to setup ip addr
iosv_0.execs([
  [
    f"interface {ini.iosv_0.g0_0.name}",
    f"cdp enable",
    f"no shutdown",
  ],
])

iosv_1.execs([
  [
    f"interface {ini.iosv_0.g0_0.name}",
    f"cdp enable",
    f"no shutdown",
  ],
])
wait_until.seconds(15)
iosv_0.execs([
  f"show cdp",
  f"show cdp interface",
  f"show cdp neighbors",
  f"show cdp neighbors detail",
  f"show cdp entry *",
])

iosv_1.execs([
  f"show cdp",
  f"show cdp interface",
  f"show cdp neighbors",
  f"show cdp neighbors detail",
  f"show cdp entry *",
])
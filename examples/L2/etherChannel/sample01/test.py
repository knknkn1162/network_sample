from genie import testbed
from cml import CONFIG_YAML, Cml, Pcap
from lib.device import Device
from lib import wait, ipv4
import ini
import time
import wait_until, calc

tb = testbed.load(CONFIG_YAML)

# switch
iosvl2_0 = Device(tb, 'iosvl2_0')
iosvl2_1 = Device(tb, 'iosvl2_1')



print("####### exec #######")

iosvl2_0.execs([
  [
    f"interface {ini.iosvl2_0.g0_0.name}",
    f"switchport trunk encapsulation dot1q",
    # set trunk mode in 2etherchannel
    f"switchport mode trunk",
    f"channel-group {ini.channel_group} mode active",
    # protocol(option) PAgP or LACP
    f"channel-protocol lacp",
  ],
  [
    f"interface {ini.iosvl2_0.g0_1.name}",
    f"switchport trunk encapsulation dot1q",
    f"switchport mode trunk",
    f"channel-group {ini.channel_group} mode active",
    # protocol(option) PAgP or LACP
    f"channel-protocol lacp",
  ],
])

iosvl2_1.execs([
  [
    f"interface {ini.iosvl2_1.g0_0.name}",
    f"switchport trunk encapsulation dot1q",
    f"switchport mode trunk",
    f"channel-group {ini.channel_group} mode passive",
  ],
  [
    f"interface {ini.iosvl2_1.g0_1.name}",
    f"switchport trunk encapsulation dot1q",
    f"switchport mode trunk",
    f"channel-group {ini.channel_group} mode passive",
  ],
])

wait_until.populate_etherchannel(iosvl2_0, count=2, protocol=ini.ETHERCHANNEL_LACP)
wait_until.populate_etherchannel(iosvl2_1, count=2, protocol=ini.ETHERCHANNEL_LACP)

iosvl2_0.execs([
  f"show etherchannel summary",
  f"show spanning-tree",
  # SP: passive
  f"show lacp neighbor",
])

iosvl2_1.execs([
  f"show etherchannel summary",
  f"show spanning-tree",
  # SA: active
  f"show lacp neighbor",
])

# down
iosvl2_0.execs([
  [
    # shutdown the one of links
    f"interface {ini.iosvl2_0.g0_1.name}",
    f"shutdown",
  ],
])

# P -> D(down)
wait_until.populate_etherchannel(iosvl2_0, 1, protocol=ini.ETHERCHANNEL_LACP)
# P -> w -> s(suspended)
wait_until.populate_etherchannel(iosvl2_1, 1, protocol=ini.ETHERCHANNEL_LACP)

iosvl2_0.execs([
  f"show etherchannel summary",
  f"show lacp neighbor",
])

iosvl2_1.execs([
  f"show etherchannel summary",
  f"show lacp neighbor",
])
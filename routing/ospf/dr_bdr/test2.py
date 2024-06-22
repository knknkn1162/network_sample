from genie import testbed
from cml import CONFIG_YAML, Cml, Pcap, Lab
from lib.device import Device
from lib import wait, ipv4
import ini
import time
import wait_until, calc
import show

tb = testbed.load(CONFIG_YAML)


iosv_0 = Device(tb, 'iosv_0')
iosv_1 = Device(tb, 'iosv_1')
iosv_2 = Device(tb, 'iosv_2')
iosv_3 = Device(tb, 'iosv_3')

cml0 = Cml()
lab0 = Lab(cml0.lab)
# pcap0 = Pcap(cml0, ini.switch_0.__name__, ini.iosv_1.__name__)

print("####### exec #######")

iosv_0.execs([
  f"show ip ospf neighbor",
])
iosv_1.execs([
  f"show ip ospf neighbor",
])
# 192.168.0.1     100   FULL/DR 
iosv_2.execs([
  f"show ip ospf neighbor",
])
iosv_3.execs([
  f"show ip ospf neighbor",
])

# change settings

# save settings
# for dev in [iosv_0, iosv_1, iosv_2, iosv_3]:
#   dev.save()

# lab0.restart(is_wipe=False, waittime=5)
node_iosv_0 = cml0.lab.get_node_by_label(ini.iosv_0.__name__)
print(f"stop node {ini.iosv_0.__name__}")
node_iosv_0.stop()

wait_until.seconds(15)
# delete iosv_0 in the neighbor
iosv_2.execs([
  f"show ip ospf neighbor",
])

node_iosv_0.start()
wait_until.seconds(15)
# 192.168.0.1     100   2WAY/DROTHER
iosv_2.execs([
  f"show ip ospf neighbor",
])
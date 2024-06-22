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

iosv_2.execs([
  [
    f"interface {ini.iosv_2.g0_0.name}",
    f"ip addr {ini.iosv_2.g0_0.ip_addr} {ini.iosv_2.g0_0.subnet_mask}",
    f"no shutdown"
  ],
])

iosv_3.execs([
  [
    f"interface {ini.iosv_3.g0_0.name}",
    f"ip addr {ini.iosv_3.g0_0.ip_addr} {ini.iosv_3.g0_0.subnet_mask}",
    f"no shutdown"
  ],
])

# ospf setting
iosv_0.execs([
  [
    f"router ospf {ini.ospf_process_id}",
    f"network {ini.iosv_network0} {ini.INVERSE_MASK_24} area {ini.iosv_0.g0_0.area_id}",
  ],
])

iosv_1.execs([
  [
    f"router ospf {ini.ospf_process_id}",
    f"network {ini.iosv_network0} {ini.INVERSE_MASK_24} area {ini.iosv_1.g0_0.area_id}",
  ],
])
iosv_2.execs([
  [
    f"router ospf {ini.ospf_process_id}",
    f"network {ini.iosv_network0} {ini.INVERSE_MASK_24} area {ini.iosv_2.g0_0.area_id}",
  ],
])
iosv_3.execs([
  [
    f"router ospf {ini.ospf_process_id}",
    f"network {ini.iosv_network0} {ini.INVERSE_MASK_24} area {ini.iosv_3.g0_0.area_id}",
  ],
])

# save settings
for dev in [iosv_0, iosv_1, iosv_2, iosv_3]:
  dev.save()

lab0.restart(is_wipe=False, waittime=5)

#pcap0.stop(); pcap0.download(file=ini.pcap0_file)

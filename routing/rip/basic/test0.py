from genie import testbed
from cml import CONFIG_YAML, Cml
from lib.device import Device
import ini
import ipaddress
import time
from lib import wait

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


# wait until
def count_rip(device: Device):
  res = device.parse("show ip route")
  routes = res.get('vrf', {}).get('default', {}).get('address_family', {}).get('ipv4', {}).get('routes', {})
  cnt = 0
  for key, val in routes.items():
    cnt += (val.get('source_protocol') == 'rip')
  return cnt

@wait.retry(30, 6, 5)
def count_rips(device1, device2, device3):
  return count_rip(device1) + count_rip(device2) + count_rip(device3)


count_rips(iosv_0, iosv_1, iosv_2)

#cml.download_pcap(key, file=ini.pcap_file)
#cml.stop_pcap(ini.iosv_0.__name__, ini.iosv_1.__name__)

# test ping
server_0.execs([
  f"ping {ini.server_1.eth0.ip_addr} -c 5"
])
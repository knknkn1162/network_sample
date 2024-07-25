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
iosv_2 = Device(tb, 'iosv_2')

server_0 = Device(tb, 'server_0')
cml0 = Cml()
#pcap1_2 = Pcap(cml0, ini.iosv_1.__name__, ini.iosv_2.__name__)
#pcap0_2 = Pcap(cml0, ini.iosv_0.__name__, ini.iosv_2.__name__)

print("####### exec #######")
# set ip
server_0.execs([
  # eth0 setting
  ## disable DHCP
  f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
  f"sudo ifconfig eth0 {ini.server_0.eth0.ip_addr} netmask {ini.server_0.eth0.subnet_mask} up",
  f"sudo route add default gw {ini.iosv_0.g0_2.ip_addr}",
  f"ifconfig eth0"
])


## up
iosv_0.execs([
  [
    f"interface {ini.iosv_0.g0_0.name}",
    f"ip addr {ini.iosv_0.g0_0.ip_addr} {ini.iosv_0.g0_0.subnet_mask}",
    f"bandwidth {ini.iosv_0.g0_0.bandwidth}",
    f"no shutdown",
  ],
  [
    f"interface {ini.iosv_0.g0_1.name}",
    f"ip addr {ini.iosv_0.g0_1.ip_addr} {ini.iosv_0.g0_1.subnet_mask}",
    f"no shutdown",
  ],
  [
    f"interface {ini.iosv_0.g0_2.name}",
    f"ip addr {ini.iosv_0.g0_2.ip_addr} {ini.iosv_0.g0_2.subnet_mask}",
    f"no shutdown",
  ],
])

iosv_1.execs([
  [
    f"interface {ini.iosv_1.g0_0.name}",
    f"ip addr {ini.iosv_1.g0_0.ip_addr} {ini.iosv_1.g0_0.subnet_mask}",
    f"no shutdown",
  ],
  [
    f"interface {ini.iosv_1.g0_1.name}",
    f"ip addr {ini.iosv_1.g0_1.ip_addr} {ini.iosv_1.g0_1.subnet_mask}",
    f"no shutdown",
  ],
])


iosv_2.execs([
  [
    f"interface {ini.iosv_2.g0_0.name}",
    f"ip addr {ini.iosv_2.g0_0.ip_addr} {ini.iosv_2.g0_0.subnet_mask}",
    f"no shutdown",
  ],
  [
    f"interface {ini.iosv_2.g0_1.name}",
    f"ip addr {ini.iosv_2.g0_1.ip_addr} {ini.iosv_2.g0_1.subnet_mask}",
    f"bandwidth {ini.iosv_2.g0_1.bandwidth}",
    f"no shutdown",
  ],
  [
    f"interface {ini.iosv_2.loopback0.name}",
    f"ip addr {ini.iosv_2.loopback0.ip_addr} {ini.iosv_2.loopback0.subnet_mask}",
  ]
])

# eigrp settings
#pcap1_2.start(maxpackets=1000)
#pcap0_2.start(maxpackets=1000)

iosv_0_g0_0_network0 = ipv4.get_network0(ini.iosv_0.g0_0.ip_addr, ini.iosv_0.g0_0.subnet_mask)
iosv_0_g0_1_network0 = ipv4.get_network0(ini.iosv_0.g0_1.ip_addr, ini.iosv_0.g0_1.subnet_mask)
iosv_0_g0_2_network0 = ipv4.get_network0(ini.iosv_0.g0_2.ip_addr, ini.iosv_0.g0_2.subnet_mask)

iosv_0.execs([
  [
    f"router eigrp {ini.eigrp_num}",
    f"no auto-summary",
    f"network {iosv_0_g0_0_network0}",
    f"network {iosv_0_g0_1_network0}",
    f"network {iosv_0_g0_2_network0}",
    f"passive-interface {ini.iosv_0.g0_2.name}",
  ]
])
iosv_1_g0_0_network0 = ipv4.get_network0(ini.iosv_1.g0_0.ip_addr, ini.iosv_1.g0_0.subnet_mask)
iosv_1_g0_1_network0 = ipv4.get_network0(ini.iosv_1.g0_1.ip_addr, ini.iosv_1.g0_1.subnet_mask)
iosv_1.execs([
  [
    f"router eigrp {ini.eigrp_num}",
    f"no auto-summary",
    f"network {iosv_1_g0_0_network0}",
    f"network {iosv_1_g0_1_network0}",
  ]
])
iosv_2_g0_0_network0 = ipv4.get_network0(ini.iosv_2.g0_0.ip_addr, ini.iosv_2.g0_0.subnet_mask)
iosv_2_g0_1_network0 = ipv4.get_network0(ini.iosv_2.g0_1.ip_addr, ini.iosv_2.g0_1.subnet_mask)
iosv_2_loopback0_network0 = ipv4.get_network0(ini.iosv_2.loopback0.ip_addr, ini.iosv_2.loopback0.subnet_mask)
iosv_2.execs([
  [
    f"router eigrp {ini.eigrp_num}",
    f"no auto-summary",
    f"network {iosv_2_g0_0_network0}",
    f"network {iosv_2_g0_1_network0}",
    f"network {iosv_2_loopback0_network0}",
  ]
])

wait_until.populate_eigrp(iosv_0, ini.eigrp_num, 2)
wait_until.populate_eigrp(iosv_1, ini.eigrp_num, 2)
wait_until.populate_eigrp(iosv_2, ini.eigrp_num, 2)
wait_until.populate_server_ping(server_0, ini.iosv_2.loopback0.ip_addr)

iosv_0.execs([
  f"show ip protocols",
  f"show ip eigrp neighbors detail",
  f"show ip route eigrp",
  f"show ip eigrp topology",
  f"show ip eigrp traffic",
])

iosv_1.execs([
  f"show ip protocols",
  f"show ip eigrp neighbors detail",
  f"show ip route eigrp",
  f"show ip eigrp topology",
  f"show ip eigrp traffic",
])

iosv_2.execs([
  f"show ip protocols",
  f"show ip eigrp neighbors detail",
  f"show ip route eigrp",
  f"show ip eigrp topology",
  f"show ip eigrp traffic",
])

# load balancing
# via 192.168.1.2 (131072/130816), GigabitEthernet0/1
# via 192.168.0.3 (153856/128256), GigabitEthernet0/0
## 131072 * 2 > 153856, so we set the variance=2
iosv_0.execs([
  [
    f"router eigrp {ini.eigrp_num}",
    f"variance 2",
  ]
])


iosv_0.execs([
  f"show ip route eigrp",
  f"show ip route {ini.iosv_2.loopback0.ip_addr}",
])

iosv_0.execs([
  f"traceroute {ini.iosv_2.loopback0.ip_addr} probe 10",
  f"traceroute {ini.iosv_2.loopback0.ip_addr} probe 10",
  f"traceroute {ini.iosv_2.loopback0.ip_addr} probe 10",
])

#pcap1_2.stop(); pcap1_2.download(file=ini.pcap1_file)
#pcap0_2.stop(); pcap0_2.download(file=ini.pcap0_file)
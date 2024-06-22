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
server_1 = Device(tb, 'server_1')

cml0 = Cml()
pcap0 = Pcap(cml0, ini.iosv_0.__name__, ini.iosv_1.__name__)
pcap1 = Pcap(cml0, ini.iosv_1.__name__, ini.iosv_2.__name__)

print("####### exec #######")
# set ip
server_0.execs([
  # eth0 setting
  ## disable DHCP
  f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
  f"sudo ifconfig eth0 {ini.server_0.eth0.ip_addr} netmask {ini.server_0.eth0.subnet_mask} up",
  f"sudo route add default gw {ini.iosv_0.g0_1.ip_addr}",
  f"ifconfig eth0"
])

server_1.execs([
  # eth0 setting
  ## disable DHCP
  f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
  f"sudo ifconfig eth0 {ini.server_1.eth0.ip_addr} netmask {ini.server_1.eth0.subnet_mask} up",
  f"sudo route add default gw {ini.iosv_1.g0_1.ip_addr}",
  f"ifconfig eth0"
])

# interface up
iosv_0.execs([
  [
    f"interface {ini.iosv_0.g0_0.name}",
    f"ip addr {ini.iosv_0.g0_0.ip_addr} {ini.iosv_0.g0_0.subnet_mask}",
    f"no shutdown"
  ],
  [
    f"interface {ini.iosv_0.g0_1.name}",
    f"ip addr {ini.iosv_0.g0_1.ip_addr} {ini.iosv_0.g0_1.subnet_mask}",
    f"no shutdown"
  ],
  [
    f"interface {ini.iosv_0.loopback0.name}",
    f"ip addr {ini.iosv_0.loopback0.ip_addr} {ini.iosv_0.loopback0.subnet_mask}",
    #f"no shutdown"
  ],
])

iosv_1.execs([
  [
    f"interface {ini.iosv_1.g0_0.name}",
    f"ip addr {ini.iosv_1.g0_0.ip_addr} {ini.iosv_1.g0_0.subnet_mask}",
    f"no shutdown"
  ],
  [
    f"interface {ini.iosv_1.g0_1.name}",
    f"ip addr {ini.iosv_1.g0_1.ip_addr} {ini.iosv_1.g0_1.subnet_mask}",
    f"no shutdown"
  ],
  [
    f"interface {ini.iosv_1.loopback0.name}",
    f"ip addr {ini.iosv_1.loopback0.ip_addr} {ini.iosv_1.loopback0.subnet_mask}",
    #f"no shutdown"
  ],
])

iosv_2.execs([
  [
    f"interface {ini.iosv_2.g0_0.name}",
    f"ip addr {ini.iosv_2.g0_0.ip_addr} {ini.iosv_2.g0_0.subnet_mask}",
    f"no shutdown"
  ],
  [
    f"interface {ini.iosv_2.g0_1.name}",
    f"ip addr {ini.iosv_2.g0_1.ip_addr} {ini.iosv_2.g0_1.subnet_mask}",
    f"no shutdown"
  ],
  [
    f"interface {ini.iosv_2.loopback0.name}",
    f"ip addr {ini.iosv_2.loopback0.ip_addr} {ini.iosv_2.loopback0.subnet_mask}",
    #f"no shutdown"
  ],
])

# ospf setting
pcap0.start(maxpackets=500)
pcap1.start(maxpackets=500)

iosv_0_g0_0_network0 = ipv4.get_network0(ini.iosv_0.g0_0.ip_addr, ini.iosv_0.g0_0.subnet_mask)
iosv_0_g0_1_network0 = ipv4.get_network0(ini.iosv_0.g0_1.ip_addr, ini.iosv_0.g0_1.subnet_mask)
area_id = 0 #backbone area
iosv_0.execs([
  [
    f"router ospf {ini.ospf_process_id}",
    # ループバックインターフェイスでOSPFを有効にしない設定 -> 他のルータがloopback interfaceを認識しない
    f"network {iosv_0_g0_0_network0} {ini.INVERSE_MASK_24} area {ini.iosv_0.g0_0.area_id}",
    f"network {iosv_0_g0_1_network0} {ini.INVERSE_MASK_24} area {ini.iosv_0.g0_1.area_id}",
  ],
])

iosv_1_g0_0_network0 = ipv4.get_network0(ini.iosv_1.g0_0.ip_addr, ini.iosv_1.g0_0.subnet_mask)
iosv_1_g0_1_network0 = ipv4.get_network0(ini.iosv_1.g0_1.ip_addr, ini.iosv_1.g0_1.subnet_mask)
iosv_1.execs([
  [
    f"router ospf {ini.ospf_process_id}",
    f"network {iosv_1_g0_0_network0} {ini.INVERSE_MASK_24} area {ini.iosv_1.g0_0.area_id}",
    f"network {iosv_1_g0_1_network0} {ini.INVERSE_MASK_24} area {ini.iosv_1.g0_1.area_id}",
  ],
])

iosv_2_g0_0_network0 = ipv4.get_network0(ini.iosv_2.g0_0.ip_addr, ini.iosv_2.g0_0.subnet_mask)
iosv_2_g0_1_network0 = ipv4.get_network0(ini.iosv_2.g0_1.ip_addr, ini.iosv_2.g0_1.subnet_mask)
iosv_2.execs([
  [
    f"router ospf {ini.ospf_process_id}",
    f"network {iosv_2_g0_0_network0} {ini.INVERSE_MASK_24} area {ini.iosv_2.g0_0.area_id}",
    f"network {iosv_2_g0_1_network0} {ini.INVERSE_MASK_24} area {ini.iosv_2.g0_1.area_id}",
  ],
])

# check "show ip route"
wait_until.populate_ospf(iosv_0, count=2)
wait_until.populate_ospf(iosv_1, count=2)
wait_until.populate_ospf(iosv_2, count=2)


iosv_0.execs([
  # neighbor table
  f"show running-config | section router ospf {ini.ospf_process_id}",
  f"show ip ospf neighbor",
  # LSDB(topology)
  f"show ip ospf database",
  # routing table
  f"show ip route",
  f"show ip protocols",
  f"show ip ospf interface brief",
  f"show ip ospf interface {ini.iosv_0.g0_0.name}",
])

iosv_1.execs([
  f"show running-config | section router ospf {ini.ospf_process_id}",
  f"show ip ospf neighbor",
  # LSDB(topology)
  f"show ip ospf database",
  f"show ip route",
  f"show ip protocols",
  f"show ip ospf interface brief",
  f"show ip ospf interface {ini.iosv_1.g0_0.name}",
  f"show ip ospf interface {ini.iosv_1.g0_1.name}",
])

iosv_2.execs([
  f"show running-config | section router ospf {ini.ospf_process_id}",
  f"show ip ospf neighbor",
  # LSDB(topology)
  f"show ip ospf database",
  f"show ip route",
  f"show ip protocols",
  f"show ip ospf interface brief",
  f"show ip ospf interface {ini.iosv_2.g0_0.name}",
])

pcap0.stop(); pcap0.download(file=ini.pcap0_file)
pcap1.stop(); pcap1.download(file=ini.pcap1_file)
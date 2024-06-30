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
server_0 = Device(tb, 'server_0')
server_1 = Device(tb, 'server_1')

cml0 = Cml()
pcap = Pcap(Cml(), ini.switch_0.__name__, ini.iosv_0.__name__)


print("####### exec #######")

# server settings -> DHCP enable by default

# interface up
iosv_0.execs([
  [
    f"interface {ini.iosv_0.g0_0.name}",
    f"ip addr {ini.iosv_0.g0_0.ip_addr} {ini.iosv_0.g0_0.subnet_mask}",
    f"no shutdown",
  ],
  [
    f"interface {ini.iosv_0.g0_1.name}",
    f"ip addr {ini.iosv_0.g0_1.ip_addr} {ini.iosv_0.g0_1.subnet_mask}",
    f"no shutdown",
  ]
])

iosv_1.execs([
  [
    f"interface {ini.iosv_1.g0_0.name}",
    f"ip addr {ini.iosv_1.g0_0.ip_addr} {ini.iosv_1.g0_0.subnet_mask}",
    f"no shutdown",
  ],
])

wait_until.populate_up(iosv_0, 2)
wait_until.populate_up(iosv_1, 1)

# show mac address
show.mac_ip(iosv_0)
show.mac_ip(iosv_1)

# routing
g0_0_network0 = ipv4.get_network0(ini.iosv_0.g0_0.ip_addr, ini.iosv_0.g0_0.subnet_mask)
iosv_1.execs([
  [
    # DHCP offser and ack is unicast, so we have to set routing for server network
    f"ip route {g0_0_network0} {ini.iosv_0.g0_0.subnet_mask} {ini.iosv_0.g0_1.ip_addr}"
  ]
])

# dhcp server setting
## relay agent
pcap.start(maxpackets=300)
iosv_0.execs([
  [
    f"interface {ini.iosv_0.g0_0.name}",
    f"ip helper-address {ini.iosv_1.g0_0.ip_addr}",
  ]
])

g0_0_network0 = ipv4.get_network0(ini.iosv_0.g0_0.ip_addr, ini.iosv_0.g0_0.subnet_mask)
iosv_1.execs([
  [
    f"ip dhcp pool {ini.dhcp_pool_name}",
    f"network {g0_0_network0} {ini.iosv_0.g0_0.subnet_mask}",
    # default gw on servers
    f"default-router {ini.iosv_0.g0_0.ip_addr}",
    # optional
    #f"lease 10",
    #f"dns-server {dns_ip_addr}",
  ],
  [
    f"ip dhcp excluded-address {ini.iosv_0.g0_0.ip_addr}",
    # Cisco IOSをDHCPサーバとして稼動させていて、DHCPデータベースエージェントとして設定しない場合、次のように設定することが推奨
    f"no ip dhcp conflict logging",
  ],
])
# wait until dhcp populate
wait_until.populate_server_ping(server_0, ini.iosv_1.g0_0.ip_addr)
wait_until.populate_server_ping(server_1, ini.iosv_1.g0_0.ip_addr)
pcap.stop(); pcap.download(file=ini.pcap_file)

iosv_1.execs([
  f"show ip dhcp pool",
  f"show ip dhcp binding",
  f"show ip dhcp conflict",
])

# check
server_0.execs([
  f"ifconfig eth0",
  f"route -e",
])
server_1.execs([
  f"ifconfig eth0",
  f"route -e",
])
from genie import testbed
from cml import CONFIG_YAML, Cml, Pcap
from lib.device import Device
from lib import wait, ipv4
import ini
import time
import wait_until


tb = testbed.load(CONFIG_YAML)
pcap = Pcap(Cml(), ini.server_0.__name__, ini.iosvl2_0.__name__)

# tinylinux
server_0 = Device(tb, 'server_0')
server_1 = Device(tb, 'server_1')

# router
iosv_0 = Device(tb, 'iosv_0') # as DHCP server
iosv_1 = Device(tb, 'iosv_1') # as DHCP client
iosvl2_0 = Device(tb, 'iosvl2_0')



print("####### exec #######")

pcap.start(maxpackets=500)

# up
iosv_0.execs([
  [
    f"interface {ini.iosv_0.g0_0.name}",
    f"ip addr {ini.iosv_0.g0_0.ip_addr} {ini.iosv_0.g0_0.subnet_mask}",
    f"no shutdown"
  ],
])

wait_until.populate_up(iosv_0, 1)

## dhcp client setting
iosv_1.execs([
  [
    f"interface {ini.iosv_1.g0_0.name}",
    f"ip address dhcp",
    f"no shutdown"
  ]
])

# dhcp server setting
dhcp_pool_name = "DHCPPOOL"
router0_ipv4 = ipv4.get_network0(ini.iosv_0.g0_0.ip_addr, ini.iosv_0.g0_0.subnet_mask)
iosv_0.execs([
  [
    f"ip dhcp pool {dhcp_pool_name}",
    f"network {router0_ipv4} {ini.iosv_0.g0_0.subnet_mask}",
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
  # relay agent settings
  # [
  #   f"interface {ini.iosv_0.g0_0.name}",
  #   f"ip helper-address {dhcp_server_ip_addr}",
  # ]
])
# wait until dhcp populate
wait_until.seconds(5)

iosv_0.execs([
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
## check as dhcp client
iosv_1.execs([
  f"show ip interface brief",
  f"show interfaces {ini.iosv_1.g0_0.name}",
  f"show dhcp lease",
  # check default route automatically
  f"show ip route",
])

wait_until.seconds(3)
pcap.stop()
pcap.download(ini.pcap_file)
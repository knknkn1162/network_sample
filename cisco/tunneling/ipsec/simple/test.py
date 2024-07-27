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
pcap = Pcap(cml0, ini.iosv_0.__name__, ini.iosv_1.__name__)

print("####### exec #######")
# set ip
server_0.execs([
  # eth0 setting
  ## disable DHCP
  f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
  f"sudo ifconfig eth0 {ini.server_0.eth0.ip_addr} netmask {ini.server_0.eth0.subnet_mask} up",
  f"sudo route add default gw {ini.iosv_0.g0_0.ip_addr}",
  f"ifconfig eth0",
  f"route -e",
])

server_1.execs([
  # eth0 setting
  ## disable DHCP
  f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
  f"sudo ifconfig eth0 {ini.server_1.eth0.ip_addr} netmask {ini.server_1.eth0.subnet_mask} up",
  f"sudo route add default gw {ini.iosv_1.g0_0.ip_addr}",
  f"ifconfig eth0",
  f"route -e",
])

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
  ],
  # default gw
  [
    f"ip route 0.0.0.0 0.0.0.0 {ini.iosv_1.g0_1.ip_addr}",
  ]
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
  # default gw
  [
    f"ip route 0.0.0.0 0.0.0.0 {ini.iosv_0.g0_1.ip_addr}",
  ]
])

# it works
wait_until.populate_server_ping(server_0, ini.server_1.eth0.ip_addr)

server_0_network0 = ipv4.get_network0(ini.server_0.eth0.ip_addr, ini.server_0.eth0.subnet_mask)
server_1_network0 = ipv4.get_network0(ini.server_1.eth0.ip_addr, ini.server_1.eth0.subnet_mask)
iosv_0.execs([
  # ike phase 1
  [
    f"crypto isakmp policy {ini.priority}",
    ## authentication
    f"authentication pre-share",
    ## crypto algothrism
    #f"encryption 3des",
    ## hash algorithm
    #f"hash sha",
    ## lifetime in ISAKMP SA
    #f"lifetime 43200",
    ## DH group
    f"group {ini.dh_group}",
  ],
  [
    # 0: Specifies an UNENCRYPTED password will follow
    f"crypto isakmp key {ini.preshared_key} address {ini.iosv_1.g0_1.ip_addr}",
    ## DPD(optional)
    #f"crypto isakmp keepalive 30 periodic",
  ],
  # ike phase 2
  [
    ## crypto algo, hash algo, ID?
    f"crypto ipsec transform-set {ini.transform_label} {ini.crypto_algo} {ini.hash_algo}",
    ## lifetime in IPsec SA
    #f"crypto ipsec security-association lifetime seconds 41200",
    ## dh group, PFS
    #f"set pfs group{ini.dh_group}",
  ],
  [
    # access-list {ini.acl_num} permit ip {src} {src_mask} {dst} {dst_mask}
    f"access-list {ini.acl_num} permit ip {server_0_network0} {ini.INVERSE_MASK_24} {server_1_network0} {ini.INVERSE_MASK_24}",
  ],
  [
    f"crypto map {ini.crypto_map_label} {ini.seq_number} ipsec-isakmp",
    # set access-list
    f"match address {ini.acl_num}",
    f"set peer {ini.iosv_1.g0_1.ip_addr}",
    f"set transform-set {ini.transform_label}",
  ],
])

iosv_1.execs([
  # ike phase 1
  [
    f"crypto isakmp policy {ini.priority}",
    ## authentication
    f"authentication pre-share",
    f"group {ini.dh_group}",
  ],
  [
    f"crypto isakmp key {ini.preshared_key} address {ini.iosv_0.g0_1.ip_addr}",
  ],
  # ike phase 2
  [
    f"crypto ipsec transform-set {ini.transform_label} {ini.crypto_algo} {ini.hash_algo}",
  ],
  [
    # access-list {ini.acl_num} permit ip {src} {src_mask} {dst} {dst_mask}
    f"access-list {ini.acl_num} permit ip {server_1_network0} {ini.INVERSE_MASK_24} {server_0_network0} {ini.INVERSE_MASK_24}",
  ],
  [
    f"crypto map {ini.crypto_map_label} {ini.seq_number} ipsec-isakmp",
    # set access-list
    f"match address {ini.acl_num}",
    f"set peer {ini.iosv_0.g0_1.ip_addr}",
    f"set transform-set {ini.transform_label}",
  ],
])


# apply
pcap.start(maxpackets=500)
iosv_0.execs([
  [
    f"interface {ini.iosv_0.g0_1.name}",
    f"crypto map {ini.crypto_map_label}",
  ]
])

iosv_1.execs([
  [
    f"interface {ini.iosv_1.g0_1.name}",
    f"crypto map {ini.crypto_map_label}",
  ]
])

wait_until.populate_server_ping(server_0, ini.server_1.eth0.ip_addr)

pcap.stop(); pcap.download(file=ini.pcap_file)

iosv_0.execs([
  f"show crypto isakmp policy",
  f"show crypto isakmp sa",
])

iosv_1.execs([
  f"show crypto isakmp policy",
  f"show crypto isakmp sa",
])

iosv_0.execs([
  f"show crypto ipsec transform-set",
  f"show crypto map",
  f"show crypto session detail",
  f"show crypto ipsec sa",
])

iosv_1.execs([
  f"show crypto ipsec transform-set",
  f"show crypto map",
  f"show crypto session detail",
  f"show crypto ipsec sa",
])
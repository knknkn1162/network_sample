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



print("####### exec #######")
server_0.execs([
  # eth0 setting
  ## disable DHCP
  f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
  f"sudo ifconfig eth0 {ini.server_0.eth0.ip_addr} netmask {ini.server_0.eth0.subnet_mask} up",
  f"sudo route add default gw {ini.iosv_0.g0_0.ip_addr}",
  f"ifconfig eth0",
])

server_1.execs([
  # eth0 setting
  ## disable DHCP
  f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
  f"sudo ifconfig eth0 {ini.server_1.eth0.ip_addr} netmask {ini.server_1.eth0.subnet_mask} up",
  f"sudo route add default gw {ini.iosv_1.g0_0.ip_addr}",
  f"ifconfig eth0",
])

## up
iosv_0.execs([
  [
    f"interface {ini.iosv_0.g0_0.name}",
    f"ip addr {ini.iosv_0.g0_0.ip_addr} {ini.iosv_0.g0_0.subnet_mask}",
    f"ip nat inside",
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

## pppoe client
iosv_0.execs([
  # Dialerインターフェースを作成して、カプセル化タイプ、認証方式、ダイヤラプールなどの設定を行い、これをEthernetポートに関連づける
  [
    f"interface {ini.iosv_0.dialer1.name}",
    # ダイヤラインターフェースに割り当てるIPアドレスをPPP（IPCP）で自動取得
    f"ip address negotiated",
    f"encapsulation ppp",
    f"dialer pool {ini.iosv_0.dialer1.pool}",
    f"dialer-group {ini.iosv_0.dialer1.group}",
    # プロバイダ側(サーバー側)でのみ認証
    f"ppp authentication chap callin",
    f"ppp chap hostname {ini.iosv_1.chap_hostname}",
    f"ppp chap password {ini.chap_password}",
    f"ip nat outside",
  ],
  [
    # 「dialer-list」でPPPoEセッション開始のトリガーとなる対象トラフィックを指定する
    f"dialer-list {ini.iosv_0.dialer1.group} protocol ip permit"
  ],
])

num = 1
server_0_network0 = ipv4.get_network0(ini.server_0.eth0.ip_addr, ini.server_0.eth0.subnet_mask)
iosv_0.execs([
  [
    f"ip route 0.0.0.0 0.0.0.0 {ini.iosv_0.dialer1.name}",
    # napt settings
    f"ip nat inside source list {num} interface {ini.iosv_0.dialer1.name} overload",
    f"access-list {num} permit {server_0_network0} {ini.INVERSE_MASK_24}",
  ],
])


iosv_0.execs([
  [
    f"interface {ini.iosv_0.g0_1.name}",
    # IPアドレスをPPP（IPCP）で自動取得
    f"no ip address",
    f"pppoe enable",
    f"pppoe-client dial-pool-number {ini.iosv_0.dialer1.pool}",
    f"no shutdown",
  ],
])

### pppoe server

iosv_1.execs([
  [
    f"username {ini.iosv_1.chap_hostname} password {ini.chap_password}",
  ],
  [
    f"interface {ini.iosv_1.loopback0.name}",
    f"ip address {ini.iosv_1.loopback0.ip_addr} {ini.iosv_1.loopback0.subnet_mask}"
  ],
])

iosv_1.execs([
  [
    f"interface {ini.iosv_1.vtemplate1.name}",
    # WAN側（インターネット接続側）に割り振られるIPアドレスをなし（unnumbered）にする
    f"ip unnumbered {ini.iosv_1.loopback0.name}",
    f"peer default ip address pool {ini.iosv_1.vtemplate1.pool_name}",
    f"ppp authentication chap",
  ],
  [
    f"ip local pool {ini.iosv_1.vtemplate1.pool_name} {ini.iosv_1.vtemplate1.from_ip_addr} {ini.iosv_1.vtemplate1.to_ip_addr}",
  ],
  [
    f"bba-group pppoe {ini.iosv_1.g0_1.pppoe_group_name}",
    # association between pppoe <-> virtual template
    f"{ini.iosv_1.vtemplate1.name}",
  ],
  [
    f"interface {ini.iosv_1.g0_1.name}",
    f"no ip address",
    f"pppoe enable group {ini.iosv_1.g0_1.pppoe_group_name}",
    f"no shutdown",
  ]
])


wait_until.populate_server_ping(server_0, ini.server_1.eth0.ip_addr, count=15)

show.mac_ip(iosv_0)
iosv_0.execs([
  # cannot parse in "ios" type
  f"show pppoe session",
  f"show ip interface brief",
  f"show ip route",
])

show.mac_ip(iosv_1)
iosv_1.execs([
  f"show pppoe session",
  f"show ip interface brief",
  f"show ip route",
])

iosv_0.execs([
  f"show ip nat translations",
  f"show ip access-lists",
])

iosv_1.execs([
  f"show ip nat translations",
  f"show ip access-lists",
])
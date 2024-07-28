from genie import testbed
from cmlmag.cml import CONFIG_YAML, Cml
from cmlmag.device import Device
from cmlmag import wait, ipv4
import cmlmag.parse as parse
import cmlmag.wait_until as wait_until
import ini

def main():
  tb = testbed.load(CONFIG_YAML)
  # switch
  iosv_0 = Device(tb, ini.iosv_0.__name__)
  iosv_1 = Device(tb, ini.iosv_1.__name__)
  iosv_2 = Device(tb, ini.iosv_2.__name__)

  server_0 = Device(tb, ini.server_0.__name__)
  server_1 = Device(tb, ini.server_1.__name__)
  print("####### exec #######")
  cml = Cml()
  pcap01 = cml.lab.create_pcap(iosv_0.name, iosv_1.name, auth_token=cml.auth_token)
  pcap02 = cml.lab.create_pcap(server_0.name, iosv_0.name, auth_token=cml.auth_token)

  # server setup
  server_0.execs([
    # eth0 setting
    ## disable DHCP
    f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
    f"sudo ifconfig eth0 {ini.server_0.eth0.ip_addr.ip} netmask {ini.server_0.eth0.ip_addr.netmask} up",
    f"sudo route add default gw {ini.iosv_0.g0_1.ip_addr.ip}",
    f"ifconfig eth0",
    f"route -e",
  ])

  # server setup
  server_1.execs([
    # eth0 setting
    ## disable DHCP
    f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
    f"sudo ifconfig eth0 {ini.server_1.eth0.ip_addr.ip} netmask {ini.server_1.eth0.ip_addr.netmask} up",
    f"sudo route add default gw {ini.iosv_2.g0_1.ip_addr.ip}",
    f"ifconfig eth0",
    f"route -e",
  ])

  ## up
  iosv_0.execs([
    [
      f"interface {ini.iosv_0.g0_0.name}",
      # unnumbered
      f"no ip address",
      f"no shutdown",
    ],
    [
      f"interface {ini.iosv_0.g0_1.name}",
      #f"no ip address",
      f"ip addr {ini.iosv_0.g0_1.ip_addr.ip} {ini.iosv_0.g0_1.ip_addr.netmask}",
      f"no shutdown",
    ],
    # for PPPoE
    [
      f"interface {ini.iosv_0.loopback0.name}",
      f"ip addr {ini.iosv_0.loopback0.ip_addr.ip} {ini.iosv_0.loopback0.ip_addr.netmask}",
      f"no shutdown",
    ],
  ])

  iosv_1.execs([
    [
      f"interface {ini.iosv_1.g0_0.name}",
      f"no ip address",
      #f"ip addr {ini.iosv_1.g0_0.ip_addr.ip} {ini.iosv_1.g0_0.ip_addr.netmask}",
      f"no shutdown",
    ],
    [
      f"interface {ini.iosv_1.g0_1.name}",
      f"no ip address",
      #f"ip addr {ini.iosv_1.g0_1.ip_addr.ip} {ini.iosv_1.g0_1.ip_addr.netmask}",
      f"no shutdown",
    ],
    [
      f"interface {ini.iosv_1.loopback0.name}",
      f"ip addr {ini.iosv_1.loopback0.ip_addr.ip} {ini.iosv_1.loopback0.ip_addr.netmask}",
      f"no shutdown",
    ],
  ])

  iosv_2.execs([
    [
      f"interface {ini.iosv_2.g0_0.name}",
      # unnumbered
      f"no ip address",
      f"no shutdown",
    ],
    [
      f"interface {ini.iosv_2.g0_1.name}",
      #f"no ip address",
      f"ip addr {ini.iosv_2.g0_1.ip_addr.ip} {ini.iosv_2.g0_1.ip_addr.netmask}",
      f"no shutdown",
    ],
    # for PPPoE
    [
      f"interface {ini.iosv_2.loopback0.name}",
      f"ip addr {ini.iosv_2.loopback0.ip_addr.ip} {ini.iosv_2.loopback0.ip_addr.netmask}",
      f"no shutdown",
    ],
  ])

  iosv_0.show_mac_ip()
  iosv_1.show_mac_ip()
  iosv_2.show_mac_ip()

  ############### PPPoE ##################
   # as server
  iosv_1.execs([
    [
      f"interface {ini.iosv_1.g0_0.name}",
      f"pppoe enable group {ini.iosv_1.bba_group_name01}",
    ],
    [
      f"bba-group pppoe {ini.iosv_1.bba_group_name01}",
      f"{ini.iosv_1.vt1.name}",
    ],
    [
      f"interface {ini.iosv_1.vt1.name}",
      f"ip unnumbered {ini.iosv_1.loopback0.name}",
    ],
  ])
  iosv_1.execs([
    [
      f"interface {ini.iosv_1.g0_1.name}",
      f"pppoe enable group {ini.iosv_1.bba_group_name02}",
    ],
    [
      f"bba-group pppoe {ini.iosv_1.bba_group_name02}",
      f"{ini.iosv_1.vt2.name}",
    ],
    [
      f"interface {ini.iosv_1.vt2.name}",
      f"ip unnumbered {ini.iosv_1.loopback1.name}",
    ],
  ])

  # client
  iosv_0.execs([
    [
      f"interface {ini.iosv_0.g0_0.name}",
      f"pppoe enable",
      f"pppoe-client dial-pool-number {ini.iosv_0.dialer0.pool_num}",
    ],
    # dialer settings
    [
      f"interface {ini.iosv_0.dialer0.name}",
      f"encapsulation ppp",
      f"dialer pool {ini.iosv_0.dialer0.pool_num}",
      f"ip unnumbered {ini.iosv_0.loopback0.name}",
    ],
  ])

  iosv_2.execs([
    [
      f"interface {ini.iosv_2.g0_0.name}",
      f"pppoe enable",
      f"pppoe-client dial-pool-number {ini.iosv_2.dialer0.pool_num}",
    ],
    # dialer settings
    [
      f"interface {ini.iosv_2.dialer0.name}",
      f"encapsulation ppp",
      f"dialer pool {ini.iosv_2.dialer0.pool_num}",
      f"ip unnumbered {ini.iosv_2.loopback0.name}",
    ],
  ])

  # routing
  iosv_0.execs([
    [
      f"ip route 0.0.0.0 0.0.0.0 {ini.iosv_0.dialer0.name}"
    ]
  ])

  iosv_2.execs([
    [
      f"ip route 0.0.0.0 0.0.0.0 {ini.iosv_2.dialer0.name}"
    ]
  ])

  ############### ipsec ##################
  ## IKE phase 1
  iosv_0.execs([
    [
      f"crypto isakmp policy {ini.ipsec.phase1.ipsec_priority}",
      #f"encryption des",
      #f"hash sha",
      #f"lifetime 86400",
      f"group {ini.ipsec.phase1.dh_group}",
      f"authentication pre-share",
      f"crypto isakmp key {ini.ipsec.phase1.preshared_key} address {ini.iosv_2.loopback0.ip_addr.ip}",
      f"crypto isakmp keepalive 30 periodic",
    ],
  ])

  iosv_2.execs([
    [
      f"crypto isakmp policy {ini.ipsec.phase1.ipsec_priority}",
      #f"encryption des",
      #f"hash sha",
      #f"lifetime 86400",
      f"group {ini.ipsec.phase1.dh_group}",
      f"authentication pre-share",
      f"crypto isakmp key {ini.ipsec.phase1.preshared_key} address {ini.iosv_0.loopback0.ip_addr.ip}",
      f"crypto isakmp keepalive 30 periodic",
    ],
  ])

  ## IKE phase 2
  iosv_0.execs([
    [
      f"crypto ipsec transform-set {ini.ipsec.phase2.transform_set.label} {ini.ipsec.phase2.transform_set.crypto_param} {ini.ipsec.phase2.transform_set.sig_param}",
      #f"mode tunnel",
    ],
    [
      #f"crypto ipsec security-association lifetime seconds 3600",
      f"access-list {ini.ipsec.phase2.acl_num} permit ip any any",
      # mapping
      f"crypto map {ini.ipsec.phase2.crypto_map.label} {ini.ipsec.phase2.crypto_map.seq_num} ipsec-isakmp",
      f"match address {ini.ipsec.phase2.acl_num}",
      f"set peer {ini.iosv_2.loopback0.ip_addr.ip}",
      f"set transform-set {ini.ipsec.phase2.transform_set.label}",
    ]
  ])

  iosv_2.execs([
    [
      f"crypto ipsec transform-set {ini.ipsec.phase2.transform_set.label} {ini.ipsec.phase2.transform_set.crypto_param} {ini.ipsec.phase2.transform_set.sig_param}",
      #f"mode tunnel",
    ],
    [
      #f"crypto ipsec security-association lifetime seconds 3600",
      f"access-list {ini.ipsec.phase2.acl_num} permit ip any any",
      # mapping
      f"crypto map {ini.ipsec.phase2.crypto_map.label} {ini.ipsec.phase2.crypto_map.seq_num} ipsec-isakmp",
      f"match address {ini.ipsec.phase2.acl_num}",
      f"set peer {ini.iosv_0.loopback0.ip_addr.ip}",
      f"set transform-set {ini.ipsec.phase2.transform_set.label}",
    ]
  ])

  ### apply crypto_map to interface
  iosv_0.execs([
    [
      f"interface {ini.iosv_0.dialer0.name}",
      f"crypto map {ini.ipsec.phase2.crypto_map.label}",
    ]
  ])

  iosv_2.execs([
    [
      f"interface {ini.iosv_2.dialer0.name}",
      f"crypto map {ini.ipsec.phase2.crypto_map.label}",
    ]
  ])

  ############### CHECK ##################
  def populate_server_ping(device: Device, target_ip: str):
    @wait.retry(count=30, result=0, sleep_time=5)
    def _do(device: Device):
      return device.server_ping(target_ip)
    return _do(device)

  populate_server_ping(server_0, ini.server_1.eth0.ip_addr.ip)

  iosv_0.execs([
    # IKE phase 1
    f"show crypto isakmp sa",
    f"show crypto ipsec sa",
    f"show pppoe session",
    f"show pppoe session all",
  ])

  iosv_2.execs([
    # IKE phase 2
    f"show crypto isakmp sa",
    f"show crypto ipsec sa",
    f"show pppoe session",
    f"show pppoe session all",
  ])

  iosv_0.execs([
    f"show crypto ipsec transform-set",
    f"show crypto map",
    f"show crypto session detail",
  ])

  iosv_2.execs([
    f"show crypto ipsec transform-set",
    f"show crypto map",
    f"show crypto session detail",
  ])

  pcap01.start(maxpackets=100)
  pcap02.start(maxpackets=100)
  server_0.server_ping(ini.server_1.eth0.ip_addr.ip)
  pcap01.download(file=ini.pcap01_file)
  pcap02.download(file=ini.pcap02_file)


if __name__ == '__main__':
  main()
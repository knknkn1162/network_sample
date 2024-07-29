from genie import testbed
from cmlmag.cml import CONFIG_YAML, Cml
from cmlmag.device import Device
from cmlmag import wait, ipv4
import cmlmag.parse as parse
import cmlmag.wait_until as wait_until
import ini
from cmlmag.structure.stp_info import (
  Role as StpRole,
  State as StpState
)

def main():
  tb = testbed.load(CONFIG_YAML)
  # switch
  iosv_0 = Device(tb, ini.iosv_0.__name__)
  iosv_1 = Device(tb, ini.iosv_1.__name__)

  server_0 = Device(tb, ini.server_0.__name__)
  server_1 = Device(tb, ini.server_1.__name__)
  server_2 = Device(tb, ini.server_2.__name__)
  server_3 = Device(tb, ini.server_3.__name__)
  print("####### exec #######")

  cml = Cml()
  pcap = cml.lab.create_pcap(iosv_0.name, iosv_1.name, auth_token=cml.auth_token)

  # server setup
  server_0.execs([
    # eth0 setting
    ## disable DHCP
    f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
    f"sudo ifconfig eth0 {ini.server_0.eth0.ip_addr.ip} netmask {ini.server_0.eth0.ip_addr.netmask} up",
    f"sudo route add default gw {ini.iosv_0.g0_0.ip_addr.ip}",
    f"ifconfig eth0",
    f"route -e",
  ])

  server_1.execs([
    # eth0 setting
    ## disable DHCP
    f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
    f"sudo ifconfig eth0 {ini.server_1.eth0.ip_addr.ip} netmask {ini.server_1.eth0.ip_addr.netmask} up",
    f"sudo route add default gw {ini.iosv_0.g0_1.ip_addr.ip}",
    f"ifconfig eth0",
    f"route -e",
  ])

  server_2.execs([
    # eth0 setting
    ## disable DHCP
    f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
    f"sudo ifconfig eth0 {ini.server_2.eth0.ip_addr.ip} netmask {ini.server_2.eth0.ip_addr.netmask} up",
    f"sudo route add default gw {ini.iosv_1.g0_0.ip_addr.ip}",
    f"ifconfig eth0",
    f"route -e",
  ])

  server_3.execs([
    # eth0 setting
    ## disable DHCP
    f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
    f"sudo ifconfig eth0 {ini.server_3.eth0.ip_addr.ip} netmask {ini.server_3.eth0.ip_addr.netmask} up",
    f"sudo route add default gw {ini.iosv_1.g0_1.ip_addr.ip}",
    f"ifconfig eth0",
    f"route -e",
  ])

  # vrf setting first
  # VRF-lite setting
  iosv_0.execs([
    [
      f"ip vrf {ini.site_a.name}",
      f"rd {ini.site_a.rd}",
    ],
    [
      f"ip vrf {ini.site_b.name}",
      f"rd {ini.site_b.rd}",
    ],
    [
      f"interface {ini.iosv_0.g0_0.name}",
      f"ip vrf forwarding {ini.iosv_0.g0_0.site.name}",
    ],
    [
      f"interface {ini.iosv_0.g0_1.name}",
      f"ip vrf forwarding {ini.iosv_0.g0_1.site.name}",
    ],
    [
      f"interface {ini.iosv_0.g0_2.name}.{ini.iosv_0.g0_2.sub0.num}",
      f"ip vrf forwarding {ini.iosv_0.g0_2.sub0.site.name}",
    ],
    [
      f"interface {ini.iosv_0.g0_2.name}.{ini.iosv_0.g0_2.sub1.num}",
      f"ip vrf forwarding {ini.iosv_0.g0_2.sub1.site.name}",
    ],
  ])

  iosv_1.execs([
    [
      f"ip vrf {ini.site_a.name}",
      f"rd {ini.site_a.rd}",
    ],
    [
      f"ip vrf {ini.site_b.name}",
      f"rd {ini.site_b.rd}",
    ],
    [
      f"interface {ini.iosv_1.g0_0.name}",
      f"ip vrf forwarding {ini.iosv_1.g0_0.site.name}",
    ],
    [
      f"interface {ini.iosv_1.g0_1.name}",
      f"ip vrf forwarding {ini.iosv_1.g0_1.site.name}",
    ],
    [
      f"interface {ini.iosv_1.g0_2.name}.{ini.iosv_1.g0_2.sub0.num}",
      f"ip vrf forwarding {ini.iosv_1.g0_2.sub0.site.name}",
    ],
    [
      f"interface {ini.iosv_1.g0_2.name}.{ini.iosv_1.g0_2.sub1.num}",
      f"ip vrf forwarding {ini.iosv_1.g0_2.sub1.site.name}",
    ],
  ])

  ## up
  iosv_0.execs([
    [
      f"interface {ini.iosv_0.g0_0.name}",
      f"ip addr {ini.iosv_0.g0_0.ip_addr.ip} {ini.iosv_0.g0_0.ip_addr.netmask}",
      f"no shutdown",
    ],
    [
      f"interface {ini.iosv_0.g0_1.name}",
      # if vrf setting later, <ip_addr> overlaps with ..
      f"ip addr {ini.iosv_0.g0_1.ip_addr.ip} {ini.iosv_0.g0_1.ip_addr.netmask}",
      f"no shutdown",
    ],
    [
      f"interface {ini.iosv_0.g0_2.name}",
      f"no ip address",
      f"no shutdown",
    ],
    [
      f"interface {ini.iosv_0.g0_2.name}.{ini.iosv_0.g0_2.sub0.num}",
      # Configuring IP routing on a LAN subinterface is only allowed if that 
      # subinterface is already configured as part of an IEEE 802.10, IEEE 802.1Q, 
      # or ISL vLAN
      f"encapsulation dot1Q {ini.iosv_0.g0_2.sub0.num}",
      f"ip addr {ini.iosv_0.g0_2.sub0.ip_addr.ip} {ini.iosv_0.g0_2.sub0.ip_addr.netmask}",
      f"no shutdown",
    ],
    [
      f"interface {ini.iosv_0.g0_2.name}.{ini.iosv_0.g0_2.sub1.num}",
      f"encapsulation dot1Q {ini.iosv_0.g0_2.sub1.num}",
      f"ip addr {ini.iosv_0.g0_2.sub1.ip_addr.ip} {ini.iosv_0.g0_2.sub1.ip_addr.netmask}",
      f"no shutdown",
    ],
  ])

  iosv_1.execs([
    [
      f"interface {ini.iosv_1.g0_0.name}",
      f"ip addr {ini.iosv_1.g0_0.ip_addr.ip} {ini.iosv_1.g0_0.ip_addr.netmask}",
      f"no shutdown",
    ],
    [
      f"interface {ini.iosv_1.g0_1.name}",
      f"ip addr {ini.iosv_1.g0_1.ip_addr.ip} {ini.iosv_1.g0_1.ip_addr.netmask}",
      f"no shutdown",
    ],
    [
      f"interface {ini.iosv_0.g0_2.name}",
      f"no ip address",
      f"no shutdown",
    ],
    [
      f"interface {ini.iosv_1.g0_2.name}.{ini.iosv_0.g0_2.sub0.num}",
      f"encapsulation dot1Q {ini.iosv_1.g0_2.sub0.num}",
      f"ip addr {ini.iosv_1.g0_2.sub0.ip_addr.ip} {ini.iosv_1.g0_2.sub0.ip_addr.netmask}",
      f"no shutdown",
    ],
    [
      f"interface {ini.iosv_1.g0_2.name}.{ini.iosv_1.g0_2.sub1.num}",
      f"encapsulation dot1Q {ini.iosv_1.g0_2.sub1.num}",
      f"ip addr {ini.iosv_1.g0_2.sub1.ip_addr.ip} {ini.iosv_1.g0_2.sub1.ip_addr.netmask}",
      f"no shutdown",
    ],
  ])

  # routing
  iosv_0.execs([
    [
      f"ip route vrf {ini.site_a.name} 0.0.0.0 0.0.0.0 {ini.iosv_1.g0_2.sub0.ip_addr.ip}",
      f"ip route vrf {ini.site_b.name} 0.0.0.0 0.0.0.0 {ini.iosv_1.g0_2.sub1.ip_addr.ip}",
    ],
  ])
  iosv_1.execs([
    [
      f"ip route vrf {ini.site_a.name} 0.0.0.0 0.0.0.0 {ini.iosv_0.g0_2.sub0.ip_addr.ip}",
      f"ip route vrf {ini.site_b.name} 0.0.0.0 0.0.0.0 {ini.iosv_0.g0_2.sub1.ip_addr.ip}",
    ],
  ])

  wait.seconds(30)
  server_0.server_ping(ini.server_2.eth0.ip_addr.ip)
  server_1.server_ping(ini.server_3.eth0.ip_addr.ip)

  iosv_0.execs([
    f"show ip vrf brief",
    f"show ip route",
    f"show ip route vrf {ini.site_a.name}",
    f"show ip route vrf {ini.site_b.name}",
  ])
  iosv_1.execs([
    f"show ip vrf brief",
    f"show ip route",
    f"show ip route vrf {ini.site_a.name}",
    f"show ip route vrf {ini.site_b.name}",
  ])
  
  # pcap.start(maxpackets=500)
  # server_0.server_ping(ini.server_1.eth0.ip_addr.ip)
  # pcap.download(file=ini.pcap_file)

if __name__ == '__main__':
  main()
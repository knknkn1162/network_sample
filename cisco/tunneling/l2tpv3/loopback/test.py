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
  iosv_2 = Device(tb, ini.iosv_2.__name__)

  server_0 = Device(tb, ini.server_0.__name__)
  server_1 = Device(tb, ini.server_1.__name__)
  print("####### exec #######")
  cml = Cml()
  #pcap = cml.lab.create_pcap(iosvl2_0.name, iosvl2_2.name, auth_token=cml.auth_token)

  # server setup
  server_0.execs([
    # eth0 setting
    ## disable DHCP
    f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
    f"sudo ifconfig eth0 {ini.server_0.eth0.ip_addr.ip} netmask {ini.server_0.eth0.ip_addr.netmask} up",
    #f"sudo route add default gw {ini.iosv_0.loopback0.ip_addr.ip}",
    f"ifconfig eth0",
    #f"route -e",
  ])

  # server setup
  server_1.execs([
    # eth0 setting
    ## disable DHCP
    f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
    f"sudo ifconfig eth0 {ini.server_1.eth0.ip_addr.ip} netmask {ini.server_1.eth0.ip_addr.netmask} up",
    #f"sudo route add default gw {ini.iosv_2.loopback0.ip_addr.ip}",
    f"ifconfig eth0",
    #f"route -e",
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
      f"no ip address",
      #f"ip addr {ini.iosv_0.g0_1.ip_addr.ip} {ini.iosv_0.g0_1.ip_addr.netmask}",
      f"no shutdown",
    ],
    # for OSPF
    [
      f"interface {ini.iosv_0.loopback0.name}",
      f"ip addr {ini.iosv_0.loopback0.ip_addr.ip} {ini.iosv_0.loopback0.ip_addr.netmask}",
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
    # for OSPF
    [
      f"interface {ini.iosv_1.loopback0.name}",
      f"ip addr {ini.iosv_1.loopback0.ip_addr.ip} {ini.iosv_1.loopback0.ip_addr.netmask}",
      f"no shutdown",
    ],
  ])

  iosv_2.execs([
    [
      f"interface {ini.iosv_2.g0_0.name}",
      f"ip addr {ini.iosv_2.g0_0.ip_addr.ip} {ini.iosv_2.g0_0.ip_addr.netmask}",
      f"no shutdown",
    ],
    [
      f"interface {ini.iosv_2.g0_1.name}",
      f"no ip address",
      #f"ip addr {ini.iosv_2.g0_1.ip_addr.ip} {ini.iosv_2.g0_1.ip_addr.netmask}",
      f"no shutdown",
    ],
    # for OSPF
    [
      f"interface {ini.iosv_2.loopback0.name}",
      f"ip addr {ini.iosv_2.loopback0.ip_addr.ip} {ini.iosv_2.loopback0.ip_addr.netmask}",
      f"no shutdown",
    ],
  ])

  # ospf routing
  iosv_0.execs([
    [
      f"router ospf {ini.ospf_process_id}",
      f"network {ini.iosv_0.g0_0.ip_addr.ip} {ini.iosv_0.g0_0.ip_addr.hostmask} area 0",
      f"network {ini.iosv_0.loopback0.ip_addr.ip} {ini.iosv_0.loopback0.ip_addr.hostmask} area 0",
    ],
  ])

  iosv_1.execs([
    [
      f"router ospf {ini.ospf_process_id}",
      f"network {ini.iosv_1.g0_0.ip_addr.ip} {ini.iosv_1.g0_0.ip_addr.hostmask} area 0",
      f"network {ini.iosv_1.g0_1.ip_addr.ip} {ini.iosv_1.g0_1.ip_addr.hostmask} area 0",
    ],
  ])

  iosv_2.execs([
    [
      f"router ospf {ini.ospf_process_id}",
      f"network {ini.iosv_2.g0_0.ip_addr.ip} {ini.iosv_2.g0_0.ip_addr.hostmask} area 0",
      f"network {ini.iosv_2.loopback0.ip_addr.ip} {ini.iosv_2.loopback0.ip_addr.hostmask} area 0",
    ],
  ])

  def populate_router_ping(device: Device, target_ip: str):
    @wait.retry(count=30, result=0, sleep_time=5)
    def _do(device: Device):
      return parse.router_ping(device, target_ip)
    return _do(device)

  populate_router_ping(iosv_0, ini.iosv_2.loopback0.ip_addr.ip)

  # L2TP
  iosv_0.execs([
    [
      f"pseudowire-class L2TPv3",
      f"encapsulation l2tpv3",
      f"ip local interface {ini.iosv_2.g0_0.name}"
    ],
    [
      f"interface {ini.iosv_0.g0_1.name}",
      # set destination
      f"xconnect {ini.iosv_2.g0_0.ip_addr.ip} {ini.vc_id} encapsulation l2tpv3 pw-class L2TPv3",
    ],
  ])

  iosv_2.execs([
    [
      f"pseudowire-class L2TPv3",
      f"encapsulation l2tpv3",
      f"ip local interface {ini.iosv_2.g0_0.name}"
    ],
    [
      f"interface {ini.iosv_2.g0_1.name}",
      # set destination
      f"xconnect {ini.iosv_0.g0_0.ip_addr.ip} {ini.vc_id} encapsulation l2tpv3 pw-class L2TPv3",
    ],
  ])

  wait_until.seconds(30)

  def populate_server_ping(device: Device, target_ip: str):
    @wait.retry(count=30, result=0, sleep_time=5)
    def _do(device: Device):
      return device.server_ping(target_ip)
    return _do(device)

  populate_server_ping(server_0, ini.server_1.eth0.ip_addr.ip)
  
  iosv_0.execs([
    f"show xconnect all",
    f"show l2tp session",
  ])

  iosv_2.execs([
    f"show xconnect all",
    f"show l2tp session",
  ])

if __name__ == '__main__':
  main()
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
  pcap = cml.lab.create_pcap("sw_0", iosv_0.name, auth_token=cml.auth_token)

  # server setup
  server_0.execs([
    # eth0 setting
    ## disable DHCP
    f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
    f"sudo ifconfig eth0 {ini.server_0.eth0.ip_addr} netmask {ini.server_0.eth0.subnet_mask} up",
    f"sudo route add default gw {ini.server_0.eth0.default_gw_addr}",
    f"ifconfig eth0",
    f"route -e",
  ])

  server_1.execs([
      # eth0 setting
      ## disable DHCP
      f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
      f"sudo ifconfig eth0 {ini.server_1.eth0.ip_addr} netmask {ini.server_1.eth0.subnet_mask} up",
      f"sudo route add default gw {ini.server_1.eth0.default_gw_addr}",
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
      f"no shutdown",
    ],
    [
      f"interface {ini.iosv_2.loopback0.name}",
      f"ip addr {ini.iosv_2.loopback0.ip_addr} {ini.iosv_2.loopback0.subnet_mask}",
      #f"no shutdown",
    ],
  ])


  iosv_0.show_mac_ip()
  iosv_1.show_mac_ip()
  iosv_2.show_mac_ip()

  # routing(RIP)
  g0_0_network0 = ipv4.get_network0(ini.iosv_0.g0_0.ip_addr, ini.iosv_0.g0_0.subnet_mask)
  g0_1_network0 = ipv4.get_network0(ini.iosv_0.g0_1.ip_addr, ini.iosv_0.g0_1.subnet_mask)
  iosv_0.execs([
    [
      f"router rip",
      f"version 2",
      f"network {g0_0_network0}",
      f"network {g0_1_network0}",
      f"no auto-summary",
    ],
  ])
  g0_0_network0 = ipv4.get_network0(ini.iosv_1.g0_0.ip_addr, ini.iosv_1.g0_0.subnet_mask)
  g0_1_network0 = ipv4.get_network0(ini.iosv_1.g0_1.ip_addr, ini.iosv_1.g0_1.subnet_mask)
  iosv_1.execs([
    [
      f"router rip",
      f"version 2",
      f"network {g0_0_network0}",
      f"network {g0_1_network0}",
      f"no auto-summary",
    ],
  ])

  g0_0_network0 = ipv4.get_network0(ini.iosv_2.g0_0.ip_addr, ini.iosv_2.g0_0.subnet_mask)
  g0_1_network0 = ipv4.get_network0(ini.iosv_2.g0_1.ip_addr, ini.iosv_2.g0_1.subnet_mask)
  loopback0_network0 = ipv4.get_network0(ini.iosv_2.loopback0.ip_addr, ini.iosv_2.loopback0.subnet_mask)
  iosv_2.execs([
    [
      f"router rip",
      f"version 2",
      f"network {g0_0_network0}",
      f"network {g0_1_network0}",
      f"network {loopback0_network0}",
      f"no auto-summary",
    ],
  ])

  # HSRP setting
  iosv_0.execs([
    [
      f"interface {ini.iosv_0.g0_0.name}",
      f"standby {ini.hsrp0.group_id} ip {ini.hsrp0.virtual_ip_addr}",
      f"standby {ini.hsrp0.group_id} priority {ini.iosv_0.g0_0.hsrp0_priority}",
      f"standby {ini.hsrp0.group_id} preempt",
      f"standby {ini.hsrp1.group_id} ip {ini.hsrp1.virtual_ip_addr}",
      f"standby {ini.hsrp1.group_id} priority {ini.iosv_0.g0_0.hsrp1_priority}",
      f"standby {ini.hsrp1.group_id} preempt",
    ],
  ])

  iosv_1.execs([
    [
      f"interface {ini.iosv_1.g0_0.name}",
      f"standby {ini.hsrp0.group_id} ip {ini.hsrp0.virtual_ip_addr}",
      f"standby {ini.hsrp0.group_id} priority {ini.iosv_1.g0_0.hsrp0_priority}",
      f"standby {ini.hsrp0.group_id} preempt",
      f"standby {ini.hsrp1.group_id} ip {ini.hsrp1.virtual_ip_addr}",
      f"standby {ini.hsrp1.group_id} priority {ini.iosv_1.g0_0.hsrp1_priority}",
      f"standby {ini.hsrp1.group_id} preempt",
    ],
  ])

  def populate_server_ping(device: Device, target_ip: str, count=5):
    @wait.retry(count=30, result=0, sleep_time=3)
    def _do(device: Device):
      return device.server_ping(target_ip, count)
    return _do(device)
  populate_server_ping(server_0, ini.iosv_2.loopback0.ip_addr)
  populate_server_ping(server_1, ini.iosv_2.loopback0.ip_addr)


  pcap.start(maxpackets=500)
  server_0.server_ping(ini.iosv_2.loopback0.ip_addr)
  server_1.server_ping(ini.iosv_2.loopback0.ip_addr)
  # 5 packets
  pcap.download(file=ini.pcap_file)


if __name__ == '__main__':
  main()
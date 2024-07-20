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
  iosvl2_0 = Device(tb, ini.iosvl2_0.__name__)
  iosvl2_1 = Device(tb, ini.iosvl2_1.__name__)
  iosvl2_2 = Device(tb, ini.iosvl2_2.__name__)


  iosv_0 = Device(tb, ini.iosv_0.__name__)

  server_0 = Device(tb, ini.server_0.__name__)
  server_1 = Device(tb, ini.server_1.__name__)
  print("####### exec #######")
  cml = Cml()
  pcap = cml.lab.create_pcap(iosvl2_0.name, iosvl2_2.name, auth_token=cml.auth_token)

  # server setup
  server_0.execs([
    # eth0 setting
    ## disable DHCP
    f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
    f"sudo ifconfig eth0 {ini.server_0.eth0.ip_addr} netmask {ini.server_0.eth0.subnet_mask} up",
    # set default gw to virtual address of hsrp
    f"sudo route add default gw {ini.hsrp0.virtual_ip_addr}",
    f"ifconfig eth0",
    f"route -e",
  ])

  server_1.execs([
      # eth0 setting
      ## disable DHCP
      f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
      f"sudo ifconfig eth0 {ini.server_1.eth0.ip_addr} netmask {ini.server_1.eth0.subnet_mask} up",
      # set default gw to virtual address of hsrp
      f"sudo route add default gw {ini.hsrp0.virtual_ip_addr}",
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
    [
      f"interface {ini.iosv_0.loopback0.name}",
      f"ip addr {ini.iosv_0.loopback0.ip_addr} {ini.iosv_0.loopback0.subnet_mask}",
      #f"no shutdown",
    ],
  ])

  iosvl2_0.execs([
    [
      f"interface {ini.iosvl2_0.g0_0.name}",
      f"switchport mode access",
      f"switchport access {ini.iosvl2_0.vlan0.name}",
      f"no shutdown",
    ],
    [
      "ip routing",
    ],
    # routed port
    [
      f"interface {ini.iosvl2_0.g0_1.name}",
      f"no switchport",
      f"ip address {ini.iosvl2_0.g0_1.ip_addr} {ini.iosvl2_0.g0_1.subnet_mask}",
    ],
    # svi
    [
      f"interface {ini.iosvl2_0.vlan0.name}",
      f"ip address {ini.iosvl2_0.vlan0.ip_addr} {ini.iosvl2_0.vlan0.subnet_mask}",
      f"no shutdown",
    ],
  ])

  iosvl2_1.execs([
    [
      f"interface {ini.iosvl2_1.g0_0.name}",
      f"switchport mode access",
      f"switchport access {ini.iosvl2_1.vlan0.name}",
      f"no shutdown",
    ],
    [
      "ip routing",
    ],
    # routed port
    [
      f"interface {ini.iosvl2_1.g0_1.name}",
      f"no switchport",
      f"ip address {ini.iosvl2_1.g0_1.ip_addr} {ini.iosvl2_1.g0_1.subnet_mask}",
    ],
    # svi
    [
      f"interface {ini.iosvl2_1.vlan0.name}",
      f"ip address {ini.iosvl2_1.vlan0.ip_addr} {ini.iosvl2_1.vlan0.subnet_mask}",
      f"no shutdown",
    ],
  ])

  iosvl2_2.execs([
    [
      f"interface {ini.iosvl2_2.g0_0.name}",
      f"switchport mode access",
      f"switchport access {ini.iosvl2_2.vlan0.name}",
    ],
      [
      f"interface {ini.iosvl2_2.g0_1.name}",
      f"switchport mode access",
      f"switchport access {ini.iosvl2_2.vlan0.name}",
    ],
    [
      f"interface {ini.iosvl2_2.g0_2.name}",
      f"switchport mode access",
      f"switchport access {ini.iosvl2_2.vlan0.name}",
    ],
    [
      f"interface {ini.iosvl2_2.g0_3.name}",
      f"switchport mode access",
      f"switchport access {ini.iosvl2_2.vlan0.name}",
    ],
  ])

  # routing
  g0_0_network0 = ipv4.get_network0(ini.iosv_0.g0_0.ip_addr, ini.iosv_0.g0_0.subnet_mask)
  g0_1_network0 = ipv4.get_network0(ini.iosv_0.g0_1.ip_addr, ini.iosv_0.g0_1.subnet_mask)
  loopback0_network0 = ipv4.get_network0(ini.iosv_0.loopback0.ip_addr, ini.iosv_0.loopback0.subnet_mask)

  iosv_0.execs([
    [
      f"router rip",
      f"version 2",
      f"network {g0_0_network0}",
      f"network {g0_1_network0}",
      f"network {loopback0_network0}",
      f"no auto-summary",
    ],
  ])
  g0_0_network0 = ipv4.get_network0(ini.iosvl2_0.vlan0.ip_addr, ini.iosvl2_0.vlan0.subnet_mask)
  g0_1_network0 = ipv4.get_network0(ini.iosvl2_0.g0_1.ip_addr, ini.iosvl2_0.g0_1.subnet_mask)
  iosvl2_0.execs([
    [
      f"router rip",
      f"version 2",
      f"network {g0_0_network0}",
      f"network {g0_1_network0}",
      f"no auto-summary",
    ],
  ])

  g0_0_network0 = ipv4.get_network0(ini.iosvl2_1.vlan0.ip_addr, ini.iosvl2_0.vlan0.subnet_mask)
  g0_1_network0 = ipv4.get_network0(ini.iosvl2_1.g0_1.ip_addr, ini.iosvl2_1.g0_1.subnet_mask)
  iosvl2_1.execs([
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
  iosvl2_0.execs([
    [
      f"interface {ini.iosvl2_0.vlan0.name}",
      # "address is not within a subnet on this interface" warning if not svi
      f"standby {ini.hsrp0.group_id} ip {ini.hsrp0.virtual_ip_addr}",
      f"standby {ini.hsrp0.group_id} priority {ini.iosvl2_0.vlan0.hsrp0_priority}",
      f"standby {ini.hsrp0.group_id} preempt",
    ],
  ])

  iosvl2_1.execs([
    [
      f"interface {ini.iosvl2_1.vlan0.name}",
      f"standby {ini.hsrp0.group_id} ip {ini.hsrp0.virtual_ip_addr}",
      f"standby {ini.hsrp0.group_id} priority {ini.iosvl2_1.vlan0.hsrp0_priority}",
      f"standby {ini.hsrp0.group_id} preempt",
    ],
  ])

  def populate_server_ping(device: Device, target_ip: str, count=5):
    @wait.retry(count=30, result=0, sleep_time=3)
    def _do(device: Device):
      return device.server_ping(target_ip, count)
    return _do(device)
  populate_server_ping(server_0, ini.iosv_0.loopback0.ip_addr)
  populate_server_ping(server_1, ini.iosv_0.loopback0.ip_addr)


  pcap.start(maxpackets=500)
  server_0.server_ping(ini.iosv_0.loopback0.ip_addr)
  server_1.server_ping(ini.iosv_0.loopback0.ip_addr)
  # 5 packets
  pcap.download(file=ini.pcap_file)

  iosvl2_0.execs([
    f"show standby",
  ])
  iosvl2_1.execs([
    f"show standby",
  ])

if __name__ == '__main__':
  main()
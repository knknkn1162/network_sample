from genie import testbed
from cmlmag.cml import CONFIG_YAML, Cml
from cmlmag.device import Device
from cmlmag import wait, ipv4
import cmlmag.parse as parse
import cmlmag.wait_until as wait_until
import ini
from cmlmag.structure.stp_info import (
  Role as StpRole
)

def main():
  tb = testbed.load(CONFIG_YAML)
  # switch
  iosvl2_0 = Device(tb, 'iosvl2_0')
  iosvl2_1 = Device(tb, 'iosvl2_1')
  iosvl2_2 = Device(tb, 'iosvl2_2')

  server_0 = Device(tb, 'server_0')
  server_1 = Device(tb, 'server_1')

  print("####### exec #######")
  cml = Cml()
  pcap01 = cml.lab.create_pcap(ini.iosvl2_0.__name__, ini.iosvl2_1.__name__)
  pcap12 = cml.lab.create_pcap(ini.iosvl2_1.__name__, ini.iosvl2_2.__name__)
  pcap20 = cml.lab.create_pcap(ini.iosvl2_2.__name__, ini.iosvl2_0.__name__)


  # switch
  # server setting
  server_0.execs([
    ## disable DHCP
    f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
    f"sudo ifconfig eth0 {ini.server_0.eth0.ip_addr} netmask {ini.server_0.eth0.subnet_mask} up",
    f"ifconfig eth0",
  ])

  server_1.execs([
    ## disable DHCP
    f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
    f"sudo ifconfig eth0 {ini.server_1.eth0.ip_addr} netmask {ini.server_1.eth0.subnet_mask} up",
    f"ifconfig eth0",
  ])

  iosvl2_0.show_mac_ip()
  iosvl2_1.show_mac_ip()
  iosvl2_2.show_mac_ip()

  ## switchport settings
  iosvl2_0.execs([
    [
      f"interface {ini.iosvl2_0.g0_0.name}",
      f"switchport mode access",
      f"switchport access vlan {ini.vlan_num}",
    ],
    [
      f"interface {ini.iosvl2_0.g0_1.name}",
      f"switchport mode access",
      f"switchport access vlan {ini.vlan_num}",
    ],
    [
      f"interface {ini.iosvl2_0.g0_2.name}",
      f"switchport mode access",
      f"switchport access vlan {ini.vlan_num}",
    ],
  ])

  iosvl2_1.execs([
    [
      f"interface {ini.iosvl2_1.g0_0.name}",
      f"switchport mode access",
      f"switchport access vlan {ini.vlan_num}",
    ],
    [
      f"interface {ini.iosvl2_1.g0_1.name}",
      f"switchport mode access",
      f"switchport access vlan {ini.vlan_num}",
    ],
  ])

  iosvl2_2.execs([
    [
      f"interface {ini.iosvl2_2.g0_0.name}",
      f"switchport mode access",
      f"switchport access vlan {ini.vlan_num}",
    ],
    [
      f"interface {ini.iosvl2_2.g0_1.name}",
      f"switchport mode access",
      f"switchport access vlan {ini.vlan_num}",
    ],
    [
      f"interface {ini.iosvl2_2.g0_2.name}",
      f"switchport mode access",
      f"switchport access vlan {ini.vlan_num}",
    ],
  ])

  # spanning tree settings
  pcap01.start(maxpackets=200)
  pcap12.start(maxpackets=200)
  pcap20.start(maxpackets=200)

  iosvl2_0.execs([
    [
      f"spanning-tree vlan {ini.vlan_num} priority {ini.iosvl2_0.stp_priority}",
    ]
  ])
  iosvl2_1.execs([
    [
      f"spanning-tree vlan {ini.vlan_num} priority {ini.iosvl2_1.stp_priority}",
    ]
  ])
  iosvl2_2.execs([
    [
      f"spanning-tree vlan {ini.vlan_num} priority {ini.iosvl2_2.stp_priority}",
    ]
  ])

  wait_until.seconds(2)
  wait_until.populate_stp(iosvl2_0, ini.vlan_num, 3)
  wait_until.populate_stp(iosvl2_1, ini.vlan_num, 2)
  wait_until.populate_stp(iosvl2_2, ini.vlan_num, 3)

  pcap01.download(file=ini.pcap01_file)
  pcap12.download(file=ini.pcap12_file)
  pcap20.download(file=ini.pcap20_file)

  result = parse.get_stp_info(iosvl2_0, ini.vlan_num, ini.iosvl2_0.g0_0.name)
  assert result.role == StpRole.designated
  result = parse.get_stp_info(iosvl2_0, ini.vlan_num, ini.iosvl2_0.g0_1.name)
  assert result.role == StpRole.designated
  result = parse.get_stp_info(iosvl2_0, ini.vlan_num, ini.iosvl2_0.g0_2.name)
  assert result.role == StpRole.designated

  result = parse.get_stp_info(iosvl2_1, ini.vlan_num, ini.iosvl2_1.g0_0.name)
  assert result.role == StpRole.root
  result = parse.get_stp_info(iosvl2_1, ini.vlan_num, ini.iosvl2_1.g0_1.name)
  assert result.role == StpRole.designated

  result = parse.get_stp_info(iosvl2_2, ini.vlan_num, ini.iosvl2_2.g0_0.name)
  assert result.role == StpRole.root
  result = parse.get_stp_info(iosvl2_2, ini.vlan_num, ini.iosvl2_2.g0_1.name)
  assert result.role == StpRole.alternate
  result = parse.get_stp_info(iosvl2_2, ini.vlan_num, ini.iosvl2_2.g0_2.name)
  assert result.role == StpRole.designated

  iosvl2_0.execs([
    f"show spanning-tree vlan {ini.vlan_num}",
  ])

  iosvl2_1.execs([
    f"show spanning-tree vlan {ini.vlan_num}",
  ])

  iosvl2_2.execs([
    f"show spanning-tree vlan {ini.vlan_num}",
  ])

if __name__ == '__main__':
  main()
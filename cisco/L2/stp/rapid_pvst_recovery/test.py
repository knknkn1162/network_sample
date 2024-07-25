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
  iosvl2_3 = Device(tb, ini.iosvl2_3.__name__)

  server_0 = Device(tb, ini.server_0.__name__)
  server_1 = Device(tb, ini.server_1.__name__)
  print("####### exec #######")
  cml = Cml()
  pcap01 = cml.lab.create_pcap(iosvl2_0.name, iosvl2_1.name, auth_token=cml.auth_token)
  pcap02 = cml.lab.create_pcap(iosvl2_0.name, iosvl2_2.name, auth_token=cml.auth_token)
  pcap13 = cml.lab.create_pcap(iosvl2_1.name, iosvl2_3.name, auth_token=cml.auth_token)
  pcap23 = cml.lab.create_pcap(iosvl2_2.name, iosvl2_3.name, auth_token=cml.auth_token)


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
  iosvl2_3.show_mac_ip()

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
  ])

  iosvl2_3.execs([
    [
      f"interface {ini.iosvl2_3.g0_0.name}",
      f"switchport mode access",
      f"switchport access vlan {ini.vlan_num}",
    ],
    [
      f"interface {ini.iosvl2_3.g0_1.name}",
      f"switchport mode access",
      f"switchport access vlan {ini.vlan_num}",
    ],
    [
      f"interface {ini.iosvl2_3.g0_2.name}",
      f"switchport mode access",
      f"switchport access vlan {ini.vlan_num}",
    ],
  ])

  # Rapid PVST+
  iosvl2_0.execs([
    [
      f"spanning-tree mode rapid-pvst",
    ],
  ])
  iosvl2_1.execs([
   [
      f"spanning-tree mode rapid-pvst",
   ],
  ])
  iosvl2_2.execs([
   [
      f"spanning-tree mode rapid-pvst",
   ],
  ])
  iosvl2_3.execs([
   [
      f"spanning-tree mode rapid-pvst",
   ],
  ])

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
  iosvl2_3.execs([
    [
      f"spanning-tree vlan {ini.vlan_num} priority {ini.iosvl2_3.stp_priority}",
    ]
  ])

  wait_until.populate_stp(iosvl2_0, ini.vlan_num, 3)
  wait_until.populate_stp(iosvl2_1, ini.vlan_num, 2)
  wait_until.populate_stp(iosvl2_2, ini.vlan_num, 2)
  wait_until.populate_stp(iosvl2_3, ini.vlan_num, 3)

  wait_until.populate_server_ping(server_0, ini.server_1.eth0.ip_addr)
  result0 = parse.get_stp_info(iosvl2_0, ini.vlan_num, ini.iosvl2_0.g0_0.name)
  result1 = parse.get_stp_info(iosvl2_0, ini.vlan_num, ini.iosvl2_0.g0_1.name)
  result2 = parse.get_stp_info(iosvl2_0, ini.vlan_num, ini.iosvl2_0.g0_2.name)
  assert (result0.role, result1.role, result2.role) == (StpRole.designated, StpRole.designated, StpRole.designated)

  result0 = parse.get_stp_info(iosvl2_1, ini.vlan_num, ini.iosvl2_1.g0_0.name)
  result1 = parse.get_stp_info(iosvl2_1, ini.vlan_num, ini.iosvl2_1.g0_1.name)
  assert (result0.role, result1.role) == (StpRole.root, StpRole.designated)

  result0 = parse.get_stp_info(iosvl2_2, ini.vlan_num, ini.iosvl2_2.g0_0.name)
  result1 = parse.get_stp_info(iosvl2_2, ini.vlan_num, ini.iosvl2_2.g0_1.name)
  assert (result0.role, result1.role) == (StpRole.designated, StpRole.root)

  result0 = parse.get_stp_info(iosvl2_3, ini.vlan_num, ini.iosvl2_3.g0_0.name)
  result1 = parse.get_stp_info(iosvl2_3, ini.vlan_num, ini.iosvl2_3.g0_1.name)
  result2 = parse.get_stp_info(iosvl2_3, ini.vlan_num, ini.iosvl2_3.g0_2.name)
  assert (result0.role, result1.role, result2.role) == (StpRole.alternate, StpRole.root, StpRole.designated)

  iosvl2_0.execs([
    f"show spanning-tree vlan {ini.vlan_num}",
  ])

  iosvl2_1.execs([
    f"show spanning-tree vlan {ini.vlan_num}",
  ])

  iosvl2_2.execs([
    f"show spanning-tree vlan {ini.vlan_num}",
  ])
  iosvl2_3.execs([
    f"show spanning-tree vlan {ini.vlan_num}",
  ])

  # enable debugger
  for dev in [iosvl2_0, iosvl2_1, iosvl2_2, iosvl2_3]:
    dev.execs([
      f"debug spanning-tree all",
    ])

  # spanning tree settings
  pcap01.start(maxpackets=200)
  pcap02.start(maxpackets=200)
  pcap13.start(maxpackets=200)
  pcap23.start(maxpackets=200)

  # enable debugger
  cml.lab.stop_link_by_nodes(iosvl2_1.name, iosvl2_3.name)
  # wait until
  flag = True
  while flag:
    #wait_until.seconds(1)
    result = parse.get_stp_info(iosvl2_3, ini.vlan_num, ini.iosvl2_3.g0_0.name)
    if result.role == StpRole.root and result.port_state == StpState.forwarding:
      flag = False

  wait_until.populate_server_ping(server_0, ini.server_1.eth0.ip_addr)

  # disable debugger
  for dev in [iosvl2_0, iosvl2_1, iosvl2_2, iosvl2_3]:
    dev.execs([
      f"no debug spanning-tree all",
    ])

  pcap01.download(file=ini.pcap01_file)
  pcap02.download(file=ini.pcap02_file)
  pcap13.download(file=ini.pcap13_file)
  pcap23.download(file=ini.pcap23_file)
  iosvl2_0.execs([
    f"show spanning-tree vlan {ini.vlan_num}",
  ])

  iosvl2_1.execs([
    f"show spanning-tree vlan {ini.vlan_num}",
  ])

  iosvl2_2.execs([
    f"show spanning-tree vlan {ini.vlan_num}",
  ])
  iosvl2_3.execs([
    f"show spanning-tree vlan {ini.vlan_num}",
  ])

if __name__ == '__main__':
  main()
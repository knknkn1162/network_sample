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
  iosvl2_0 = Device(tb, ini.iosvl2_0.__name__)

  server_0 = Device(tb, ini.server_0.__name__)
  server_1 = Device(tb, ini.server_1.__name__)
  server_2 = Device(tb, ini.server_2.__name__)
  server_3 = Device(tb, ini.server_3.__name__)
  server_4 = Device(tb, ini.server_4.__name__)
  server_5 = Device(tb, ini.server_5.__name__)


  print("####### exec #######")
  cml = Cml()
  pcap = cml.lab.create_pcap(iosvl2_0.name, server_0.name, auth_token=cml.auth_token)

  server_0.execs([
    # eth0 setting
    ## disable DHCP
    f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
    f"sudo ifconfig eth0 {ini.server_0.eth0.ip_addr.ip} netmask {ini.server_0.eth0.ip_addr.netmask} up",
    f"ifconfig eth0",
  ])
  server_1.execs([
    # eth0 setting
    ## disable DHCP
    f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
    f"sudo ifconfig eth0 {ini.server_1.eth0.ip_addr.ip} netmask {ini.server_1.eth0.ip_addr.netmask} up",
    f"ifconfig eth0",
  ])
  server_2.execs([
    # eth0 setting
    ## disable DHCP
    f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
    f"sudo ifconfig eth0 {ini.server_2.eth0.ip_addr.ip} netmask {ini.server_2.eth0.ip_addr.netmask} up",
    f"ifconfig eth0",
  ])
  server_3.execs([
    # eth0 setting
    ## disable DHCP
    f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
    f"sudo ifconfig eth0 {ini.server_3.eth0.ip_addr.ip} netmask {ini.server_3.eth0.ip_addr.netmask} up",
    f"ifconfig eth0",
  ])
  server_4.execs([
    # eth0 setting
    ## disable DHCP
    f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
    f"sudo ifconfig eth0 {ini.server_4.eth0.ip_addr.ip} netmask {ini.server_4.eth0.ip_addr.netmask} up",
    f"ifconfig eth0",
  ])
  server_5.execs([
    # eth0 setting
    ## disable DHCP
    f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
    f"sudo ifconfig eth0 {ini.server_5.eth0.ip_addr.ip} netmask {ini.server_5.eth0.ip_addr.netmask} up",
    f"ifconfig eth0",
  ])

  iosvl2_0.execs([
    [
      # Private VLANs can only be configured 
      # when VTP is in transparent/off modes in VTP version 1 or 2 and 
      # in server/transparent/off modes in VTP version 3 when pruning is turned off
      f"vtp mode transparent",
    ],
    [
      f"vlan {ini.vlan.isolated.num}",
      f"private-vlan isolated",
    ],
    [
      f"vlan {ini.vlan.community0.num}",
      f"private-vlan community",
    ],
    [
      f"vlan {ini.vlan.community1.num}",
      f"private-vlan community",
    ],
    [
      f"vlan {ini.vlan.primary.num}",
      f"private-vlan primary",
      # TOOD: f"private-vlan association add {ini.vlan.isolated.num}" cannot be used.
      f"private-vlan association {ini.vlan.isolated.num},{ini.vlan.community0.num},{ini.vlan.community1.num}",
    ],
  ])

  iosvl2_0.execs([
    [
      f"interface {ini.iosvl2_0.g0_4.name}",
      f"switchport mode private-vlan promiscuous",
      f"switchport private-vlan mapping {ini.vlan.primary.num} add {ini.vlan.isolated.num}",
      f"switchport private-vlan mapping {ini.vlan.primary.num} add {ini.vlan.community0.num}",
      f"switchport private-vlan mapping {ini.vlan.primary.num} add {ini.vlan.community1.num}",

    ],
    [
      f"interface {ini.iosvl2_0.g0_0.name}",
      f"switchport mode private-vlan host",
      f"switchport private-vlan host-association {ini.vlan.primary.num} {ini.vlan.isolated.num}",
    ],
    [
      f"interface {ini.iosvl2_0.g0_1.name}",
      f"switchport mode private-vlan host",
      f"switchport private-vlan host-association {ini.vlan.primary.num} {ini.vlan.isolated.num}",
    ],
    [
      f"interface {ini.iosvl2_0.g0_2.name}",
      f"switchport mode private-vlan host",
      f"switchport private-vlan host-association {ini.vlan.primary.num} {ini.vlan.community0.num}",
    ],
    [
      f"interface {ini.iosvl2_0.g0_3.name}",
      f"switchport mode private-vlan host",
      f"switchport private-vlan host-association {ini.vlan.primary.num} {ini.vlan.community0.num}",
    ],
    [
      f"interface {ini.iosvl2_0.g0_5.name}",
      f"switchport mode private-vlan host",
      f"switchport private-vlan host-association {ini.vlan.primary.num} {ini.vlan.community1.num}",
    ],
    [
      f"interface vlan {ini.vlan.primary.num}",
      f"private-vlan mapping add {ini.vlan.isolated.num}",
      f"private-vlan mapping add {ini.vlan.community0.num}",
      f"private-vlan mapping add {ini.vlan.community1.num}",
      f"no shutdown",
    ]
  ])

  wait.seconds(20)
  iosvl2_0.execs([
    f"show ip interface brief",
    f"show interfaces status",
    f"show vlan",
    f"show vlan private-vlan",
    f"show interface private-vlan mapping",
  ])

  def populate_server_ping(device: Device, target_ip: str, result: int, count=5):
    @wait.bretry(count=30, sleep_time=3)
    def _do(device: Device):
      return device.server_ping(target_ip, count) == result
    return _do(device)
  
  # isolated <-> promiscuous
  populate_server_ping(server_0, ini.server_1.eth0.ip_addr.ip, result=1)
  populate_server_ping(server_0, ini.server_2.eth0.ip_addr.ip, result=1)
  populate_server_ping(server_0, ini.server_4.eth0.ip_addr.ip, result=0)

  # community0 <-> community0, promiscuous
  populate_server_ping(server_2, ini.server_3.eth0.ip_addr.ip, result=0)
  populate_server_ping(server_2, ini.server_4.eth0.ip_addr.ip, result=0)
  populate_server_ping(server_2, ini.server_5.eth0.ip_addr.ip, result=1)

  # community1 <-> promiscuous
  populate_server_ping(server_5, ini.server_4.eth0.ip_addr.ip, result=0)

  pcap.start(maxpackets=100)
  server_0.server_ping(ini.server_4.eth0.ip_addr.ip)
  pcap.download(file=ini.pcap_file0)

if __name__ == '__main__':
  main()
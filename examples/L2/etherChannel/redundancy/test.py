from genie import testbed
from cmlmag.cml import CONFIG_YAML, Cml
from cmlmag.device import Device
from cmlmag import wait, ipv4
import cmlmag.parse as parse
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

  server_0 = Device(tb, ini.server_0.__name__)
  server_1 = Device(tb, ini.server_1.__name__)
  server_2 = Device(tb, ini.server_2.__name__)

  print("####### exec #######")
  cml = Cml()
  pcap01 = cml.lab.create_pcap(iosvl2_0.name, iosvl2_1.name, auth_token=cml.auth_token)

  # server ip
  server_0.execs([
    # eth0 setting
    ## disable DHCP
    f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
    f"sudo ifconfig eth0 {ini.server_0.eth0.ip_addr} netmask {ini.server_0.eth0.subnet_mask} up",
    f"ifconfig eth0",
  ])

  server_1.execs([
    # eth0 setting
    ## disable DHCP
    f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
    f"sudo ifconfig eth0 {ini.server_1.eth0.ip_addr} netmask {ini.server_1.eth0.subnet_mask} up",
    f"ifconfig eth0",
  ])


  server_2.execs([
    # eth0 setting
    ## disable DHCP
    f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
    f"sudo ifconfig eth0 {ini.server_2.eth0.ip_addr} netmask {ini.server_2.eth0.subnet_mask} up",
    f"ifconfig eth0",
  ])

  iosvl2_0.show_mac_ip()
  iosvl2_1.show_mac_ip()

  iosvl2_0.execs([
    [
      f"interface {ini.iosvl2_0.g0_0.name}",
      f"switchport trunk encapsulation dot1q",
      f"switchport mode trunk",
      f"channel-protocol lacp",
      f"channel-group {ini.iosvl2_0.ether_channel.num} mode active",
      f"port-channel load-balance src-mac",
    ],
    [
      f"interface {ini.iosvl2_0.g0_1.name}",
      f"switchport trunk encapsulation dot1q",
      f"switchport mode trunk",
      f"channel-protocol lacp",
      f"channel-group {ini.iosvl2_0.ether_channel.num} mode active",
      f"port-channel load-balance src-mac",
    ],
  ])

  iosvl2_1.execs([
    [
      f"interface {ini.iosvl2_1.g0_0.name}",
      f"switchport trunk encapsulation dot1q",
      f"switchport mode trunk",
      f"channel-protocol lacp",
      # 対向のスイッチは同じgroupにする必要はない
      f"channel-group {ini.iosvl2_1.ether_channel.num} mode passive",
      f"port-channel load-balance dst-mac",
    ],
    [
      f"interface {ini.iosvl2_1.g0_1.name}",
      f"switchport trunk encapsulation dot1q",
      f"switchport mode trunk",
      f"channel-protocol lacp",
      f"channel-group {ini.iosvl2_1.ether_channel.num} mode passive",
      f"port-channel load-balance dst-mac",
    ],
  ])

  def check_stp_state(device: Device, interface: str):
    @wait.retry(count=30, result=StpState.forwarding, sleep_time=2)
    def _do(device: Device):
      device.execs([
        f"show lacp neighbor",
      ])
      try:
        return parse.get_stp_info(device, interface).port_state
      except:
        return None
    return _do(device)
  
  check_stp_state(iosvl2_0, ini.iosvl2_0.ether_channel.name)
  check_stp_state(iosvl2_1, ini.iosvl2_1.ether_channel.name)

  def populate_server_ping(device: Device, target_ip: str, count=5):
    @wait.retry(count=30, result=0, sleep_time=3)
    def _do(device: Device):
      return device.server_ping(target_ip, count)
    return _do(device)
  
  populate_server_ping(server_0, ini.server_2.eth0.ip_addr, count=10)
  populate_server_ping(server_1, ini.server_2.eth0.ip_addr, count=10)

  pcap01.start(maxpackets=200)
  # one of the link removed
  cml.lab.remove_link_by_nodes(iosvl2_0.name, iosvl2_1.name)

  # TODO: should work, but failed...
  populate_server_ping(server_0, ini.server_2.eth0.ip_addr)
  populate_server_ping(server_1, ini.server_2.eth0.ip_addr)

  pcap01.download(file=ini.pcap01_file)

if __name__ == '__main__':
  main()
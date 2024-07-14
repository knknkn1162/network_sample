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

  print("####### exec #######")
  cml = Cml()
  pcap01 = cml.lab.create_pcap(iosvl2_0.name, iosvl2_1.name, auth_token=cml.auth_token)


  iosvl2_0.show_mac_ip()
  iosvl2_1.show_mac_ip()


  ## switchport settings
  pcap01.start(maxpackets=100)
  iosvl2_0.execs([
    [
      f"interface {ini.iosvl2_0.g0_0.name}",
      f"switchport trunk encapsulation dot1q",
      f"switchport mode trunk",
      f"channel-protocol lacp",
      f"channel-group {ini.iosvl2_0.ether_channel.num} mode active",
    ],
    [
      f"interface {ini.iosvl2_0.g0_1.name}",
      f"switchport trunk encapsulation dot1q",
      f"switchport mode trunk",
      f"channel-protocol lacp",
      f"channel-group {ini.iosvl2_0.ether_channel.num} mode active",
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
    ],
    [
      f"interface {ini.iosvl2_1.g0_1.name}",
      f"switchport trunk encapsulation dot1q",
      f"switchport mode trunk",
      f"channel-protocol lacp",
      f"channel-group {ini.iosvl2_1.ether_channel.num} mode passive",
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

  pcap01.download(file=ini.pcap01_file)
  iosvl2_0.execs([
    f"show etherchannel summary",
    f"show etherchannel detail",
    f"show spanning-tree",
    f"show pagp neighbor",
  ])

  iosvl2_1.execs([
    f"show etherchannel summary",
    f"show etherchannel detail",
    f"show spanning-tree",
    f"show pagp neighbor",
  ])



if __name__ == '__main__':
  main()
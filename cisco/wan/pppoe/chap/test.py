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
  iosv_1 = Device(tb, 'iosv_1')
  iosv_2 = Device(tb, 'iosv_2')

  #server_1 = Device(tb, 'server_1')

  # password setting
  iosv_1.execs([
    [
      f"username {ini.iosv_1.username} password {ini.iosv_1.password}",
    ]
  ])

  iosv_1.execs([
    [
      f"interface {ini.iosv_1.loopback0.name}",
      f"ip address {ini.iosv_1.loopback0.ip_addr.ip} {ini.iosv_1.loopback0.ip_addr.netmask}",
    ],
    [
      f"interface {ini.iosv_1.g0_0.name}",
      f"no ip address",
      f"pppoe enable group {ini.iosv_1.bba_group_name}",
      f"no shutdown",
    ],
    # associate phycical I/F <-> virtual-template
    [
      f"bba-group pppoe {ini.iosv_1.bba_group_name}",
      f"{ini.iosv_1.vt1.name}",
    ],
    # virtual template settings
    [
      f"interface {ini.iosv_1.vt1.name}",
      f"ip unnumbered {ini.iosv_1.loopback0.name}",
      f"peer default ip address pool {ini.pool_name}",
      # CHAP settings
      f"ppp authentication chap",
    ],
    # IPCP
    [
      f"ip local pool {ini.pool_name} {ini.iosv_2.dialer0.assigned_ip_addr.ip}"
    ],
  ])

  # client
  iosv_2.execs([
    [
      f"interface {ini.iosv_2.g0_0.name}",
      # dialer pool 1に所属するインターフェイスはpppoeを使って接続するように設定
      f"pppoe-client dial-pool-number {ini.iosv_2.dialer0.pool_num}",
      f"no shutdown",
    ],
    # dialer settings
    [
      f"interface {ini.iosv_2.dialer0.name}",
      f"encapsulation ppp",
      # associate Physical I/F and dialer I/F
      f"dialer pool {ini.iosv_2.dialer0.pool_num}",
      f"ip mtu {ini.mtu_size}",
      # IPCP
      f"ip address negotiated",

      # CHAP
      ## do not request authe from client -> server
      f"ppp authentication chap callin",
      f"ppp chap hostname {ini.iosv_1.username}",
      f"ppp chap password {ini.iosv_1.password}",
    ],
  ])

  def populate_router_ping(device: Device, target_ip: str, sleep_time=3):
    @wait.retry(count=30, result=0, sleep_time=sleep_time)
    def _populate_router_ping(device: Device):
      try:
        return parse.router_ping(device, target_ip)
      except Exception as e:
        print(f"populate_router_ping: Exception: {e}")
        return None
    return _populate_router_ping(device)
  
  populate_router_ping(iosv_2, ini.iosv_1.loopback0.ip_addr.ip)

  iosv_1.execs([
    f"show pppoe session",
    f"show pppoe session all",
    f"show ip interface {ini.iosv_1.vt1.access_name}",
    f"show ip interface brief",
    f"show ip route",
  ])

  iosv_2.execs([
    f"show pppoe session",
    f"show pppoe session all",
    f"show interface {ini.iosv_2.dialer0.name}",
    f"show ip interface brief",
    f"show ip route",
  ])
  
if __name__ == '__main__':
  main()
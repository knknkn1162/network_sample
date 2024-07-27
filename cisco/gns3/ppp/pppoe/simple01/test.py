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
  r1 = Device(tb, 'R1')
  r2 = Device(tb, 'R2')

  # server
  r1.execs([
    [
      f"interface {ini.r1.f0_0.name}",
      f"pppoe enable group {ini.r1.bba_group_name}",
      f"no shutdown",
    ],
    # associate phycical I/F <-> virtual-template
    [
      f"bba-group pppoe {ini.r1.bba_group_name}",
      f"{ini.r1.vt1.name}",
    ],
    # virtual template settings
    [
      f"interface {ini.r1.vt1.name}",
      f"ip addr {ini.r1.vt1.ip_addr.ip} {ini.r1.vt1.ip_addr.netmask}",
    ]
  ])

  # client
  r2.execs([
    [
      f"interface {ini.r2.f0_0.name}",
      # dialer pool 1に所属するインターフェイスはpppoeを使って接続するように設定
      f"pppoe-client dial-pool-number {ini.r2.dialer0.pool_num}",
      f"no shutdown",
    ],
    # dialer settings
    [
      f"interface {ini.r2.dialer0.name}",
      f"encapsulation ppp",
      # associate Physical I/F and dialer I/F
      f"dialer pool {ini.r2.dialer0.pool_num}",
      # 0を指定した場合は無通信状態が続いても切断しない
      #f"dialer idle-timeout 0",
      # for OSPF
      f"ip mtu {ini.mtu_size}",
      f"ip address {ini.r2.dialer0.ip_addr.ip} {ini.r2.dialer0.ip_addr.netmask}",
    ],
  ])

  def populate_router_ping(device: Device, target_ip: str, sleep_time=3):
    @wait.retry(count=30, result=0, sleep_time=sleep_time)
    def _populate_router_ping(device: Device):
      return parse.router_ping(device, target_ip)
    return _populate_router_ping(device)
  
  populate_router_ping(r1, ini.r2.dialer0.ip_addr.ip)

  r1.execs([
    f"show pppoe session",
    f"show ip interface {ini.r1.vt1.access_name}",
    f"show ip interface brief",
    f"show ip route",
  ])

  r2.execs([
    f"show pppoe session",
    f"show interface {ini.r2.dialer0.name}",
    f"show ip interface brief",
    f"show ip route",
  ])
  

if __name__ == '__main__':
  main()
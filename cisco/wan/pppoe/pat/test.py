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

  server_1 = Device(tb, 'server_1')

  # server
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
      # 0を指定した場合は無通信状態が続いても切断しない
      #f"dialer idle-timeout 0",
      # for OSPF
      f"ip mtu {ini.mtu_size}",
      # static
      #f"ip address {ini.iosv_2.dialer0.ip_addr.ip} {ini.iosv_2.dialer0.ip_addr.netmask}",
      # IPCP
      f"ip address negotiated",
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

  # PAT settings
  server_1.execs([

    f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
    f"sudo ifconfig eth0 {ini.server_1.eth0.ip_addr.ip} netmask {ini.server_1.eth0.ip_addr.netmask} up",
    f"sudo route add default gw {ini.iosv_2.g0_1.ip_addr.ip}",
    f"ifconfig eth0",
    f"route -e",
  ])

  iosv_2.execs([
    [
      f"interface {ini.iosv_2.g0_1.name}",
      f"ip address {ini.iosv_2.g0_1.ip_addr.ip} {ini.iosv_2.g0_1.ip_addr.netmask}",
      f"ip nat inside",
      f"no shutdown",
    ],
    [
      f"interface {ini.iosv_2.dialer0.name}",
      f"ip nat outside",
    ],
    [
      f"ip route 0.0.0.0 0.0.0.0 {ini.iosv_2.dialer0.name}",
    ],
    # PAT settings
    [
      f"access-list {ini.acl_num} permit {ini.iosv_2.g0_1.ip_addr.network.network_address} {ini.iosv_2.g0_1.ip_addr.hostmask}",
      f"ip nat inside source list {ini.acl_num} interface {ini.iosv_2.dialer0.name} overload",
    ]
  ])

  wait.seconds(30)
  server_1.server_ping(ini.iosv_1.loopback0.ip_addr.ip)
  iosv_2.execs([
    f"show ip nat translations",
  ])
  
if __name__ == '__main__':
  main()
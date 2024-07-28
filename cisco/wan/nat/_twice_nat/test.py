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
  iosv_0 = Device(tb, ini.iosv_0.__name__)

  server_0 = Device(tb, ini.server_0.__name__)
  server_1 = Device(tb, ini.server_1.__name__)
  print("####### exec #######")
  cml = Cml()

  # server setup
  server_0.execs([
    # eth0 setting
    ## disable DHCP
    f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
    f"sudo ifconfig eth0 {ini.server_0.eth0.ip_addr.ip} netmask {ini.server_0.eth0.ip_addr.netmask} up",
    f"sudo route add default gw {ini.iosv_0.g0_0.ip_addr.ip}",
    f"ifconfig eth0",
    f"route -e",
  ])

  # server setup
  server_1.execs([
    # eth0 setting
    ## disable DHCP
    f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
    f"sudo ifconfig eth0 {ini.server_1.eth0.ip_addr.ip} netmask {ini.server_1.eth0.ip_addr.netmask} up",
    f"sudo route add default gw {ini.iosv_0.g0_1.ip_addr.ip}",
    f"ifconfig eth0",
    f"route -e",
  ])

  iosv_0.execs([
    [
      f"interface {ini.iosv_0.g0_0.name}",
      f"ip addr {ini.iosv_0.g0_0.ip_addr.ip} {ini.iosv_0.g0_0.ip_addr.netmask}",
      f"no shutdown",
    ],
    [
      f"interface {ini.iosv_0.g0_1.name}",
      f"ip addr {ini.iosv_0.g0_1.ip_addr.ip} {ini.iosv_0.g0_1.ip_addr.netmask}",
      f"no shutdown",
    ],
  ])

  # twice nat
  iosv_0.execs([
    [
      f"interface {ini.iosv_0.g0_0.name}",
      f"ip nat inside"
    ],
    [
      f"interface {ini.iosv_0.g0_1.name}",
      f"ip nat outside"
    ],
    [
      f"ip nat inside source static {ini.server_0.eth0.ip_addr.ip} {ini.iosv_0.g0_1.inside_global_ip.ip}",
      f"ip nat outside source static {ini.server_1.eth0.ip_addr.ip} {ini.iosv_0.g0_0.inside_local_ip.ip}",
      # route first, NAT second
      f"ip route {ini.iosv_0.g0_0.inside_local_ip.ip} 255.255.255.255 {ini.iosv_0.g0_1.name}",
    ]
  ])

  def populate_server_ping(device: Device, target_ip: str):
    @wait.retry(count=30, result=0, sleep_time=3)
    def _do(device: Device):
      return device.server_ping(target_ip)
    return _do(device)

  populate_server_ping(server_0, ini.server_1.eth0.ip_addr.ip)
  # even if server_0 doesn't know the g0_1 network, we can ping
  populate_server_ping(server_0, ini.iosv_0.g0_0.inside_local_ip.ip)
  populate_server_ping(server_1, ini.iosv_0.g0_1.inside_global_ip.ip)

if __name__ == '__main__':
  main()
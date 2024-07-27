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

  r1.execs([
    [
      f"interface {ini.r1.s2_0.name}",
      f"encapsulation frame-relay",
      # associate DLCI adn Virtual-Template
      f"frame-relay interface-dlci {ini.r1.s2_0.dlci_num} ppp {ini.r1.vt1.name}",
      f"no shutdown",
    ],
    [
      f"interface {ini.r1.vt1.name}",
      f"ip address {ini.r1.vt1.ip_addr.ip} {ini.r1.vt1.ip_addr.netmask}",
      f"no shutdown",
    ],
  ])

  r2.execs([
    [
      f"interface {ini.r2.s2_0.name}",
      f"encapsulation frame-relay",
      # associate DLCI adn Virtual-Template
      f"frame-relay interface-dlci {ini.r2.s2_0.dlci_num} ppp {ini.r2.vt1.name}",
      f"no shutdown",
    ],
    [
      f"interface {ini.r2.vt1.name}",
      f"ip address {ini.r2.vt1.ip_addr.ip} {ini.r2.vt1.ip_addr.netmask}",
      f"no shutdown",
    ],
  ])

  def populate_router_ping(device: Device, target_ip: str, sleep_time=3):
    @wait.retry(count=30, result=0, sleep_time=sleep_time)
    def _populate_router_ping(device: Device):
      return parse.router_ping(device, target_ip)
    return _populate_router_ping(device)
  
  populate_router_ping(r1, ini.r2.vt1.ip_addr.ip)

  r1.execs([
    f"show ip interface brief",
  ])

  r2.execs([
    f"show ip interface brief",
  ])
  

if __name__ == '__main__':
  main()
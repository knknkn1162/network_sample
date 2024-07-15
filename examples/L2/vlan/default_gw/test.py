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

  iosv_0 = Device(tb, 'iosv_0')
  iosvl2_0 = Device(tb, 'iosvl2_0')

  server_0 = Device(tb, 'server_0')
  server_1 = Device(tb, 'server_1')

  cml0 = Cml()
  print("####### exec #######")

  # server settings -> DHCP enable by default
  server_0.execs([
    # eth0 setting
    ## disable DHCP
    f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
    f"sudo ifconfig eth0 {ini.server_0.eth0.ip_addr} netmask {ini.server_0.eth0.subnet_mask} up",
    f"sudo route add default gw {ini.iosv_0.g0_0.ip_addr}",
    f"ifconfig eth0",
    f"route -e",
  ])

  server_1.execs([
    # eth0 setting
    ## disable DHCP
    f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
    f"sudo ifconfig eth0 {ini.server_1.eth0.ip_addr} netmask {ini.server_1.eth0.subnet_mask} up",
    f"sudo route add default gw {ini.iosv_0.g0_1.ip_addr}",
    f"ifconfig eth0",
    f"route -e",
  ])

  # interface up
  iosv_0.execs([
    [
      f"interface {ini.iosv_0.g0_0.name}",
      f"ip addr {ini.iosv_0.g0_0.ip_addr} {ini.iosv_0.g0_0.subnet_mask}",
      f"no shutdown"
    ],
    [
      f"interface {ini.iosv_0.g0_1.name}",
      f"ip addr {ini.iosv_0.g0_1.ip_addr} {ini.iosv_0.g0_1.subnet_mask}",
      f"no shutdown"
    ],
  ])

  iosvl2_0.execs([
    [
      # disable l3 switch
      f"no ip routing",
    ],
    # set ip
    [
      f"interface {ini.iosvl2_0.vlan1.name}",
      f"ip address {ini.iosvl2_0.vlan1.ip_addr} {ini.iosvl2_0.vlan1.subnet_mask}",
      f"no shutdown"
    ],
    # # telnet settings
    # [
    #   f"line vty 0 4",
    #   f"password {ini.iosvl2_0.vty_password}",
    #   f"login",
    #   f"transport input telnet",
    #   # for auto-test, comment out
    #   #f"enable secret {ini.iosvl2_0.enable_password}"
    # ],
  ])

  wait_until.populate_up(iosv_0, 2)
  wait_until.populate_up(iosvl2_0, 3)

  server_0.server_ping(ini.server_1.eth0.ip_addr)
  iosvl2_0.execs([
    [
      f"ip default-gateway {ini.iosv_0.g0_0.ip_addr}",
    ]
  ])

  server_0.server_ping(ini.server_1.eth0.ip_addr, count=30)
  # server_0.execs([
  #   f"telnet {ini.iosvl2_0.vlan1.ip_addr}"
  # ])

  # # TODO: it should fail, but it actually works.
  # server_1.execs([
  #   f"timeout -sKILL 10 telnet {ini.iosvl2_0.vlan1.ip_addr}"
  # ])

  # iosvl2_0.execs([
  #   [
  #     f"ip default-gateway {ini.iosv_0.g0_0.ip_addr}",
  #   ]
  # ])

  # server_0.execs([
  #   f"telnet {ini.iosvl2_0.vlan1.ip_addr}"
  # ])

  # # success
  # server_1.execs([
  #   f"telnet {ini.iosvl2_0.vlan1.ip_addr}"
  # ])



if __name__ == '__main__':
  main()
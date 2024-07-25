from genie import testbed
from conf import CONFIG_YAML
from lib.device import Device
from lib import wait, ipv4
import ini
import time
import wait_until, calc

tb = testbed.load(CONFIG_YAML)

# switch
r1 = Device(tb, 'R1')
r2 = Device(tb, 'R2')
pc1 = Device(tb, 'pc1')
pc2 = Device(tb, 'pc2')

# ip
pc1.execs([
  f"ip {ini.pc1.eth0.ip_addr} {ini.pc1.eth0.subnet_mask} {ini.r1.g0_0.ip_addr}",
  f"show",
])

pc2.execs([
  f"ip {ini.pc2.eth0.ip_addr} {ini.pc2.eth0.subnet_mask} {ini.r2.g0_0.ip_addr}",
  f"show",
])

# ppp setting
pc2_network0 = ipv4.get_network0(ini.pc2.eth0.ip_addr, ini.pc2.eth0.subnet_mask)
r1.execs([
  [
    f"interface {ini.r1.g0_0.name}",
    f"ip addr {ini.r1.g0_0.ip_addr} {ini.r1.g0_0.subnet_mask}",
    f"no shutdown",
  ],
  [
    f"interface {ini.r1.s0_0.name}",
    f"encapsulation ppp",
    f"ip addr {ini.r1.s0_0.ip_addr} {ini.r1.s0_0.subnet_mask}",
    f"no shutdown",
  ],
  [
    f"ip route {pc2_network0} {ini.pc2.eth0.subnet_mask} {ini.r2.s0_0.ip_addr}",
  ],
])

pc1_network0 = ipv4.get_network0(ini.pc1.eth0.ip_addr, ini.pc1.eth0.subnet_mask)
r2.execs([
  [
    f"interface {ini.r2.g0_0.name}",
    f"ip addr {ini.r2.g0_0.ip_addr} {ini.r2.g0_0.subnet_mask}",
    f"no shutdown",
  ],
  [
    f"interface {ini.r2.s0_0.name}",
    f"encapsulation ppp",
    f"ip addr {ini.r2.s0_0.ip_addr} {ini.r2.s0_0.subnet_mask}",
    f"no shutdown",
  ],
  [
    f"ip route {pc1_network0} {ini.pc1.eth0.subnet_mask} {ini.r1.s0_0.ip_addr}",
  ],
])

# test ping
calc.vpcs_ping(pc1, ini.pc2.eth0.ip_addr, count=15)

# PAP settings
r1.execs([
  [
    f"username {ini.r1.username} password {ini.r1.password}",
  ],
])
r2.execs([
  [
    f"username {ini.r2.username} password {ini.r2.password}",
  ]
])

r1.execs([
  [
    f"interface {ini.r1.s0_0.name}",
    f"ppp authentication pap",
    f"ppp pap sent-username {ini.r2.username} password {ini.r2.password}",
  ],
])

r2.execs([
  [
    f"interface {ini.r2.s0_0.name}",
    f"ppp authentication pap",
    f"ppp pap sent-username {ini.r1.username} password {ini.r1.password}",
  ],
])

# test ping
calc.vpcs_ping(pc1, ini.pc2.eth0.ip_addr, count=15)
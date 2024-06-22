from genie import testbed
from cml import CONFIG_YAML, Cml
from lib.device import Device
from lib import wait, ipv4
import ini
import time
import wait_until


tb = testbed.load(CONFIG_YAML)
cml = Cml()
lab = cml.lab

# tinylinux
server_0 = Device(tb, 'server_0')
server_srv = Device(tb, 'server_srv')

# router
iosv_0 = Device(tb, 'iosv_0')
iosv_1 = Device(tb, 'iosv_1')
iosv_isp = Device(tb, 'iosv_isp')



print("####### exec #######")
server_0.execs([
  # eth0 setting
  ## disable DHCP
  f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
  f"sudo ifconfig eth0 {ini.server_0.eth0.ip_addr} netmask {ini.server_0.eth0.subnet_mask} up",
  f"sudo route add default gw {ini.iosv_0.g0_1.ip_addr}",
  f"ifconfig eth0",
  f"route -e",
])

server_srv.execs([
  # eth0 setting
  ## disable DHCP
  f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
  f"sudo ifconfig eth0 {ini.server_srv.eth0.ip_addr} netmask {ini.server_srv.eth0.subnet_mask} up",
  f"sudo route add default gw {ini.iosv_isp.g0_1.ip_addr}",
  f"ifconfig eth0",
  f"route -e",
])

# up
iosv_0.execs([
  [
    f"interface {ini.iosv_0.g0_0.name}",
    f"ip addr {ini.iosv_0.g0_0.ip_addr} {ini.iosv_0.g0_0.subnet_mask}",
    f"no shutdown"
  ],
  [
    f"interface {ini.iosv_0.g0_1.name}",
    f"ip addr {ini.iosv_0.g0_1.ip_addr} {ini.iosv_0.g0_1.subnet_mask}",
    f"no shutdown",
  ],
  f"show ip interface brief",
])

wait_until.populate_up(iosv_0, count=2)

iosv_1.execs([
  [
    f"interface {ini.iosv_1.g0_0.name}",
    f"ip addr {ini.iosv_1.g0_0.ip_addr} {ini.iosv_1.g0_0.subnet_mask}",
    f"no shutdown"
  ],
  [
    f"interface {ini.iosv_1.g0_1.name}",
    f"ip addr {ini.iosv_1.g0_1.ip_addr} {ini.iosv_1.g0_1.subnet_mask}",
    f"no shutdown"
  ],
  f"show ip interface brief",
])

wait_until.populate_up(iosv_0, count=2)

iosv_isp.execs([
  [
    f"interface {ini.iosv_isp.g0_0.name}",
    f"ip addr {ini.iosv_isp.g0_0.ip_addr} {ini.iosv_isp.g0_0.subnet_mask}",
    f"no shutdown"
  ],
  [
    f"interface {ini.iosv_isp.g0_1.name}",
    f"ip addr {ini.iosv_isp.g0_1.ip_addr} {ini.iosv_isp.g0_1.subnet_mask}",
    f"no shutdown"
  ],
  f"show ip interface brief",
])

wait_until.populate_up(iosv_0, count=2)

# rip settings @ iosv_0
iosv_0_g0_0_addr0 = ipv4.get_network0(ini.iosv_0.g0_0.ip_addr, ini.iosv_0.g0_0.subnet_mask)
iosv_0_g0_1_addr0 = ipv4.get_network0(ini.iosv_0.g0_1.ip_addr, ini.iosv_0.g0_1.subnet_mask)
iosv_0.execs([
  [
    f"router rip",
    f"version 2",
    f"network {iosv_0_g0_0_addr0}",
    f"network {iosv_0_g0_1_addr0}",
    f"no auto-summary",
  ]
])

# rip settings @ iosv_1
iosv_1_addr0 = ipv4.get_network0(ini.iosv_1.g0_0.ip_addr, ini.iosv_1.g0_0.subnet_mask)
iosv_1.execs([
  [
    # default route setting
    f"ip route 0.0.0.0 0.0.0.0 {ini.iosv_isp.g0_0.ip_addr}"
  ],
  [
    f"router rip",
    f"version 2",
    f"network {iosv_1_addr0}",
    f"no auto-summary",
    # we want to advertise route include default route
    f"default-information originate",
  ],
])

wait_until.populate_static(iosv_1)
wait_until.populate_rip(iosv_0)
# test ping
wait_until.populate_router_ping(iosv_1, ini.server_srv.eth0.ip_addr)

# boundary between nat inside and nat outside
server_0_addr0 = ipv4.get_network0(ini.server_0.eth0.ip_addr, ini.server_0.eth0.subnet_mask)
iosv_1.execs([
  # -[in]-> [g0_0 -> g0_1] -[out]->
  [
    f"interface {ini.iosv_1.g0_0.name}",
    f"ip nat inside",
  ],
  [
    f"interface {ini.iosv_1.g0_1.name}",
    f"ip nat outside",
  ],
  # for permit ping from server_0 -> server_srv
  [
    f"ip nat inside source list 1 interface {ini.iosv_isp.g0_1.name} overload",
    f"access-list 1 permit {server_0_addr0} {ini.INVERSE_MASK_24}"
  ],
  f"show running-config | include ip nat",
  # assume that there are no items
  f"show ip nat translations",
])

# test ping
wait_until.populate_server_ping(server_0, ini.server_srv.eth0.ip_addr)

# check NAT table and statistics
iosv_1.execs([
  f"show ip nat translations",
  f"show ip nat statistics",
  f"show ip access-lists",
])

# reflexive access list setting
in_acl_name = "FROM_INET"
out_acl_name = "TO_INET"
ref_acl_name = "REF"
iosv_1.execs([
  ## in
  [
    f"ip access-list extended {in_acl_name}",
    f"evaluate {ref_acl_name}",
    f"deny ip any any",
  ],
  ## out
  [
    f"ip access-list extended {out_acl_name}",
    # add reflexive item in ACL table automatically
    f"permit ip any any reflect {ref_acl_name}"
  ],
  [
    f"interface {ini.iosv_1.g0_1.name}",
    f"ip access-group {in_acl_name} in",
    f"ip access-group {out_acl_name} out",
  ],
  f"show ip access-lists",
])

# test ping
wait_until.populate_server_ping(server_0, ini.server_srv.eth0.ip_addr)

# check NAT table and statistics
iosv_1.execs([
  f"show ip nat translations",
  f"show ip nat statistics",
  f"show ip access-lists",
])
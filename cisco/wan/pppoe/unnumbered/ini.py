from ipaddress import ip_interface

mtu_size = 1492
pool_name = "TESTPOOL01"
acl_num = 1
# PPPoE server
class iosv_1:
   bba_group_name = "BBA01"
   class g0_0:
      name = "GigabitEthernet0/0"
   class vt1:
      name = "Virtual-Template 1"
      access_name = "Virtual-Access 1.1"
   # used for unnumbered
   class loopback0:
      name = "loopback 0"
      ip_addr = ip_interface("10.0.0.100/32")
   class loopback1:
      name = "loopback 1"
      ip_addr = ip_interface("10.0.0.200/32")

# PPPoE client
class iosv_2:
   class g0_0:
      name = "GigabitEthernet0/0"
   class g0_1:
      name = "GigabitEthernet0/1"
      ip_addr = ip_interface("192.168.0.254/24")
   class dialer0:
      pool_num = 1
      name = "Dialer 0"
   class loopback0:
      name = "loopback 0"
      ip_addr = ip_interface("10.0.0.1/32")
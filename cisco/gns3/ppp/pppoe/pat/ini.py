from ipaddress import ip_interface

mtu_size = 1492
pool_name = "TESTPOOL01"
acl_num = 1
# PPPoE server
class r1:
   bba_group_name = "BBA01"
   class f0_0:
      name = "FastEthernet0/0"
   class vt1:
      name = "Virtual-Template 1"
      access_name = "Virtual-Access 1.1"
      ip_addr = ip_interface("192.168.12.1/24")
   class loopback0:
      name = "loopback 0"
      ip_addr = ip_interface("10.0.0.100/32")

# PPPoE client
class r2:
   class f0_0:
      name = "FastEthernet0/0"
   class f0_1:
      name = "FastEthernet0/1"
      ip_addr = ip_interface("192.168.0.254/24")
   class dialer0:
      pool_num = 1
      name = "Dialer 0"
      # static
      assigned_ip_addr = ip_interface("10.0.0.1/32")

class pc1:
   class eth0:
      ip_addr = ip_interface("192.168.0.1/24")

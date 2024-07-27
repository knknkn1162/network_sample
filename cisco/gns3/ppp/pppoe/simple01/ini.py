from ipaddress import ip_interface

mtu_size = 1492
# PPPoE server
class r1:
   bba_group_name = "BBA01"
   class f0_0:
      name = "FastEthernet0/0"
   class vt1:
      name = "Virtual-Template 1"
      access_name = "Virtual-Access 1.1"
      ip_addr = ip_interface("192.168.12.1/24")

# PPPoE client
class r2:
   class f0_0:
      name = "FastEthernet0/0"
   class dialer0:
      pool_num = 1
      name = "Dialer 0"
      # static
      ip_addr = ip_interface("192.168.12.2/24")

from ipaddress import ip_interface

class iosv_0:
  class g0_0:
    name = "GigabitEthernet0/0"
    ip_addr = ip_interface("192.168.0.254/24")
    inside_local_ip = ip_interface("192.168.0.253/24")
  class g0_1:
    name = "GigabitEthernet0/1"
    ip_addr = ip_interface("192.168.1.254/24")
    inside_global_ip = ip_interface("192.168.1.253/24")

class server_0:
   class eth0:
      name = "eth0"
      ip_addr = ip_interface("192.168.0.1/24")

class server_1:
   class eth0:
      name = "eth0"
      ip_addr = ip_interface("192.168.1.1/24")
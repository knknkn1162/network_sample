from ipaddress import ip_interface
acl_num = 1
dns_server_addr = "8.8.8.8"
target_fqdn = "google.co.jp"
class r1:
  name = "R1"
  class f0_0:
    name = "FastEthernet0/0"
    ip_addr = ip_interface("10.0.0.254/24")
  class f0_1:
    name = "FastEthernet0/1"
      

class pc1:
    class eth0:
       ip_addr = ip_interface("10.0.0.1/24")

class pc2:
    class eth0:
       ip_addr = ip_interface("10.0.0.2/24")

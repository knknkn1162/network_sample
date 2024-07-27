from ipaddress import ip_interface

class r1:
   class s2_0:
      name = "Serial 2/0"
      ip_addr = ip_interface("192.168.1.1/24")


class r2:
   class s2_0:
      name = "Serial 2/0"
      expected_ip_addr = ip_interface("192.168.1.2/24")

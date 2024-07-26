from ipaddress import ip_interface
SUBNET_MASK_24 = "255.255.255.0"
INVERSE_MASK_24 = "0.0.0.255"

class vyos0:
   class eth0:
      ip_addr = ip_interface("192.168.1.1/24")
   class eth1:
      ip_addr = ip_interface("192.168.0.254/24")
   class loop:
      ip_addr = ip_interface("10.0.0.1/32")

class vyos1:
   class eth0:
      ip_addr = ip_interface("192.168.1.2/24")
   class eth1:
      ip_addr = ip_interface("192.168.2.2/24")
   class loop:
      ip_addr = ip_interface("10.0.0.2/32")

class vyos2:
   class eth0:
      ip_addr = ip_interface("192.168.2.3/24")
   class eth1:
      ip_addr = ip_interface("192.168.3.254/24")
   class loop:
      ip_addr = ip_interface("10.0.0.3/32")

class pc1:
    class eth0:
      ip_addr = ip_interface("192.168.0.1/24")

class pc2:
    class eth0:
      ip_addr = ip_interface("192.168.3.1/24")

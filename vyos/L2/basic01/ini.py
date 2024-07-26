from ipaddress import ip_interface
SUBNET_MASK_24 = "255.255.255.0"
INVERSE_MASK_24 = "0.0.0.255"
pcap_file = "test.pcap"
class vyos0:
   class br0:
      ip_addr = ip_interface("192.168.0.100/24")

class pc1:
    class eth0:
       ip_addr = ip_interface("192.168.0.1/24")

class pc2:
    class eth0:
       ip_addr = ip_interface("192.168.0.2/24")
from ipaddress import ip_interface
SUBNET_MASK_24 = "255.255.255.0"
INVERSE_MASK_24 = "0.0.0.255"
pcap_file = "test.pcap"
class vyos0:
   class eth0:
      ip_addr = ip_interface("192.168.0.1/24")
      class dhcp:
         label = "LAN01"
         start = ip_interface("192.168.0.3/24")
         end = ip_interface("192.168.0.254/24")
         exclude_address = ip_interface("192.168.0.254/24")

class pc1:
    class eth0:
       expected_ip_addrs = [ip_interface("192.168.0.3/24"), ip_interface("192.168.0.4/24")]

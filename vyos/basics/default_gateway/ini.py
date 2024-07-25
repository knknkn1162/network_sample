SUBNET_MASK_24 = "255.255.255.0"
INVERSE_MASK_24 = "0.0.0.255"
pcap_file = "test.pcap"

class vyos0:
   class eth0:
      ip_addr = "192.168.0.254"
      prefix_len = 24

class pc1:
    class eth0:
      ip_addr = "192.168.0.1"
      subnet_mask = SUBNET_MASK_24
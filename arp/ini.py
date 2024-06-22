SUBNET_MASK_24 = "255.255.255.0"
SUBNET_MASK_32 = "255.255.255.255"
INVERSE_MASK_24 = "0.0.0.255"
pcap_file="test.pcap"

class iosvl2_0:
  class g0_0:
    slot = 0
  class g0_1:
    slot = 1

class server_0:
  class eth0:
    slot = 0
    ip_addr = "192.168.0.1"
    subnet_mask = SUBNET_MASK_24

class server_1:
  class eth0:
    slot = 0
    ip_addr = "192.168.0.2"
    subnet_mask = SUBNET_MASK_24
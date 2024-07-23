SUBNET_MASK_24 = "255.255.255.0"
INVERSE_MASK_24 = "0.0.0.255"
pcap01_file = "test01.pcap"
default_gw = "192.168.0.254"

class sw_0:
   class port0:
      name = "port0"
      slot = 0
   class port1:
      name = "port1"
      slot = 1

class ubuntu_0:
   class ens2:
      ip_addr = "192.168.0.2"
      subnet_mask = SUBNET_MASK_24
      prefix_len = 24
      default_gw = default_gw

class ubuntu_1:
   class ens2:
      pass
   class ens3:
      ip_addr = "192.168.0.1"
      subnet_mask = SUBNET_MASK_24
      prefix_len = 24
      default_gw = default_gw

class ext_conn0:
   pass
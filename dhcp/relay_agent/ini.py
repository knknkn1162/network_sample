SUBNET_MASK_24 = "255.255.255.0"
SUBNET_MASK_32 = "255.255.255.255"
INVERSE_MASK_24 = "0.0.0.255"
dhcp_pool_name = "DHCPPOOL"
pcap_file = "test.pcap"

class iosv_0:
  class g0_0:
    name = "GigabitEthernet0/0"
    slot = 0
    ip_addr = "192.168.1.254"
    subnet_mask = SUBNET_MASK_24
  class g0_1:
    name = "GigabitEthernet0/1"
    slot = 1
    ip_addr = "192.168.2.1"
    subnet_mask = SUBNET_MASK_24

class iosv_1:
  class g0_0:
    name = "GigabitEthernet0/0"
    slot = 0
    ip_addr = "192.168.2.2"
    subnet_mask = SUBNET_MASK_24


class switch_0:
  class port0:
    slot = 0
  class port1:
    slot = 1
  class port2:
    slot = 2
   

class server_0:
   class eth0:
      name = "eth0"
      slot = 0
class server_1:
   class eth0:
      name = "eth0"
      slot = 0
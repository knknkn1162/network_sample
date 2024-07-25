SUBNET_MASK_24 = "255.255.255.0"
SUBNET_MASK_32 = "255.255.255.255"
INVERSE_MASK_24 = "0.0.0.255"
pcap0_file = "test0.pcap"
pcap1_file = "test1.pcap"
eigrp_num = 1
BANDWIDTH0=100000


class iosv_0:
  class g0_0:
    name = "GigabitEthernet0/0"
    slot = 0
    ip_addr = "192.168.0.1"
    subnet_mask = SUBNET_MASK_24
    bandwidth = BANDWIDTH0
  class g0_1:
    name = "GigabitEthernet0/1"
    slot = 1
    ip_addr = "192.168.1.1"
    subnet_mask = SUBNET_MASK_24
  class g0_2:
    name = "GigabitEthernet0/2"
    slot = 2
    ip_addr = "192.168.10.254"
    subnet_mask = SUBNET_MASK_24
  
class iosv_1:
  class g0_0:
    name = "GigabitEthernet0/0"
    slot = 0
    ip_addr = "192.168.1.2"
    subnet_mask = SUBNET_MASK_24
  class g0_1:
    name = "GigabitEthernet0/1"
    slot = 1
    ip_addr = "192.168.2.2"
    subnet_mask = SUBNET_MASK_24

class iosv_2:
  class g0_0:
    name = "GigabitEthernet0/0"
    slot = 0
    ip_addr = "192.168.2.3"
    subnet_mask = SUBNET_MASK_24
  class g0_1:
    name = "GigabitEthernet0/1"
    slot = 1
    ip_addr = "192.168.0.3"
    subnet_mask = SUBNET_MASK_24
    bandwidth = BANDWIDTH0
  class loopback0:
    name = "loopback 0"
    ip_addr = "30.0.0.1"
    subnet_mask = SUBNET_MASK_24

class server_0:
    class eth0:
      slot = 0
      ip_addr = "192.168.10.1"
      subnet_mask = SUBNET_MASK_24
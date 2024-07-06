SUBNET_MASK_24 = "255.255.255.0"
SUBNET_MASK_32 = "255.255.255.255"
INVERSE_MASK_24 = "0.0.0.255"
ospf_process_id = 11
pcap0_file = "test0.pcap"
pcap1_file = "test1.pcap"
from lib import ipv4

class iosv_0:
  class g0_0:
    name = "GigabitEthernet0/0"
    slot = 0
    ip_addr = "192.168.0.1"
    subnet_mask = SUBNET_MASK_24
    area_id = 0
    test1_priority = 100
iosv_network0 = ipv4.get_network0(iosv_0.g0_0.ip_addr, iosv_0.g0_0.subnet_mask)

class iosv_1:
  test1_router_id = "192.168.100.100"
  class g0_0:
    name = "GigabitEthernet0/0"
    slot = 0
    ip_addr = "192.168.0.2"
    subnet_mask = SUBNET_MASK_24
    area_id = 0

class iosv_2:
  class g0_0:
    name = "GigabitEthernet0/0"
    slot = 0
    ip_addr = "192.168.0.3"
    subnet_mask = SUBNET_MASK_24
    area_id = 0

class iosv_3:
  class g0_0:
    name = "GigabitEthernet0/0"
    slot = 0
    ip_addr = "192.168.0.4"
    subnet_mask = SUBNET_MASK_24
    area_id = 0

class switch_0:
  class port0:
    slot = 0
  class port1:
    slot = 1
  class port2:
    slot = 2
  class port3:
    slot = 3
SUBNET_MASK_24 = "255.255.255.0"
INVERSE_MASK_24 = "0.0.0.255"
pcap01_file = "test01.pcap"

class channel0:
   num = 1
   name = "Port-channel1"
class channel1:
   num = 2
   name = "Port-channel2"

class iosvl2_0:
   class g0_0:
      name = "GigabitEthernet0/0"
   class g0_1:
      name = "GigabitEthernet0/1"
   ether_channel = channel0

class iosvl2_1:
   class g0_0:
      name = "GigabitEthernet0/0"
   class g0_1:
      name = "GigabitEthernet0/1"
   ether_channel = channel1

class server_0:
   class eth0:
      name = "eth0"
      slot = 0
      ip_addr = "192.168.0.1"
      subnet_mask = SUBNET_MASK_24

class server_1:
   class eth0:
      name = "eth0"
      slot = 0
      ip_addr = "192.168.0.2"
      subnet_mask = SUBNET_MASK_24

class server_2:
   class eth0:
      name = "eth0"
      slot = 0
      ip_addr = "192.168.0.3"
      subnet_mask = SUBNET_MASK_24
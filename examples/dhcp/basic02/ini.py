SUBNET_MASK_24 = "255.255.255.0"
INVERSE_MASK_24 = "0.0.0.255"
pcap_file = "test.pcap"

class iosvl2_0:
   class g0_0:
      name = "GigabitEthernet0/0"
      slot = 0
   class g0_1:
      name = "GigabitEthernet0/1"
      slot = 1
   class g0_2:
      name = "GigabitEthernet0/2"
      slot = 2
   class g0_3:
      name = "GigabitEthernet0/3"
      slot = 3

class iosv_0:
   class g0_0:
      name = "GigabitEthernet0/0"
      slot = 0
      ip_addr = "192.168.0.254"
      subnet_mask = SUBNET_MASK_24

class iosv_1:
   class g0_0:
      name = "GigabitEthernet0/0"
      slot = 0

class server_0:
   class eth0:
      name = "eth0"
      slot = 0

class server_1:
   class eth0:
      name = "eth0"
      slot = 0
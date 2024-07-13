SUBNET_MASK_24 = "255.255.255.0"
INVERSE_MASK_24 = "0.0.0.255"
pcap01 = "test01.pcap"
pcap02 = "test02.pcap"
pcap13 = "test13.pcap"
pcap23 = "test23.pcap"
vlan_num = 10

class iosvl2_0:
   stp_priority = 4096
   class g0_0:
      name = "GigabitEthernet0/0"
   class g0_1:
      name = "GigabitEthernet0/1"
   class g0_2:
      name = "GigabitEthernet0/2"

class iosvl2_1:
   stp_priority = 8192
   class g0_0:
      name = "GigabitEthernet0/0"
   class g0_1:
      name = "GigabitEthernet0/1"

class iosvl2_2:
   stp_priority = 12288
   class g0_0:
      name = "GigabitEthernet0/0"
   class g0_1:
      name = "GigabitEthernet0/1"

class iosvl2_3:
   stp_priority = 12288
   class g0_0:
      name = "GigabitEthernet0/0"
   class g0_1:
      name = "GigabitEthernet0/1"
   class g0_2:
      name = "GigabitEthernet0/2"

class server_0:
   class eth0:
      ip_addr = "192.168.0.1"
      subnet_mask = SUBNET_MASK_24

class server_1:
   class eth0:
      ip_addr = "192.168.0.2"
      subnet_mask = SUBNET_MASK_24
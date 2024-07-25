SUBNET_MASK_24 = "255.255.255.0"
INVERSE_MASK_24 = "0.0.0.255"
pcap_file = "test.pcap"
vlan_list = [10, 20]

class Vlan:
   class vlan0:
      num = vlan_list[0]
   class vlan1:
      num = vlan_list[1]

class iosvl2_0:
   stp_priority = 0
   class g0_0:
      name = "GigabitEthernet0/0"
      slot = 0
   class g0_1:
      name = "GigabitEthernet0/1"
      slot = 1

class iosvl2_1:
   stp_priority = 4096
   class g0_0:
      name = "GigabitEthernet0/0"
      slot = 0
   class g0_1:
      name = "GigabitEthernet0/1"
      slot = 1

class iosvl2_2:
   stp_priority = 8192
   class g0_0:
      name = "GigabitEthernet0/0"
      slot = 0
   class g0_1:
      name = "GigabitEthernet0/1"
      slot = 1
   class g0_2:
      name = "GigabitEthernet0/2"
      slot = 2
      vlan = Vlan.vlan0
   class g0_3:
      name = "GigabitEthernet0/3"
      slot = 3
      vlan = Vlan.vlan1

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
      ip_addr = "192.168.1.1"
      subnet_mask = SUBNET_MASK_24
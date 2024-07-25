SUBNET_MASK_24 = "255.255.255.0"
VLAN1_ID=2
VLAN2_ID=3
pcap_file="test.pcap"
class vlan1:
   num = 10
   name = "vlan_ex10"
class vlan2:
   num = 20
   name = "vlan_ex20"

class iosvl2_1:
   class g0_0:
      name = "GigabitEthernet0/0"
      slot = 0
      vlan = vlan1
   class g0_1:
      name = "GigabitEthernet0/1"
      slot = 1
      vlan = vlan2
   class g0_2:
      name = "GigabitEthernet0/2"
      slot = 2
      vlan = None # trunk
class iosvl2_2:
   class g0_0:
      name = "GigabitEthernet0/0"
      slot = 0
      vlan = vlan1
   class g0_1:
      name = "GigabitEthernet0/1"
      slot = 1
      vlan = vlan2
   class g0_2:
      name = "GigabitEthernet0/2"
      slot = 2
      vlan = None # trunk

class server_1:
   class eth0:
      name = "eth0"
      slot = 0
      ip_addr = "192.168.0.1"
      subnet_mask = SUBNET_MASK_24

class server_2:
   class eth0:
      name = "eth0"
      slot = 0
      ip_addr = "192.168.0.2"
      subnet_mask = SUBNET_MASK_24

class server_3:
   class eth0:
      name = "eth0"
      slot = 0
      ip_addr = "192.168.0.3"
      subnet_mask = SUBNET_MASK_24

class server_4:
   class eth0:
      name = "eth0"
      slot = 0
      ip_addr = "192.168.0.4"
      subnet_mask = SUBNET_MASK_24
SUBNET_MASK_24 = "255.255.255.0"
INVERSE_MASK_24 = "0.0.0.255"
pcap_file = "test.pcap"
vlan_list = [10, 20, 30]

class Vlan:
   class vlan0:
      num = vlan_list[0]
      name = "test_vlan0"
   class vlan1:
      num = vlan_list[1]
      name = "test_vlan1"
   class vlan2:
      num = vlan_list[2]
      name = "test_vlan2"

class iosvl2_0:
   class g0_0:
      name = "GigabitEthernet0/0"
      slot = 0
      vlan = Vlan.vlan0
   class g0_1:
      name = "GigabitEthernet0/1"
      slot = 1
      vlan = Vlan.vlan1
   class g0_2:
      name = "GigabitEthernet0/2"
      slot = 2
   class g0_3:
      name = "GigabitEthernet0/3"
      slot = 3
      vlan = Vlan.vlan2

class iosv_0:
   class g0_0:
      name = "GigabitEthernet0/0"
      slot = 0
      class sub0:
         # must start from 1
         num = 1
         vlan = Vlan.vlan0
         ip_addr = "192.168.0.254"
         subnet_mask = SUBNET_MASK_24
      class sub1:
         num = 2
         vlan = Vlan.vlan1
         ip_addr = "192.168.10.254"
         subnet_mask = SUBNET_MASK_24

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
      ip_addr = "192.168.10.1"
      subnet_mask = SUBNET_MASK_24

class server_2:
   class eth0:
      name = "eth0"
      slot = 0
      ip_addr = "192.168.10.2"
      subnet_mask = SUBNET_MASK_24
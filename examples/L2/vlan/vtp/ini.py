SUBNET_MASK_24 = "255.255.255.0"
INVERSE_MASK_24 = "0.0.0.255"
pcap_file = "test.pcap"
vtp_domain = "example3338"
vtp_password = "testtest3338"
vlan_list = [10, 20]

class Vlan:
   class vlan0:
      num = vlan_list[0]
      name = "test_vlan0"
   class vlan1:
      num = vlan_list[1]
      name = "test_vlan1"

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
      vlan_num = None

class iosvl2_1:
   class g0_0:
      name = "GigabitEthernet0/0"
      slot = 0
   class g0_1:
      name = "GigabitEthernet0/1"
      slot = 1

class iosvl2_2:
   class g0_0:
      name = "GigabitEthernet0/0"
      slot = 0
   class g0_1:
      name = "GigabitEthernet0/1"
      slot = 1
      vlan = Vlan.vlan0


class server_0:
   class eth0:
      name = "eth0"
      slot = 0
      ip_addr = "192.168.10.1"
      subnet_mask = SUBNET_MASK_24

class server_1:
   class eth0:
      name = "eth0"
      slot = 0
      ip_addr = "192.168.20.2"
      subnet_mask = SUBNET_MASK_24

class server_2:
   class eth0:
      name = "eth0"
      slot = 0
      ip_addr = "192.168.10.3"
      subnet_mask = SUBNET_MASK_24
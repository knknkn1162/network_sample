SUBNET_MASK_24 = "255.255.255.0"
VLAN1_ID=2
VLAN2_ID=3
class iosvl2:
   vlan_list = [VLAN1_ID, VLAN2_ID]
   class g0_0:
      name = "GigabitEthernet0/0"
      slot = 0
      vlan = VLAN1_ID
   class g0_1:
      name = "GigabitEthernet0/1"
      slot = 1
      vlan = VLAN1_ID
   class g0_2:
      name = "GigabitEthernet0/2"
      slot = 2
      vlan = VLAN2_ID
   class g0_3:
      name = "GigabitEthernet0/3"
      slot = 3
      vlan = VLAN2_ID
   class g0_4:
      name = "GigabitEthernet1/0"
      slot = 4
      # routed port
      vlan = None
      ip_addr = "192.168.100.254"
      subnet_mask = SUBNET_MASK_24
   class vlan1:
      num = VLAN1_ID
      ip_addr = "192.168.0.254"
      subnet_mask = SUBNET_MASK_24
   class vlan2:
      num = VLAN2_ID
      ip_addr = "192.168.1.254"
      subnet_mask = SUBNET_MASK_24


class server_1:
   class eth0:
      name = "eth0"
      slot = 0
      ip_addr = "192.168.0.1"
      subnet_mask = SUBNET_MASK_24
      vlan = VLAN1_ID

class server_2:
   class eth0:
      name = "eth0"
      slot = 0
      ip_addr = "192.168.0.1"
      subnet_mask = SUBNET_MASK_24
      vlan = VLAN1_ID


class server_3:
   class eth0:
      name = "eth0"
      slot = 0
      ip_addr = "192.168.1.1"
      subnet_mask = SUBNET_MASK_24
      vlan = VLAN2_ID

class server_4:
   class eth0:
      name = "eth0"
      slot = 0
      ip_addr = "192.168.1.2"
      subnet_mask = SUBNET_MASK_24
      vlan = VLAN2_ID

# for routed port
class server_5:
   class eth0:
      name = "eth0"
      slot = 0
      ip_addr = "192.168.100.1"
      subnet_mask = SUBNET_MASK_24
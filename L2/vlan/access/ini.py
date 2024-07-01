SUBNET_MASK_24 = "255.255.255.0"
SUBNET_MASK_32 = "255.255.255.255"
INVERSE_MASK_24 = "0.0.0.255"

class vlan0:
  num = 1
class vlan1:
  name = "vlan_ex01"
  num = 20
class vlan2:
  name = "vlan_ex02"
  num = 30

class iosvl2_0:
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
    vlan = vlan1
  class g0_3:
    name = "GigabitEthernet0/3"
    slot = 3
    vlan = vlan2

class server_0:
  class eth0:
    slot = 0
    ip_addr = "192.168.0.1"
    subnet_mask = SUBNET_MASK_24

class server_1:
  class eth0:
    slot = 0
    ip_addr = "192.168.0.2"
    subnet_mask = SUBNET_MASK_24

class server_2:
  class eth0:
    slot = 0
    ip_addr = "192.168.0.3"
    subnet_mask = SUBNET_MASK_24

class server_3:
  class eth0:
    slot = 0
    ip_addr = "192.168.0.4"
    subnet_mask = SUBNET_MASK_24
SUBNET_MASK_24 = "255.255.255.0"
SUBNET_MASK_32 = "255.255.255.255"
INVERSE_MASK_24 = "0.0.0.255"
public0_ip = "8.8.8.8"

class iosv_0:
  class g0_0:
    name = "GigabitEthernet0/0"
    slot = 0
    ip_addr = "192.168.0.254"
    subnet_mask = SUBNET_MASK_24
  class g0_1:
    name = "GigabitEthernet0/1"
    slot = 1
    ip_addr = "192.168.1.254"
    subnet_mask = SUBNET_MASK_24

class iosvl2_0:
  vty_password = "test9230"
  enable_password = "test2398"
  class g0_0:
    name = "GigabitEthernet0/0"
    slot = 0
  class g0_1:
    name = "GigabitEthernet0/1"
    slot = 1
  class vlan1:
    name = "vlan 1"
    ip_addr = "192.168.0.2"
    subnet_mask = SUBNET_MASK_24


class server_0:
  class eth0:
    slot = 0
    ip_addr = "192.168.0.1"
    subnet_mask = SUBNET_MASK_24

class server_1:
  class eth0:
    slot = 0
    ip_addr = "192.168.1.1"
    subnet_mask = SUBNET_MASK_24

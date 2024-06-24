SUBNET_MASK_24 = "255.255.255.0"
SUBNET_MASK_32 = "255.255.255.255"
INVERSE_MASK_24 = "0.0.0.255"

class iosv_0:
  as_num = 1
  eigrp_num = 1
  class g0_0:
    name = "GigabitEthernet0/0"
    slot = 0
    ip_addr = "192.168.0.1"
    subnet_mask = SUBNET_MASK_24
  class loopback0:
    name = "loopback 0"
    ip_addr = "10.0.0.1"
    subnet_mask = SUBNET_MASK_32
  
class iosv_1:
  as_num = 2
  network = "10.0.1.0"
  subnet_mask = SUBNET_MASK_24
  class g0_0:
    name = "GigabitEthernet0/0"
    slot = 0
    ip_addr = "192.168.0.2"
    subnet_mask = SUBNET_MASK_24
  class g0_1:
    name = "GigabitEthernet0/1"
    slot = 1
    ip_addr = "192.168.1.2"
    subnet_mask = SUBNET_MASK_24

class iosv_2:
  as_num = 3
  eigrp_num = 1
  network = "10.0.2.0"
  subnet_mask = SUBNET_MASK_24
  class g0_0:
    name = "GigabitEthernet0/0"
    slot = 0
    ip_addr = "192.168.1.3"
    subnet_mask = SUBNET_MASK_24
  class loopback0:
    name = "loopback 0"
    ip_addr = "10.0.1.1"
    subnet_mask = SUBNET_MASK_32
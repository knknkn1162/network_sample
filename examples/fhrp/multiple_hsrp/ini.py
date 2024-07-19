SUBNET_MASK_24 = "255.255.255.0"
SUBNET_MASK_32 = "255.255.255.255"
SUBNET_MASK_23 = "255.255.254.0"
INVERSE_MASK_24 = "0.0.0.255"

class hsrp0:
  group_id = 1
  virtual_ip_addr = "192.168.1.253"

class hsrp1:
  group_id = 2
  virtual_ip_addr = "192.168.1.254"

class iosv_0:
  class g0_0:
    name = "GigabitEthernet0/0"
    slot = 0
    ip_addr = "192.168.1.1"
    subnet_mask = SUBNET_MASK_24
    hsrp0_priority = 110
    hsrp1_priority = 100
  class g0_1:
    name = "GigabitEthernet0/1"
    slot = 1
    ip_addr = "192.168.2.1"
    subnet_mask = SUBNET_MASK_24
    hsrp0_priority = 30

class iosv_1:
  class g0_0:
    name = "GigabitEthernet0/0"
    slot = 0
    ip_addr = "192.168.1.2"
    subnet_mask = SUBNET_MASK_24
    hsrp0_priority = 100
    hsrp1_priority = 110
  class g0_1:
    name = "GigabitEthernet0/1"
    slot = 1
    ip_addr = "192.168.3.2"
    subnet_mask = SUBNET_MASK_24
    hsrp0_priority = 30


class iosv_2:
  class g0_0:
    name = "GigabitEthernet0/0"
    slot = 0
    ip_addr = "192.168.2.3"
    subnet_mask = SUBNET_MASK_24
  class g0_1:
    name = "GigabitEthernet0/1"
    slot = 1
    ip_addr = "192.168.3.3"
    subnet_mask = SUBNET_MASK_24
  class loopback0:
    name = "loopback 0"
    ip_addr = "10.0.0.1"
    subnet_mask = SUBNET_MASK_32

class sw_0:
   class port0:
      name = "port0"
      slot = 0
   class port1:
      name = "port1"
      slot = 1
   class port2:
      name = "port2"
      slot = 2

class server_0:
   class eth0:
      name = "eth0"
      slot = 0
      ip_addr = "192.168.1.10"
      subnet_mask = SUBNET_MASK_24
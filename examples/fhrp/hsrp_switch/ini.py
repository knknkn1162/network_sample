SUBNET_MASK_24 = "255.255.255.0"
SUBNET_MASK_32 = "255.255.255.255"
SUBNET_MASK_23 = "255.255.254.0"
INVERSE_MASK_24 = "0.0.0.255"
pcap_file = "test.pcap"
prio_high = 110
prio_low = 100
vlan0_num = 1
class hsrp0:
  group_id = 1
  virtual_ip_addr = "192.168.1.253"

# class hsrp1:
#   group_id = 2
#   virtual_ip_addr = "192.168.1.254"

class iosvl2_0:
  class g0_0:
    name = "GigabitEthernet0/0"
    slot = 0
  class g0_1:
    name = "GigabitEthernet0/1"
    slot = 1
    ip_addr = "192.168.2.1"
    subnet_mask = SUBNET_MASK_24
  class vlan:
    name = f"vlan {vlan0_num}"
    ip_addr = "192.168.1.100"
    subnet_mask = SUBNET_MASK_24
    hsrp0_priority = prio_high
    #hsrp1_priority = prio_low


class iosvl2_1:
  class g0_0:
    name = "GigabitEthernet0/0"
    slot = 0
  class g0_1:
    name = "GigabitEthernet0/1"
    slot = 1
    ip_addr = "192.168.3.1"
    subnet_mask = SUBNET_MASK_24
  class vlan:
    name = f"vlan {vlan0_num}"
    ip_addr = "192.168.1.101"
    subnet_mask = SUBNET_MASK_24
    hsrp0_priority = prio_low
    #hsrp1_priority = prio_low


class iosv_0:
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
      pass
   class port1:
      pass
   class port2:
      pass
   class port3:
     pass

class server_0:
   class eth0:
      name = "eth0"
      slot = 0
      ip_addr = "192.168.1.10"
      subnet_mask = SUBNET_MASK_24

class server_1:
   class eth0:
      name = "eth0"
      slot = 0
      ip_addr = "192.168.1.11"
      subnet_mask = SUBNET_MASK_24
SUBNET_MASK_24 = "255.255.255.0"
SUBNET_MASK_32 = "255.255.255.255"
SUBNET_MASK_23 = "255.255.254.0"
INVERSE_MASK_24 = "0.0.0.255"
pcap_file = "test.pcap"
hsrp_prio_high = 110
hsrp_prio_low = 100
stp_prio_high = 4096
stp_prio_low = 0
vlan0_num = 10
vlan1_num = 20
class vlan0:
  num = vlan0_num
  name = f"vlan {vlan0_num}"
  virtual_ip_addr = "192.168.10.253"
  subnet_mask = SUBNET_MASK_24
  group_id = 1

class vlan1:
  num = vlan1_num
  name = f"vlan {vlan1_num}"
  virtual_ip_addr = "192.168.20.253"
  subnet_mask = SUBNET_MASK_24
  group_id = 2

class iosvl2_0:
  class g0_0:
    name = "GigabitEthernet0/0"
    slot = 0
  class g0_1:
    name = "GigabitEthernet0/1"
    slot = 1
    ip_addr = "192.168.2.1"
    subnet_mask = SUBNET_MASK_24
  class vlan00:
    vlan = vlan0
    ip_addr = "192.168.10.100"
    hsrp0_priority = hsrp_prio_high
    stp_priority = stp_prio_low
  class vlan01:
    vlan = vlan1
    ip_addr = "192.168.20.100"
    hsrp0_priority = hsrp_prio_low
    stp_priority = stp_prio_high

class iosvl2_1:
  class g0_0:
    name = "GigabitEthernet0/0"
    slot = 0
  class g0_1:
    name = "GigabitEthernet0/1"
    slot = 1
    ip_addr = "192.168.3.1"
    subnet_mask = SUBNET_MASK_24
  class vlan00:
    vlan = vlan0
    ip_addr = "192.168.10.101"
    hsrp0_priority = hsrp_prio_low
    stp_priority = stp_prio_high
  class vlan01:
    vlan = vlan1
    ip_addr = "192.168.20.101"
    hsrp0_priority = hsrp_prio_high
    stp_priority = stp_prio_low


class iosvl2_2:
  class g0_0:
    name = "GigabitEthernet0/0"
    slot = 0
    vlan = vlan0
  class g0_1:
    name = "GigabitEthernet0/1"
    slot = 0
    vlan = vlan1
  class g0_2:
    name = "GigabitEthernet0/2"
    slot = 0
  class g0_3:
    name = "GigabitEthernet0/3"
    slot = 0

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

class server_0:
   class eth0:
      name = "eth0"
      slot = 0
      ip_addr = "192.168.10.10"
      subnet_mask = SUBNET_MASK_24

class server_1:
   class eth0:
      name = "eth0"
      slot = 0
      ip_addr = "192.168.20.11"
      subnet_mask = SUBNET_MASK_24
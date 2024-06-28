SUBNET_MASK_24 = "255.255.255.0"

class iosv_0:
   class g0_0:
      name = "GigabitEthernet0/0"
      slot = 0
      ip_addr = "192.168.1.254"
      subnet_mask = SUBNET_MASK_24
   class g0_1:
      name = "GigabitEthernet0/1"
      slot = 1
      ip_addr = "192.168.0.1"
      subnet_mask = SUBNET_MASK_24
   
class iosv_1:
   class g0_0:
      name = "GigabitEthernet0/0"
      slot = 0
      ip_addr = "192.168.2.254"
      subnet_mask = SUBNET_MASK_24
   class g0_1:
      name = "GigabitEthernet0/1"
      slot = 1
      ip_addr = "192.168.0.2"
      subnet_mask = SUBNET_MASK_24

class server_0:
   class eth0:
      name = "eth0"
      slot = 0
      ip_addr = "192.168.1.100"
      subnet_mask = SUBNET_MASK_24

class server_1:
   class eth0:
      name = "eth0"
      slot = 0
      ip_addr = "192.168.2.100"
      subnet_mask = SUBNET_MASK_24
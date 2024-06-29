SUBNET_MASK_24 = "255.255.255.0"
SUBNET_MASK_32 = "255.255.255.255"
SUBNET_MASK_23 = "255.255.254.0"
INVERSE_MASK_24 = "0.0.0.255"

class snmp_settings:
  viewname = "view001"
  oid_system = "1.3.6.1.2.1.1"
  oid_cisco = "1.3.6.1.4.1.9"
  group_name = "group001"
  user_name = "user001"
  password = "pass2039"

class iosv_0:
  class g0_0:
    name = "GigabitEthernet0/0"
    slot = 0
    ip_addr = "192.168.1.254"
    subnet_mask = SUBNET_MASK_24

class server_0:
   class eth0:
      name = "eth0"
      slot = 0
      ip_addr = "192.168.1.1"
      subnet_mask = SUBNET_MASK_24
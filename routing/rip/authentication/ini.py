SUBNET_MASK_24 = "255.255.255.0"
SUBNET_MASK_32 = "255.255.255.255"
SUBNET_MASK_23 = "255.255.254.0"
INVERSE_MASK_24 = "0.0.0.255"
pcap_file="test.pcap"

class key_chain:
  name = "keychain01"
  id = 1
  password = "pass2934"

class iosv_0:
  class g0_0:
    name = "GigabitEthernet0/0"
    slot = 0
    ip_addr = "10.0.0.1"
    subnet_mask = SUBNET_MASK_24
  
class iosv_1:
  class g0_0:
    name = "GigabitEthernet0/0"
    slot = 0
    ip_addr = "10.0.0.2"
    subnet_mask = SUBNET_MASK_24
  class g0_1:
    name = "GigabitEthernet0/1"
    slot = 1
    ip_addr = "172.16.0.1"
    subnet_mask = SUBNET_MASK_24

class iosv_2:
  class g0_0:
    name = "GigabitEthernet0/0"
    slot = 0
    ip_addr = "172.16.0.2"
    subnet_mask = SUBNET_MASK_24
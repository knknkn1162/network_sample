SUBNET_MASK_24 = "255.255.255.0"
SUBNET_MASK_32 = "255.255.255.255"
INVERSE_MASK_24 = "0.0.0.255"
pcap_file = "test.pcap"
chap_password = "exampel03942"

class iosv_0:
  class g0_0:
    name = "GigabitEthernet0/0"
    slot = 0
    ip_addr = "192.168.0.254"
    subnet_mask = SUBNET_MASK_24
  class g0_1:
    name = "GigabitEthernet0/1"
    slot = 1
  class dialer1:
    name = "dialer 1"
    pool = 1
    group = 1
  
   
class iosv_1:
  chap_hostname = "router1"
  class g0_0:
    name = "GigabitEthernet0/0"
    slot = 0
    ip_addr = "192.168.1.254"
    subnet_mask = SUBNET_MASK_24
  class g0_1:
    name = "GigabitEthernet0/1"
    slot = 1
    pppoe_group_name = "group01"
  class loopback0:
    name = "loopback 0"
    ip_addr = "10.0.0.254"
    subnet_mask = SUBNET_MASK_32
  class vtemplate1:
    name = "virtual-template 1"
    pool_name = "POOL0"
    from_ip_addr = "10.0.0.1"
    to_ip_addr = "10.0.0.100"
      
class server_0:
  class eth0:
    name = "eth0"
    slot = 0
    ip_addr = "192.168.0.1"
    subnet_mask = SUBNET_MASK_24

class server_1:
  class eth0:
    name = "eth0"
    slot = 0
    ip_addr = "192.168.1.1"
    subnet_mask = SUBNET_MASK_24
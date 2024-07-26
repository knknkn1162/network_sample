from ipaddress import ip_interface
SUBNET_MASK_24 = "255.255.255.0"
INVERSE_MASK_24 = "0.0.0.255"
pcap_file = "test.pcap"
vlan1_num = 10
vlan2_num = 20
vlan3_num = 30

class vyos0:
   class br0:
      class eth0:
         vlan_num = vlan1_num
      class eth1:
         vlan_num = vlan2_num
      class eth2:
         vlan_num = vlan1_num
      class eth3:
         vlan_num = vlan3_num

class pc1:
    class eth0:
       ip_addr = ip_interface("192.168.0.1/24")

class pc2:
    class eth0:
       ip_addr = ip_interface("192.168.1.2/24")

class pc3:
    class eth0:
       ip_addr = ip_interface("192.168.0.3/24")

class pc4:
    class eth0:
       ip_addr = ip_interface("192.168.1.4/24")
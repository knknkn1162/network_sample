from ipaddress import ip_interface
pcap_file0 = "test0.pcap"
pcap_file1 = "test1.pcap"
wpa_supplicant_path = "/etc/wpa_supplicant/wpa_supplicant.conf"

class vlan:
   class primary:
      num = 10
      #ip_addr = ip_interface("192.168.1.100/24")
   class isolated:
      num = 101
   class community0:
      num = 102
   class community1:
      num = 103

class iosvl2_0:
   class g0_0:
      name = "GigabitEthernet0/0"
   class g0_1:
      name = "GigabitEthernet0/1"
   class g0_2:
      name = "GigabitEthernet0/2"
   class g0_3:
      name = "GigabitEthernet0/3"
   class g0_4:
      name = "GigabitEthernet1/0"
   class g0_5:
      name = "GigabitEthernet1/1"

class server_0:
   class eth0:
      ip_addr = ip_interface("192.168.0.1/24")

class server_1:
   class eth0:
      ip_addr = ip_interface("192.168.0.2/24")

class server_2:
   class eth0:
      ip_addr = ip_interface("192.168.0.3/24")

class server_3:
   class eth0:
      ip_addr = ip_interface("192.168.0.4/24")

class server_4:
   class eth0:
      ip_addr = ip_interface("192.168.0.5/24")

class server_5:
   class eth0:
      ip_addr = ip_interface("192.168.0.6/24")
from ipaddress import ip_interface
pcap_file0 = "test0.pcap"
pcap_file1 = "test1.pcap"
external_dns_server = "8.8.8.8"
test_domain_name = "example.com"

class sw_0:
   class port0:
      name = "port0"
   class port1:
      name = "port1"
   class port2:
      name = "port2"

class iosv_0:
   class g0_0:
      name = "GigabitEthernet0/0"
      ip_addr = ip_interface("192.168.255.10/24")

class server_0:
   class eth0:
      ip_addr = ip_interface("192.168.255.20/24")

class ubuntu_0:
   class ens2:
      # DHCP
      pass
   class ens3:
      ip_addr = ip_interface("192.168.255.100/24")

class ex_0:
   ip_addr = ip_interface("192.168.255.1")
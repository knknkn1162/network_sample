from ipaddress import ip_interface

pcap_file = "test.pcap"
ospf_process_id = 10
vc_id = 1

class site_a:
   name = "SITE-A"
   rd = "10:10"

class site_b:
   name = "SITE-B"
   rd = "20:20"

class iosv_0:
   class g0_0:
      name = "GigabitEthernet0/0"
      ip_addr = ip_interface("192.168.0.254/24")
      site = site_a
   class g0_1:
      name = "GigabitEthernet0/1"
      ip_addr = ip_interface("192.168.0.254/24")
      site = site_b
   class g0_2:
      name = "GigabitEthernet0/2"
      class sub0:
         num = 1
         ip_addr = ip_interface("192.168.10.1/24")
         site = site_a
      class sub1:
         num = 2
         ip_addr = ip_interface("192.168.10.1/24")
         site = site_b

class iosv_1:
   class g0_0:
      name = "GigabitEthernet0/0"
      ip_addr = ip_interface("192.168.1.254/24")
      site = site_a
   class g0_1:
      name = "GigabitEthernet0/1"
      ip_addr = ip_interface("192.168.1.254/24")
      site = site_b
   class g0_2:
      name = "GigabitEthernet0/2"
      class sub0:
         num = 1
         ip_addr = ip_interface("192.168.10.2/24")
         site = site_a
      class sub1:
         num = 2
         ip_addr = ip_interface("192.168.10.2/24")
         site = site_b

class server_0:
    class eth0:
      ip_addr = ip_interface("192.168.0.1/24")

class server_1:
    class eth0:
      ip_addr = ip_interface("192.168.0.2/24")

class server_2:
    class eth0:
      ip_addr = ip_interface("192.168.1.1/24")

class server_3:
    class eth0:
      ip_addr = ip_interface("192.168.1.2/24")

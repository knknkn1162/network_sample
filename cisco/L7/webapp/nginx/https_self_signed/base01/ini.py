from ipaddress import ip_interface
pcap_file0 = "test0.pcap"
pcap_file1 = "test1.pcap"

class cert:
   country = "JP"
   state = "Tokyo"
   organization = "Example Company"
   organization_unit = "Example OU"
   common_name = "cconscons.net"
   email = f"test@{common_name}"
   cert_dir = "/etc/ssl/private"

class nginx:
   conf_file = "sample.conf"
   server_name = cert.common_name
   root_dir = "/www/dir"
   index_file = "index.html"

class ubuntu_0:
   class ens2:
      # DHCP
      pass
   class ens3:
      ip_addr = ip_interface("192.168.1.1/24")

class ex_0:
   ip_addr = ip_interface("192.168.255.1")
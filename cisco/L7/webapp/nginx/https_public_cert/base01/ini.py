from ipaddress import ip_interface
import os
pcap_file0 = "test0.pcap"
pcap_file1 = "test1.pcap"

class cert:
   domain_name = "cconscons.net"
   # use certbot
   src_dir = f"{os.getcwd()}/../certs/etc/live/{domain_name}"
   dst_dir = "/etc/ssl/private"

class nginx:
   conf_file = "sample.conf"
   subdomain="test01"
   server_name = f"{subdomain}.{cert.domain_name}"
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
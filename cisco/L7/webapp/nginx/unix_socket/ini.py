from ipaddress import ip_interface
pcap_file0 = "test0.pcap"
pcap_file1 = "test1.pcap"

resp_message = "<p>webapp ok</p>"

class nginx:
   conf_file = "sample.conf"
   socket_file = "/var/run/unix.sock"

class ubuntu_0:
   class ens2:
      # DHCP
      pass
   class ens3:
      ip_addr = ip_interface("192.168.1.1/24")

class ex_0:
   ip_addr = ip_interface("192.168.255.1")
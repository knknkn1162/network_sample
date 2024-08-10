from ipaddress import ip_interface
pcap_file0 = "test0.pcap"
pcap_file1 = "test1.pcap"

class ldap:
   url = "ldapi:///"
   class admin:
      name = "admin"
      domain_unit_names = ["example01", "com"]
      domain_name = ".".join(domain_unit_names)
      tmp_password = "pass01"
      password = "_uU89BhcsbdA"
      dn = f"cn={name},dc={domain_unit_names[0]},dc={domain_unit_names[1]}"
      organization = "myorg"
   class config:
      password = "_uU89BhcsbdB"
      dn = "cn=admin,cn=config"

class sw_0:
   class port0:
      name = "port0"
   class port1:
      name = "port1"
   class port2:
      name = "port2"

class ubuntu_0:
   class ens2:
      # DHCP
      pass
   class ens3:
      ip_addr = ip_interface("192.168.1.100/24")

class ubuntu_1:
   class ens2:
      # DHCP
      pass
   class eth3:
      ip_addr = ip_interface("192.168.1.101/24")


class ex_0:
   ip_addr = ip_interface("192.168.255.1")

class ex_1:
   ip_addr = ip_interface("192.168.255.1")
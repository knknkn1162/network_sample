from ipaddress import ip_interface

class r1:
   class vt1:
      name = "Virtual-Template1"
      ip_addr = ip_interface("192.168.1.1/24")
   class s2_0:
      name = "Serial 2/0"
      dlci_num = 102

class r2:
   class vt1:
      name = "Virtual-Template1"
      ip_addr = ip_interface("192.168.1.2/24")
   class s2_0:
      name = "Serial 2/0"
      dlci_num = 201
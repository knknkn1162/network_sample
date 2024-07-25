SUBNET_MASK_24 = "255.255.255.0"
INVERSE_MASK_24 = "0.0.0.255"
pcap_file = "test.pcap"
from typing import Self

class Dlci:
  def __init__(self, port: int, dlci: int):
    self.port = port
    self.dlci = dlci

dlci0 = Dlci(0, 102)
dlci1 = Dlci(0, 103)
dlci2 = Dlci(1, 201)
dlci3 = Dlci(2, 301)

r1_ip_addr = "10.0.0.1"
r2_ip_addr = "10.0.0.2"
r3_ip_addr = "10.0.0.3"

class r1:
  class f0_0:
    name = "FastEthernet0/0"
    ip_addr = "192.168.1.254"
    subnet_mask = SUBNET_MASK_24
  class s1_0:
    name = "Serial 1/0"
    ip_addr = r1_ip_addr
    subnet_mask = SUBNET_MASK_24


class r2:
  class f0_0:
    name = "FastEthernet0/0"
    ip_addr = "192.168.2.254"
    subnet_mask = SUBNET_MASK_24
  class s1_0:
    name = "Serial 1/0"
    ip_addr = r2_ip_addr
    subnet_mask = SUBNET_MASK_24


class r3:
  class f0_0:
    name = "FastEthernet0/0"
    ip_addr = "192.168.3.254"
    subnet_mask = SUBNET_MASK_24
  class s1_0:
    name = "Serial 1/0"
    ip_addr = r3_ip_addr
    subnet_mask = SUBNET_MASK_24


class pc1:
    class eth0:
      ip_addr = "192.168.1.1"
      subnet_mask = SUBNET_MASK_24
class pc2:
    class eth0:
      ip_addr = "192.168.2.2"
      subnet_mask = SUBNET_MASK_24
class pc3:
    class eth0:
      ip_addr = "192.168.3.3"
      subnet_mask = SUBNET_MASK_24
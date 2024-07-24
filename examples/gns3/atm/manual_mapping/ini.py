SUBNET_MASK_24 = "255.255.255.0"
INVERSE_MASK_24 = "0.0.0.255"
pcap_file = "test.pcap"
from typing import Self

class Pvc:
  def __init__(self, port: int, vpi: int, vci: int):
    self.port = port
    self.vpi = vpi
    self.vci = vci

  def get_vpi_vci(self)-> str:
    return f"{self.vpi}/{self.vci}"

  @classmethod
  def set_peer(pvc1: Self, pvc2: Self):
    pvc1.peer_pvc = pvc2
    pvc2.peer_pvc = pvc1


pvc0 = Pvc(1,1,10)
pvc1 = Pvc(1,2,20)
pvc2 = Pvc(2,3,10)
pvc3 = Pvc(3,4,20)

r1_ip_addr = "10.0.0.1"
r2_ip_addr = "10.0.0.2"
r3_ip_addr = "10.0.0.3"

class r1:
  class f0_0:
    name = "FastEthernet0/0"
    ip_addr = "192.168.1.254"
    subnet_mask = SUBNET_MASK_24
  class a1_0:
    name = "Atm1/0"
    ip_addr = r1_ip_addr
    subnet_mask = SUBNET_MASK_24
    class pvc0:
      pvc = pvc0
      peer_ip = r2_ip_addr
      subnet_mask = SUBNET_MASK_24
    class pvc1:
      pvc = pvc1
      peer_ip = r3_ip_addr
      subnet_mask = SUBNET_MASK_24


class r2:
  class f0_0:
    name = "FastEthernet0/0"
    ip_addr = "192.168.2.254"
    subnet_mask = SUBNET_MASK_24
  class a1_0:
    name = "Atm1/0"
    ip_addr = r2_ip_addr
    subnet_mask = SUBNET_MASK_24
    class pvc0:
      pvc = pvc2
      peer_ip = r1_ip_addr
      subnet_mask = SUBNET_MASK_24


class r3:
  class f0_0:
    name = "FastEthernet0/0"
    ip_addr = "192.168.3.254"
    subnet_mask = SUBNET_MASK_24
  class a1_0:
    name = "Atm1/0"
    ip_addr = r3_ip_addr
    subnet_mask = SUBNET_MASK_24
    class pvc0:
      pvc = pvc3
      peer_ip = r1_ip_addr
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
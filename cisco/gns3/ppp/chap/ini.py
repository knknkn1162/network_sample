SUBNET_MASK_24 = "255.255.255.0"
INVERSE_MASK_24 = "0.0.0.255"
chap_password = "example109324"

class r1:
  username = "r1chap"
  class g0_0:
    name = "FastEthernet0/0"
    ip_addr = "192.168.0.254"
    subnet_mask = SUBNET_MASK_24
  class s0_0:
    name = "Serial2/0"
    ip_addr = "10.0.0.1"
    subnet_mask = SUBNET_MASK_24

class r2:
  username = "r2chap"
  class g0_0:
    name = "FastEthernet0/0"
    ip_addr = "192.168.1.254"
    subnet_mask = SUBNET_MASK_24
  class s0_0:
    name = "Serial2/0"
    ip_addr = "10.0.0.2"
    subnet_mask = SUBNET_MASK_24



class pc1:
    class eth0:
      ip_addr = "192.168.0.1"
      subnet_mask = SUBNET_MASK_24
class pc2:
    class eth0:
      ip_addr = "192.168.1.1"
      subnet_mask = SUBNET_MASK_24

SUBNET_MASK_24 = "255.255.255.0"
INVERSE_MASK_24 = "0.0.0.255"
pcap_file = "test.pcap"
channel_group=1
ETHERCHANNEL_LACP='lacp'

class iosvl2_0:
  class g0_0:
    name = "GigabitEthernet0/0"
    slot = 0
  class g0_1:
    name = "GigabitEthernet0/1"
    slot = 1

class iosvl2_1:
  class g0_0:
    name = "GigabitEthernet0/0"
    slot = 0
  class g0_1:
    name = "GigabitEthernet0/1"
    slot = 1
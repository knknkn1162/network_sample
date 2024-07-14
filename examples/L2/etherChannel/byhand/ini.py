SUBNET_MASK_24 = "255.255.255.0"
INVERSE_MASK_24 = "0.0.0.255"
pcap01_file = "test01.pcap"
channel_group0 = 1
channel_group1 = 2

class channel0:
   num = 1
   name = "Port-channel1"
class channel1:
   num = 2
   name = "Port-channel2"

class iosvl2_0:
   class g0_0:
      name = "GigabitEthernet0/0"
   class g0_1:
      name = "GigabitEthernet0/1"
   ether_channel = channel0

class iosvl2_1:
   class g0_0:
      name = "GigabitEthernet0/0"
   class g0_1:
      name = "GigabitEthernet0/1"
   ether_channel = channel1
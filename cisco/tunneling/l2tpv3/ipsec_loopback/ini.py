from ipaddress import ip_interface
from typing import Self
import re
SUBNET_MASK_24 = "255.255.255.0"
INVERSE_MASK_24 = "0.0.0.255"
ospf_process_id = 10
vc_id = 1

# ipsec
class ipsec:
   class phase1:
      ipsec_priority = 1
      preshared_key = "key1234"
      dh_group = 2
   class phase2:
      # 拡張ACLの番号を 100 ～ 199、2000 ～ 2699 の範囲で指定する。
      acl_num = 100
      class transform_set:
         crypto_param = "esp-aes"
         sig_param = "esp-sha-hmac"
         label = "IPSEC01"
      class crypto_map:
         label = "CMAP01"
         seq_num = 1


class iosv_0:
   class g0_0:
      name = "GigabitEthernet0/0"
      ip_addr = ip_interface("192.168.1.1/24")
   class g0_1:
      name = "GigabitEthernet0/1"
      ip_addr = ip_interface("192.168.0.254/24")
   class loopback0:
      name = "loopback0"
      ip_addr = ip_interface("10.0.0.1/32")

class iosv_1:
   class g0_0:
      name = "GigabitEthernet0/0"
      ip_addr = ip_interface("192.168.1.2/24")
   class g0_1:
      name = "GigabitEthernet0/1"
      ip_addr = ip_interface("192.168.2.2/24")
   class loopback0:
      name = "loopback0"
      ip_addr = ip_interface("10.0.0.2/32")

class iosv_2:
   class g0_0:
      name = "GigabitEthernet0/0"
      ip_addr = ip_interface("192.168.2.3/24")
   class g0_1:
      name = "GigabitEthernet0/1"
      ip_addr = ip_interface("192.168.0.254/24")
   class loopback0:
      name = "loopback0"
      ip_addr = ip_interface("10.0.0.3/32")

class server_0:
    class eth0:
      ip_addr = ip_interface("192.168.0.1/24")

class server_1:
    class eth0:
      ip_addr = ip_interface("192.168.0.2/24")

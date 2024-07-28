from ipaddress import ip_interface
from typing import Self
import re

pcap01_file = "test01.pcap"
pcap02_file = "test02.pcap"
ospf_process_id = 10
vc_id = 1
pw_class_label = "L2TPv3z"


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
   class dialer0:
      pool_num = 1
      name = "Dialer 0"

class iosv_1:
   bba_group_name01 = "BBA01"
   bba_group_name02 = "BBA01"
   class g0_0:
      name = "GigabitEthernet0/0"
      ip_addr = ip_interface("192.168.1.2/24")
   class g0_1:
      name = "GigabitEthernet0/1"
      ip_addr = ip_interface("192.168.2.2/24")
   class loopback0:
      name = "loopback0"
      ip_addr = ip_interface("10.0.0.20/32")
   class loopback1:
      name = "loopback1"
      ip_addr = ip_interface("10.0.0.21/32")
   class vt1:
      name = "Virtual-Template 1"
      access_name = "Virtual-Access 1.1"
   class vt2:
      name = "Virtual-Template 2"
      access_name = "Virtual-Access 2.1"

class iosv_2:
   class g0_0:
      name = "GigabitEthernet0/0"
      ip_addr = ip_interface("192.168.2.3/24")
   class g0_1:
      name = "GigabitEthernet0/1"
      ip_addr = ip_interface("192.168.3.254/24")
   class loopback0:
      name = "loopback0"
      ip_addr = ip_interface("10.0.0.3/32")
   class dialer0:
      pool_num = 1
      name = "Dialer 0"

class server_0:
    class eth0:
      ip_addr = ip_interface("192.168.0.1/24")

class server_1:
    class eth0:
      # same network segment
      ip_addr = ip_interface("192.168.3.2/24")

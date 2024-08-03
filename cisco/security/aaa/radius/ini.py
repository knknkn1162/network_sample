from ipaddress import ip_interface

class sw_0:
   class port0:
      name = "port 0"

class ex_conn0:
   class port:
     pass
class iosv_0:
   class g0_0:
      name = "GigabitEthernet0/0"
      ip_addr = ip_interface("192.168.0.254/24")
      class radius_auth:
         group_name = "RAD-GROUP"
         server_name = "RADIUS-SERVER01"
         password = "secret02"
   class g0_1:
      name = "GigabitEthernet0/1"
      ip_addr = ip_interface("192.168.1.254/24")
class radius:
   init_password = "testing123"
   key = "secret01"
   user_id = "alice"
   password = "password01"

class ubuntu_0:
    class ens2:
       pass
    class ens3:
      ip_addr = ip_interface("192.168.1.1/24")
class ubuntu_1:
    class ens2:
      ip_addr = ip_interface("192.168.0.1/24")
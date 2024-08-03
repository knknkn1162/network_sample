from genie import testbed
from cmlmag.cml import CONFIG_YAML, Cml
from cmlmag.device import Device
from cmlmag import wait, ipv4
import cmlmag.parse as parse
import cmlmag.wait_until as wait_until
import ini

def main():
  tb = testbed.load(CONFIG_YAML)
  # switch
  iosv_0 = Device(tb, ini.iosv_0.__name__)
  # radius server
  ubuntu_0 = Device(tb, ini.ubuntu_0.__name__)
  ubuntu_1 = Device(tb, ini.ubuntu_1.__name__)
  print("####### exec #######")
  cml = Cml()
  pcap = cml.lab.create_pcap(iosv_0.name, ubuntu_0.name, auth_token=cml.auth_token)

  # server setup
  # setup first
  ubuntu_0.execs([
    f"ip a",
    f"""
sudo apt update && sudo apt install -y freeradius freeradius-utils
    """,
  ])
  ubuntu_1.execs([
    f"ip a",
    f"sudo apt update && sudo apt install -y freeradius-utils",
  ])
  # todo; improve
  wait.seconds(60)

  # up
  iosv_0.execs([
    [
      f"interface {ini.iosv_0.g0_0.name}",
      f"ip addr {ini.iosv_0.g0_0.ip_addr.ip} {ini.iosv_0.g0_0.ip_addr.netmask}",
      f"no shutdown",
    ],
    [
      f"interface {ini.iosv_0.g0_1.name}",
      f"ip addr {ini.iosv_0.g0_1.ip_addr.ip} {ini.iosv_0.g0_1.ip_addr.netmask}",
      f"no shutdown",
    ],
  ])

  # radius server settings
  ubuntu_0.execs([
    f"""
cat <<- EOF | sudo tee /etc/netplan/99-config.yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    {ini.ubuntu_0.ens3.__name__}:
      dhcp4: false
      dhcp6: false
      addresses: [{ini.ubuntu_0.ens3.ip_addr}]
      routes:
        - to: default
          via: {ini.iosv_0.g0_1.ip_addr.ip}
EOF
"""])
  wait.seconds(2)
  ubuntu_0.execs([
    f"sudo chmod 600 /etc/netplan/99-config.yaml",
    f"sudo netplan apply",
  ])
    
  wait.seconds(2)
  ubuntu_0.execs([
    f"ip a",
    f"ip route",
  ])

  ## ip settings
  ubuntu_1.execs([
    f"""
cat <<- EOF | sudo tee /etc/netplan/99-config.yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    {ini.ubuntu_1.ens3.__name__}:
      dhcp4: false
      dhcp6: false
      addresses: [{ini.ubuntu_1.ens3.ip_addr}]
      routes:
        - to: default
          via: {ini.iosv_0.g0_0.ip_addr.ip}
EOF
"""])
  wait.seconds(2)
  ubuntu_1.execs([
    f"sudo chmod 600 /etc/netplan/99-config.yaml",
    f"sudo netplan apply",
  ])
  wait.seconds(2)
  ubuntu_1.execs([
    f"ip a",
    f"ip route",
  ])


  # radius server settings
  ubuntu_0.execs([
    f"""
cat <<- EOF | sudo tee -a /etc/freeradius/3.0/clients.conf
client iosv_0 {{
  ipaddr = {ini.iosv_0.g0_1.ip_addr}
  secret = {ini.iosv_0.g0_1.radius_auth.key}
}}
client ubuntu_1 {{
  ipaddr = {ini.ubuntu_1.ens3.ip_addr}
  secret = {ini.ubuntu_1.ens3.radius_auth.key}
}}
EOF
"""
  ])

  wait.seconds(2)
  ubuntu_0.execs([
    f"""
cat <<- EOF | sudo tee -a /etc/freeradius/3.0/users
{ini.radius.user_id}    Cleartext-Password := "{ini.radius.password}"
       Reply-Message := "Hello, %{{User-Name}}"
EOF
"""
  ])

  wait.seconds(2)
  ubuntu_0.execs([
    f"sudo service freeradius restart",
    #f"sudo freeradius -CX",
  ])

  wait.seconds(10)
  ubuntu_0.execs([
    f"radtest {ini.radius.user_id} {ini.radius.password} localhost 0 {ini.radius.init_password}",
    f"journalctl -u freeradius | tee /dev/null"
  ])
  ubuntu_1.execs([
    f"radtest {ini.radius.user_id} {ini.radius.password} {ini.ubuntu_0.ens3.ip_addr.ip} 0 {ini.ubuntu_1.ens3.radius_auth.key}",
  ])

  # radius client settings
  iosv_0.execs([
    # register radius server
    [
      f"aaa new-model",
      f"radius server {ini.iosv_0.g0_1.radius_auth.server_name}",
      f"address ipv4 {ini.ubuntu_0.ens3.ip_addr.ip} auth-port {ini.radius.auth_port} acct-port {ini.radius.acc_port}",
      f"key {ini.iosv_0.g0_1.radius_auth.key}",
    ],
    # associate group
    [
      f"aaa group server radius {ini.iosv_0.g0_1.radius_auth.group_name}",
      f"server name {ini.iosv_0.g0_1.radius_auth.server_name}",
    ],
    # AAA settings
    # see https://www.infraexpert.com/study/aaaz08.html
    [
      # IEEE802.1X認証をグローバルで有効化
      #f"dot1x system-auth-control",
      # Authentication
      f"aaa authentication login default group {ini.iosv_0.g0_1.radius_auth.group_name}",
      #f"aaa authentication dot1x default group {ini.iosv_0.g0_1.radius_auth.group_name}",
      # Authorization
      f"aaa authorization exec default group {ini.iosv_0.g0_1.radius_auth.group_name}",
      f"aaa authorization network default group {ini.iosv_0.g0_1.radius_auth.group_name}",
      ## コンソール認可の有効化
      f"aaa authorization console",
      # Accounting
      #f"aaa accounting dot1x default start-stop group {ini.iosv_0.g0_1.radius_auth.group_name}",
      f"aaa accounting system default start-stop group {ini.iosv_0.g0_1.radius_auth.group_name}",
    ],
    # RADIUSクライアントとRADIUSサーバが通信できない状態になった時、ローカルで
    # 設定したデータベースを使用して認証、認可するように設定
    [
      f"username admin privilege 15 secret {ini.iosv_0.g0_1.radius_auth.password}"
    ],
  ])

  # telnet settings to test
  iosv_0.execs([
    [
      f"line vty 0 4",
      f"transport input telnet",
    ]
  ])

  ### CHECK
  iosv_0.execs([
    f"test aaa group radius {ini.radius.user_id} {ini.radius.password} new-code"
  ])
  pcap.start(maxpackets=100)
  # telnet test
  ubuntu_1.check_server_telnet(ini.iosv_0.g0_0.ip_addr.ip, username = ini.radius.user_id, password = ini.radius.password)
  pcap.download(file=ini.pcap_file)

if __name__ == '__main__':
  main()
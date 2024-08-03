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
  iosvl2_0 = Device(tb, ini.iosvl2_0.__name__)
  # radius server
  ubuntu_0 = Device(tb, ini.ubuntu_0.__name__)
  ubuntu_1 = Device(tb, ini.ubuntu_1.__name__)

  server_0 = Device(tb, ini.server_0.__name__)
  print("####### exec #######")
  cml = Cml()
  pcap = cml.lab.create_pcap(iosvl2_0.name, ubuntu_0.name, auth_token=cml.auth_token)

  # server install package
  # setup first
  ubuntu_0.execs([
    f"ip a",
    f"""
sudo apt update && sudo apt install -y freeradius freeradius-utils
    """,
  ])
  ubuntu_1.execs([
    f"ip a",
    f"sudo apt update && sudo apt install -y wpasupplicant",
  ])
  # todo; improve
  wait.seconds(60)

  # up
  # server setup
  server_0.execs([
    # eth0 setting
    ## disable DHCP
    f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
    f"sudo ifconfig eth0 {ini.server_0.eth0.ip_addr.ip} netmask {ini.server_0.eth0.ip_addr.netmask} up",
    # set default gw to virtual address of glbp
    f"ifconfig eth0",
  ])

  iosvl2_0.execs([
    [
      f"interface vlan {ini.iosvl2_0.vlan.num}",
      f"ip addr {ini.iosvl2_0.vlan.ip_addr.ip} {ini.iosvl2_0.vlan.ip_addr.netmask}"
    ],
    [
      f"interface {ini.iosvl2_0.g0_0.name}",
      f"switchport access vlan {ini.iosvl2_0.vlan.num}",
      f"switchport mode access",
    ],
    [
      f"interface {ini.iosvl2_0.g0_1.name}",
      f"no switchport",
      f"ip addr {ini.iosvl2_0.g0_1.ip_addr.ip} {ini.iosvl2_0.g0_1.ip_addr.netmask}",
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
          via: {ini.iosvl2_0.g0_1.ip_addr.ip}
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
          via: {ini.iosvl2_0.vlan.ip_addr.ip}
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
client iosvl2_0 {{
  ipaddr = {ini.iosvl2_0.g0_1.ip_addr}
  secret = {ini.iosvl2_0.g0_1.radius_auth.key}
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

  # radius authenticator settings
  ## aaa
  iosvl2_0.execs([
    # register radius server
    [
      f"aaa new-model",
      f"radius server {ini.iosvl2_0.g0_1.radius_auth.server_name}",
      f"address ipv4 {ini.ubuntu_0.ens3.ip_addr.ip} auth-port {ini.radius.auth_port} acct-port {ini.radius.acc_port}",
      f"key {ini.iosvl2_0.g0_1.radius_auth.key}",
    ],
    # associate group
    [
      f"aaa group server radius {ini.iosvl2_0.g0_1.radius_auth.group_name}",
      f"server name {ini.iosvl2_0.g0_1.radius_auth.server_name}",
    ],
    # AAA settings
    # see https://www.infraexpert.com/study/aaaz08.html
    [
      # IEEE802.1X認証をグローバルで有効化
      f"dot1x system-auth-control",
      # Authentication
      f"aaa authentication login default group {ini.iosvl2_0.g0_1.radius_auth.group_name}",
      f"aaa authentication dot1x default group {ini.iosvl2_0.g0_1.radius_auth.group_name}",
      # Authorization
      f"aaa authorization exec default group {ini.iosvl2_0.g0_1.radius_auth.group_name}",
      f"aaa authorization network default group {ini.iosvl2_0.g0_1.radius_auth.group_name}",
      ## コンソール認可の有効化
      f"aaa authorization console",
      # Accounting
      f"aaa accounting dot1x default start-stop group {ini.iosvl2_0.g0_1.radius_auth.group_name}",
      f"aaa accounting system default start-stop group {ini.iosvl2_0.g0_1.radius_auth.group_name}",
    ],
    # RADIUSクライアントとRADIUSサーバが通信できない状態になった時、ローカルで
    # 設定したデータベースを使用して認証、認可するように設定
    [
      f"username admin privilege 15 secret {ini.iosvl2_0.g0_1.radius_auth.password}"
    ],
  ])
  ## dot1x interface setting
  iosvl2_0.execs([
    [
      f"interface {ini.iosvl2_0.g0_0.name}",
      # IEEE802.1X認証をポートで有効化
      f"authentication port-control auto",
      # IEEE802.1X port access entity (PAE) authenticatorとしてのみ動作する設定
      f"dot1x pae authenticator",
    ]
  ])

  ## telnet settings to test
  iosvl2_0.execs([
    [
      f"line vty 0 4",
      f"transport input telnet",
    ]
  ])

  # radius supplicant settings
  ## dot1x settings
  ubuntu_1.execs([
    # see https://help.ubuntu.com/community/Network802.1xAuthentication
    f"""
cat <<- EOF | sudo tee -a /etc/wpa_supplicant/wpa_supplicant.conf
# Where is the control interface located? This is the default path:
ctrl_interface=/var/run/wpa_supplicant

# Who can use the WPA frontend? Replace "0" with a group name if you
#   want other users besides root to control it.
# There should be no need to chance this value for a basic configuration:
ctrl_interface_group=0

# IEEE 802.1X works with EAPOL version 2, but the version is defaults 
#   to 1 because of compatibility problems with a number of wireless
#   access points. So we explicitly set it to version 2:
eapol_version=2
# EAP: PPP Extensible Authentication Protocol (See https://www.infraexpert.com/study/wireless51.html)
network={{
        key_mgmt=IEEE8021X
        eap=MD5
        identity="{ini.radius.user_id}"
        anonymous_identity="{ini.radius.user_id}"
        password="{ini.radius.password}"
        phase1="auth=MD5"
        phase2="auth=PAP password={ini.radius.user_id}"
        eapol_flags=0
}}
EOF
"""
  ])

  wait.seconds(4)
  ubuntu_1.execs([
    f"sudo wpa_supplicant -c /etc/wpa_supplicant/wpa_supplicant.conf -D wired -i {ini.ubuntu_1.ens3.__name__}"
  ])

  ### CHECK
  iosvl2_0.execs([
    f"show dot1x interface {ini.iosvl2_0.g0_0.name}",
  ])

  ubuntu_1.server_ping(ini.server_0.eth0.ip_addr.ip)

  # iosvl2_0.execs([
  #   f"test aaa group radius {ini.radius.user_id} {ini.radius.password} new-code"
  # ])
  # pcap.start(maxpackets=100)
  # # telnet test
  # ubuntu_1.check_server_telnet(ini.iosvl2_0.g0_0.ip_addr.ip, username = ini.radius.user_id, password = ini.radius.password)
  # pcap.download(file=ini.pcap_file)

if __name__ == '__main__':
  main()
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
  pcap_supp = cml.lab.create_pcap(iosvl2_0.name, ubuntu_1.name, auth_token=cml.auth_token)
  pcap_authe = cml.lab.create_pcap(iosvl2_0.name, ubuntu_0.name, auth_token=cml.auth_token)


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
    f"sudo route add default gw {ini.iosvl2_0.g0_2.ip_addr.ip}",
    f"ifconfig eth0",
    f"route -e",
  ])

  iosvl2_0.execs([
    [
      f"interface vlan {ini.iosvl2_0.vlan.num}",
      f"ip addr {ini.iosvl2_0.vlan.ip_addr.ip} {ini.iosvl2_0.vlan.ip_addr.netmask}",
      f"no shutdown",
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
    [
      f"interface {ini.iosvl2_0.g0_2.name}",
      f"no switchport",
      f"ip addr {ini.iosvl2_0.g0_2.ip_addr.ip} {ini.iosvl2_0.g0_2.ip_addr.netmask}",
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

  iosvl2_0.execs([
    f"show dot1x interface {ini.iosvl2_0.g0_0.name}",
  ])

  # radius supplicant settings
  ## dot1x settings
  ubuntu_1.execs([
    # see https://help.ubuntu.com/community/Network802.1xAuthentication
    f"""
cat <<- EOF | sudo tee -a {ini.wpa_supplicant_path}
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

# When configuring WPA-Supplicant for use on a wired network, we don’t need to
#   scan for wireless access points. See the wpa-supplicant documentation if
#   you are authenticating through 802.1x on a wireless network:
ap_scan=0
# EAP: PPP Extensible Authentication Protocol (See https://www.infraexpert.com/study/wireless51.html)
network={{
        key_mgmt=IEEE8021X
        eap=PEAP
        identity="{ini.radius.user_id}"
        password="{ini.radius.password}"
        eapol_flags=0
}}
EOF
"""
  ])

  wait.seconds(4)
  pcap_supp.start(maxpackets=200)
  pcap_authe.start(maxpackets=200)
  ubuntu_1.server_ping(ini.server_0.eth0.ip_addr.ip)

  # authe dot1x
  ubuntu_1.execs([
    # -dd: verbose
    f"nohup sudo wpa_supplicant -dd -c {ini.wpa_supplicant_path} -D wired -i {ini.ubuntu_1.ens3.__name__} 2> /dev/null &",
  ])

  ### CHECK

  def populate_server_ping(device: Device, target_ip: str, count=5):
    @wait.retry(count=30, result=0, sleep_time=3)
    def _do(device: Device):
      return device.server_ping(target_ip, count)
    return _do(device)
  
  populate_server_ping(ubuntu_1, ini.server_0.eth0.ip_addr.ip)
  pcap_supp.download(ini.pcap_file0)
  pcap_authe.download(ini.pcap_file1)

  ubuntu_1.execs([
    f"cat nohup.out",
  ])

if __name__ == '__main__':
  main()
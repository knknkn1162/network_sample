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
  ubuntu_0 = Device(tb, ini.ubuntu_0.__name__)
  server_0 = Device(tb, ini.server_0.__name__)
  iosv_0 = Device(tb, ini.iosv_0.__name__)


  print("####### exec #######")
  cml = Cml()
  #pcap = cml.lab.create_pcap(iosvl2_0.name, server_0.name, auth_token=cml.auth_token)

  # install
  ubuntu_0.execs([
    f"sudo apt update && sudo apt install -y bind9 bind9utils",
  ])
  wait.seconds(60)

  ubuntu_0.execs([
    f"systemctl check named",
  ])

  # address settings
  server_0.execs([
    # eth0 setting
    ## disable DHCP
    f"[ -f /var/run/udhcpc.eth0.pid ] && sudo kill `cat /var/run/udhcpc.eth0.pid`",
    f"sudo ifconfig eth0 {ini.server_0.eth0.ip_addr.ip} netmask {ini.server_0.eth0.ip_addr.netmask} up",
    f"sudo route add default gw {ini.ex_0.ip_addr.ip}",
    f"ifconfig eth0",
    f"route -e",
    f"""
    echo "nameserver {ini.ubuntu_0.ens3.ip_addr.ip}" > /etc/resolv.conf
    """,
  ])

  iosv_0.execs([
    [
      f"interface {ini.iosv_0.g0_0.name}",
      f"ip addr {ini.iosv_0.g0_0.ip_addr.ip} {ini.iosv_0.g0_0.ip_addr.netmask}",
      f"no shutdown",
    ],
    [
      f"ip domain lookup",
      f"ip name-server {ini.ubuntu_0.ens3.ip_addr.ip}",
      f"ip route 0.0.0.0 0.0.0.0 {ini.ex_0.ip_addr.ip}",
    ]
  ])

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
EOF
"""])
  wait.seconds(2)
  ubuntu_0.execs([
    f"sudo chmod 600 /etc/netplan/99-config.yaml",
    f"sudo netplan apply",
  ])

  # forwarder settings
  ubuntu_0.execs([
    # spaces
    f'''cat << EOF | sudo tee /etc/bind/named.conf.options
options {{
  directory "/var/cache/bind";

  forwarders {{
    {ini.external_dns_server}; // forwarding public DNS server
  }};

  recursion yes; // set as resolver

  dnssec-validation auto;

  listen-on-v6 {{ any; }};
}};
EOF
'''
  ])


  wait.seconds(2)
  ubuntu_0.execs([
    f"sudo systemctl restart named",
  ])
  wait.seconds(4)
  ubuntu_0.execs([
    f"systemctl check named",
    f"journalctl -u named | tee /dev/null",
  ])
  
  ubuntu_0.execs([
    f"nslookup {ini.test_domain_name}",
  ])

  # it doesn't work
  ubuntu_0.server_ping(ini.test_domain_name)
  iosv_0.router_ping(ini.test_domain_name)

if __name__ == '__main__':
  main()
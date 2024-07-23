from genie import testbed
from cmlmag.cml import CONFIG_YAML, Cml
from cmlmag.device import Device
from cmlmag import wait, ipv4
import cmlmag.parse as parse
import cmlmag.wait_until as wait_until
import ini
from cmlmag.structure.stp_info import (
  Role as StpRole,
  State as StpState
)

def main():
  tb = testbed.load(CONFIG_YAML)
  # ubuntu
  # client
  ubuntu_0 = Device(tb, ini.ubuntu_0.__name__)
  # server
  ubuntu_1 = Device(tb, ini.ubuntu_1.__name__)

  print("####### exec #######")
  cml = Cml()

  # setup first
  ubuntu_1.execs([
    f"sudo apt-get update",
    f"sudo apt-get update -y apache2",
  ])

  cml.lab.remove_link_by_nodes(ini.ubuntu_1.__name__, ini.ext_conn0.__name__)

  # conf static ip
  ubuntu_0.execs([
    f"""
cat <<- EOF | sudo tee /etc/netplan/99-config.yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    {ini.ubuntu_0.ens2.__name__}:
      dhcp4: false
      dhcp6: false
      addresses: [{ini.ubuntu_0.ens2.ip_addr}/{ini.ubuntu_0.ens2.prefix_len}]
      routes:
        - to: default
          via: {ini.ubuntu_0.ens2.default_gw}
EOF
    """,
    f"sudo chmod 600 /etc/netplan/99-config.yaml",
    f"sudo netplan apply",
  ])

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
      addresses: [{ini.ubuntu_1.ens3.ip_addr}/{ini.ubuntu_1.ens3.prefix_len}]
      routes:
        - to: default
          via: {ini.ubuntu_1.ens3.default_gw}
EOF
    """,
    f"sudo chmod 600 /etc/netplan/99-config.yaml",
    f"sudo netplan apply",
  ])


  wait_until.seconds(5)
  res = ubuntu_0.execs([
    f"curl http://{ini.ubuntu_1.ens3.ip_addr}",
    f"echo $?",
  ])
  assert res == 0

if __name__ == '__main__':
  main()
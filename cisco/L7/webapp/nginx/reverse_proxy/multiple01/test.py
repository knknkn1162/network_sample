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
  ubuntu_1 = Device(tb, ini.ubuntu_1.__name__)
  ubuntu_2 = Device(tb, ini.ubuntu_2.__name__)

  ubuntu_0.server_execs(waits=0, cmds=[[
    f"""
    sudo apt update && \
      sudo apt install -y nginx && \
      sudo rm -rf /etc/nginx/sites-enabled/default
    """,
  ]])

  ubuntu_1.server_execs(waits=0, cmds=[[
    f"""
    sudo apt update && \
      sudo apt install -y nginx && \
      sudo rm -rf /etc/nginx/sites-enabled/default
    """,
  ]])
  wait.seconds(60)

  # ip settings
  ubuntu_0.server_execs(cmds=[
    [
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
        """,
    ],
    [
      f"sudo chmod 600 /etc/netplan/99-config.yaml",
      f"sudo netplan apply",
    ]
  ])

  ubuntu_1.server_execs(cmds=[
    [
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
EOF
        """,
    ],
    [
      f"sudo chmod 600 /etc/netplan/99-config.yaml",
      f"sudo netplan apply",
    ]
  ])

  ubuntu_2.server_execs(cmds=[
    [
      f"""
cat <<- EOF | sudo tee /etc/netplan/99-config.yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    {ini.ubuntu_2.ens2.__name__}:
      dhcp4: false
      dhcp6: false
      addresses: [{ini.ubuntu_2.ens2.ip_addr}]
EOF
        """,
    ],
    [
      f"sudo chmod 600 /etc/netplan/99-config.yaml",
      f"sudo netplan apply",
    ]
  ])

  # configure nginx
  ubuntu_0.server_execs(cmds=[
    [
      f"""cat <<EOF | sudo tee /etc/nginx/conf.d/{ini.nginx.conf_file}
# proxy for unix socket
error_log {ini.nginx.error_log} debug;
server {{
  listen 80;
  server_name {ini.ubuntu_0.ens3.ip_addr.ip};
  location / {{
    proxy_pass http://{ini.ubuntu_1.ens3.ip_addr.ip};
    proxy_set_header Host                   \$host;
    proxy_set_header X-Forwarded-Host       \$host;
    # the most safe way will be to set both according to an actual remote peer address:
    proxy_set_header X-Real-IP              \$remote_addr;
    proxy_set_header X-Forwarded-For        \$remote_addr;
  }}
}}
# catch all
server {{
  listen 80 default_server;
  server_name _;
  return 404;
}}
EOF
"""
    ],
    [
      f"sudo systemctl reload nginx",
    ],
    [
      f"systemctl check nginx",
    ]
  ])

  ubuntu_1.server_execs(cmds=[
    [
      f"""cat <<EOF | sudo tee /etc/nginx/conf.d/{ini.nginx.conf_file}
# proxy for unix socket
error_log {ini.nginx.error_log} debug;
server {{
  listen 80;
  server_name {ini.ubuntu_1.ens3.ip_addr.ip};
  set_real_ip_from {ini.ubuntu_0.ens3.ip_addr.ip};
  # get client IP address via XFF
  real_ip_header    X-Forwarded-For;
  # バックエンドには複数プロキシを経由してリクエストが到達する場合に必要
  # real_ip_recursive on;
}}
# catch all
server {{
  listen 80 default_server;
  server_name _;
  return 404;
}}
EOF
"""
    ],
    [
      f"sudo systemctl reload nginx",
    ],
    [
      f"systemctl check nginx",
    ]
  ])

  # check
  ubuntu_2.server_execs(cmds=[
    [
      # should appear welcome page
      f"curl -vvv http://{ini.ubuntu_0.ens3.ip_addr.ip}",
      f"cat {ini.nginx.error_log}",
    ],
  ])


  for serv in [ubuntu_0, ubuntu_1]:
    serv.server_execs(cmds=[
      [
        f"cat {ini.nginx.error_log}",
      ],
    ])

if __name__ == '__main__':
  main()
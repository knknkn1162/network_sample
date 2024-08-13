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
  #ubuntu_1 = Device(tb, ini.ubuntu_1.__name__)

  ubuntu_0.server_execs(waits=60, cmds=[[
    """
      sudo apt update && \
        sudo apt install -y nginx openssl && \
        sudo rm -rf /etc/nginx/sites-enabled/default
    """,
  ]])

  # get cert and priv
  with open(f"{ini.cert.src_dir}/privkey.pem") as f:
    data = f.read()
    ubuntu_0.server_execs(cmds=[
      [
        f"""cat <<EOF | sudo tee {ini.cert.dst_dir}/server.key
{data.strip()}
EOF
        """
      ]
    ])
  with open(f"{ini.cert.src_dir}/fullchain.pem") as f:
    data = f.read()
    ubuntu_0.server_execs(cmds=[
      [
        f"""cat <<EOF | sudo tee {ini.cert.dst_dir}/server.crt
{data.strip()}
EOF
        """
      ]
    ])
  

  ubuntu_0.server_execs(cmds=[
    [
      f"""cat <<EOF | sudo tee /etc/nginx/conf.d/{ini.nginx.conf_file}
server {{
  listen 443 ssl default_server;
  server_name {ini.nginx.server_name};
  ssl_certificate {ini.cert.dst_dir}/server.crt;
  ssl_certificate_key {ini.cert.dst_dir}/server.key;
  root {ini.nginx.root_dir};
}}

# catch all
server {{
  listen 80 default_server;
  server_name _;
  # Always On SSL/TLS
  return 301 https://\$host\$request_uri;
}}
EOF
      """,
    ],
    [
      f"sudo mkdir -p {ini.nginx.root_dir}",
      f"sudo chmod -R 755 {ini.nginx.root_dir}",
      f"""cat <<EOF | sudo tee {ini.nginx.root_dir}/{ini.nginx.index_file}
<html><body><h1>Hello world!!</h1></body></html>
EOF
      """,
    ],
    [
      f"sudo systemctl reload nginx",
    ],
    [
      f"journalctl -u nginx | tee /dev/null",
    ]
  ])

  wait.seconds(5)
  # check
  ubuntu_0.server_execs(cmds=[
    [
      # curl: (60) SSL: no alternative certificate subject name matches target host name '127.0.0.1'
      # More details here: https://curl.se/docs/sslcerts.html
      f"curl -vvv https://127.0.0.1",
      # -k = --insecure
      f"curl -vvv -k https://127.0.0.1",
      # resolve by curl; it should work
      f"curl -vvv --resolve {ini.nginx.server_name}:443:127.0.0.1 https://{ini.nginx.server_name}",
      f"echo 'Q' | openssl s_client -connect 127.0.0.1:443",
    ],
  ])

if __name__ == '__main__':
  main()
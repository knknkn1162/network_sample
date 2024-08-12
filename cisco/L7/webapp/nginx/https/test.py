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

  # create privkey and self-signed
  ubuntu_0.server_execs(cmds=[
    [
      # generate signkey(priv key)
      f"openssl genrsa -out server.key 4096",
      # generate CSR
      f"""
      openssl req -new \
        -key server.key \
        -subj '/C={ini.cert.country}/ST={ini.cert.state}/O={ini.cert.organization}/OU={ini.cert.organization_unit}/CN={ini.cert.common_name}/emailAddress={ini.cert.email}' \
        -out server.csr
      """,
      # self-signed certificate: server.crt"
      # -extfile: SAN: 証明書のサブジェクト代替名 (subjectAltName; SAN) にIPアドレスを追加することで、証明書の検証が成功する
      # 最近のブラウザでは、CNではなくSANを使うことが推奨
      f"""
      openssl x509 -req -days 365 -signkey server.key \
        -in server.csr \
        -out server.crt \
        -extfile - <<EOF
subjectAltName = DNS:{ini.cert.common_name}, IP:127.0.0.1
EOF
      """,
    ],
    [
      f"sudo cp server.crt server.key {ini.cert.cert_dir}",
      f"sudo chmod 400 {ini.cert.cert_dir}/server.crt",
      # in CA, cat server.crt chain.crt crossrot.crt > fullchain.crt
    ],
  ])

  ubuntu_0.server_execs(cmds=[
    [
      f"""cat <<EOF | sudo tee /etc/nginx/conf.d/{ini.nginx.conf_file}
server {{
  listen 443 ssl default_server;
  server_name {ini.nginx.server_name};
  ssl_certificate {ini.cert.cert_dir}/server.crt;
  ssl_certificate_key {ini.cert.cert_dir}/server.key;
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
      # * SSL certificate problem: self-signed certificate
      # * Closing connection 0
      # curl: (60) SSL certificate problem: self-signed certificate
      f"curl -vvv https://127.0.0.1",
      # -k = --insecure
      f"curl -vvv -k https://127.0.0.1",
      f"curl -vvv --resolve {ini.nginx.server_name}:443:127.0.0.1 https://{ini.nginx.server_name}",
      # check redirect
      f"curl -vvv -L http://127.0.0.1",
      # quit for `echo 'Q'`: https://stackoverflow.com/questions/25760596/how-to-terminate-openssl-s-client-after-connection
      f"echo 'Q' | openssl s_client -connect 127.0.0.1:443 -CAfile ./server.crt -brief",
    ],
  ])

if __name__ == '__main__':
  main()
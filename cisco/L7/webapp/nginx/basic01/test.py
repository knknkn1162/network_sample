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
    "sudo apt update && sudo apt install -y nginx",
  ]])
  ubuntu_0.server_execs(cmds=[
    [
      # # In most cases, administrators will remove this file from sites-enabled/ and
      # leave it as reference inside of sites-available where it will continue to be
      # updated by the nginx packaging team.
      f"sudo rm -rf /etc/nginx/sites-enabled/default",
    ],
    [
      f"""cat <<EOF | sudo tee /etc/nginx/conf.d/{ini.nginx.conf_file}
server {{
  listen 80;
  server_name {ini.nginx.server_name};
  access_log /var/log/nginx/static-access.log;
  error_log /var/log/nginx/static-error.log;

  location / {{
    root {ini.nginx.root_dir};
    index {ini.nginx.index_file};
  }}
}}

# catch all
server {{
  listen 80 default_server;
  server_name _;

  return 404;
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
  ])

  wait.seconds(5)
  # check
  ubuntu_0.server_execs(cmds=[
    [
      # --resolve or --connect-to
      f"curl --resolve {ini.nginx.server_name}:80:127.0.0.1 http://{ini.nginx.server_name}"
      f"curl http://127.0.0.1",
    ],
  ])

if __name__ == '__main__':
  main()
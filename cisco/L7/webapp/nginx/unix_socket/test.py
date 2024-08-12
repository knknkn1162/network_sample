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
    f"""
    sudo apt update && \
      sudo apt install -y nginx socat && \
      sudo rm -rf /etc/nginx/sites-enabled/default
    """,
  ]])

  ubuntu_0.server_execs(cmds=[
    # assume web app using socat
    [
      # exec `sudo socat unix:/var/run/unix.sock -` for client test
      f"""
        sudo socat UNIX-LISTEN:{ini.nginx.socket_file},fork EXEC:'echo -e "HTTP/1.1 200 Ok\n\n{ini.resp_message}"' &
      """,
      f"sudo chmod a+w {ini.nginx.socket_file}",
    ],
    [
      f"""cat <<EOF | sudo tee /etc/nginx/conf.d/{ini.nginx.conf_file}
# proxy for unix socket
server {{
  listen 80;
  server_name localhost;
  location / {{
    proxy_pass http://unix:{ini.nginx.socket_file}:/;
  }}
}}
# This could be OK
# receiver
# server {{
#   listen unix:/{ini.nginx.socket_file};
# }}
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
  ])

  wait.seconds(5)
  # check
  ubuntu_0.server_execs(cmds=[
    [
      f"systemctl check nginx",
    ],
    [
      # should appear welcome page
      f"curl -vvv http://localhost",
    ],
  ])

if __name__ == '__main__':
  main()
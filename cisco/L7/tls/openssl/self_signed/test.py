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

  ubuntu_0.execs([
    "sudo apt update && sudo apt install -y openssl"
  ])
  wait.seconds(60)

  ubuntu_0.execs([
    f"openssl genrsa -aes256 -out server.key -passout pass:{ini.cert.passphrase} 4096",
    # no passphrase",
    f"openssl rsa -in server.key -passin pass:{ini.cert.passphrase} -out nopassphrase.key",
    # generate CSR",
    f"""
    openssl req -new -key server.key -passin pass:{ini.cert.passphrase} \
      -subj '/C={ini.cert.country}/ST={ini.cert.state}/O={ini.cert.organization}/OU={ini.cert.organization_unit}/CN={ini.cert.common_name}/emailAddress={ini.cert.email}' \
      -out server.csr
    """,
    # self-signed certificate: server.crt"
    f"openssl x509 -req -passin pass:{ini.cert.passphrase} -days 365 -signkey server.key -in server.csr -out server.crt",
  ])

  # other
  ubuntu_0.execs([
    # no passphrase",
    f"openssl rsa -in server.key -passin pass:{ini.cert.passphrase} -out nopassphrase.key",
  ])

  # check
  ubuntu_0.execs([
    # check CSR content"
    f"openssl req -text -in server.csr -passin pass:{ini.cert.passphrase} -noout",
    # check CRT(pem): server.crt content",
    f"openssl x509 -in server.crt -noout -text",
    # check by modulus"
    f"openssl x509 -noout -modulus -in server.crt | openssl md5",
    f"openssl rsa -passin pass:{ini.cert.passphrase} -noout -modulus -in server.key | openssl md5",
    # check server.crt using -CAfile",
    f"openssl verify -verbose -CAfile server.crt server.crt",
  ])

  # check server.crt using -CAPath
  ubuntu_0.execs([
    f"mkdir -p cacerts",
    f"cp server.crt ./cacerts",
    f"cd cacerts",
    f"ln -s server.crt `$(openssl x509 -hash -noout -in server.crt).0`",
    f"cd -",
    f"openssl verify -verbose -CApath ./cacerts server.crt",
  ])

if __name__ == '__main__':
  main()
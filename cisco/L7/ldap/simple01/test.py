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

  ubuntu_0.execs([
    "sudo apt update && sudo DEBIAN_FRONTEND=noninteractive apt install -y slapd"
  ])

  wait.seconds(60)

  ubuntu_0.execs([
    f"""cat <<EOF | sudo debconf-set-selections
slapd slapd/internal/adminpw password {ini.ldap.tmp_admin_password}
slapd slapd/internal/generated_adminpw password {ini.ldap.tmp_admin_password}
slapd slapd/password1 password {ini.ldap.tmp_admin_password}
slapd slapd/password2 password {ini.ldap.tmp_admin_password}
slapd slapd/domain string {ini.ldap.domain_name}
slapd shared/organization string {ini.ldap.organization}
EOF
"""
  ])
  wait.seconds(2)
  ubuntu_0.execs([
    f"sudo dpkg-reconfigure -f noninteractive slapd",
  ])

  # check
  dn = f"cn={ini.ldap.admin_name},dc={ini.ldap.domain_unit_names[0]},dc={ini.ldap.domain_unit_names[1]}"
  ubuntu_0.execs([
    f"systemctl check slapd",
    f"sudo slapcat",
    # -D: bindDN(Distinguished Name)
    # -w: password
    # -x: simple authenitcation
    # -d: debug level
    f"ldapsearch -x '(objectclass=*)'",
    f"""
    ldapsearch -x -D "{dn}" -w "{ini.ldap.tmp_admin_password}"
    """,
    # show trace
    f"""
    ldapsearch -x -D "{dn}" -w "{ini.ldap.tmp_admin_password}" -d -1
    """,
    f"""
    ldapsearch -D "{dn}" -Y EXTERNAL -H "{ini.ldap.url}"
    """
    f"journalctl -u named | tee /dev/null",
  ])

  # change password for security
  ldif_file="admin_pass.ldif"
  ubuntu_0.execs([
    f"""cat <<EOF > {ldif_file}
# Admin schema password
dn: {dn}
changetype: modify
replace: userPassword
userPassword: `slappasswd -s {ini.ldap.admin_password}`
  EOF
"""
  ])
  wait.seconds(2)
  ubuntu_0.execs([
    f"ldapadd -Y EXTERNAL -H {ini.ldap.url} -f {ldif_file}"
  ])

  print("####### exec #######")
  cml = Cml()
  #pcap = cml.lab.create_pcap(iosvl2_0.name, server_0.name, auth_token=cml.auth_token)

if __name__ == '__main__':
  main()
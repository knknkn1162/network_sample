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
slapd slapd/internal/adminpw password {ini.ldap.admin.password}
slapd slapd/internal/generated_adminpw password {ini.ldap.admin.password}
slapd slapd/password1 password {ini.ldap.admin.password}
slapd slapd/password2 password {ini.ldap.admin.password}
slapd slapd/domain string {ini.ldap.admin.domain_name}
slapd shared/organization string {ini.ldap.admin.organization}
EOF
"""
  ])
  wait.seconds(2)
  ubuntu_0.execs([
    f"sudo dpkg-reconfigure -f noninteractive slapd",
  ])

  # check
  search_dn = f"dc={ini.ldap.admin.domain_unit_names[0]},dc={ini.ldap.admin.domain_unit_names[1]}"
  ubuntu_0.execs([
    f"systemctl check slapd",
    f"sudo slapcat",
    # -D: bindDN(Distinguished Name)
    # -b: base DN for search
    # -w: password
    # -x: simple authenitcation
    # -d: debug level
    f"ldapsearch -x -D '{ini.ldap.admin.dn}' -w '{ini.ldap.admin.password}' -b '{search_dn}'",
  ])

  ldif_file = "add.ldif"
  root_dn = f"ou=people,dc={ini.ldap.admin.domain_unit_names[0]},dc={ini.ldap.admin.domain_unit_names[1]}"
  hash01 = ubuntu_0.exec(f"slappasswd -s {ini.ldap.user01.password}").strip()
  hash02 = ubuntu_0.exec(f"slappasswd -s {ini.ldap.user02.password}").strip()
  ubuntu_0.execs([
    f"""cat <<EOF > {ldif_file}
# organizationalUnit:
# mandatory: ou
dn: {root_dn}
objectClass: organizationalUnit
ou: people

# person:
# Mandatory: sn, cn
# Optional: userPassword, telephoneNumber, seeAlso, description
dn: cn={ini.ldap.user01.cn},{root_dn}
objectClass: person
cn: {ini.ldap.user01.cn}
# Surname
sn: {ini.ldap.user01.sn}
userPassword: {hash01}

dn: cn={ini.ldap.user02.cn},{root_dn}
objectClass: person
cn: {ini.ldap.user02.cn}
# Surname
sn: {ini.ldap.user02.sn}
userPassword: {hash02}
EOF
"""
  ])

  wait.seconds(2)
  search_dn01 = f"dc={ini.ldap.admin.domain_unit_names[0]},dc={ini.ldap.admin.domain_unit_names[1]}"
  search_dn02 = f"ou=people,{search_dn01}"
  user01_dn = f"cn={ini.ldap.user01.cn},{search_dn02}"
  user02_dn = f"cn={ini.ldap.user02.cn},{search_dn02}"
  ubuntu_0.execs([
    f"sudo ldapadd -x -D '{ini.ldap.admin.dn}' -w '{ini.ldap.admin.password}' -f {ldif_file}",
    f"sleep 3",
    # check
    f"ldapsearch -D '{ini.ldap.admin.dn}' -w '{ini.ldap.admin.password}' -b '{search_dn01}'",
    f"ldapsearch -D '{ini.ldap.admin.dn}' -w '{ini.ldap.admin.password}' -b '{search_dn02}'",
    f"ldapsearch -D '{ini.ldap.admin.dn}' -w '{ini.ldap.admin.password}' -b '{user01_dn}'",
    f"ldapsearch -D '{user01_dn}' -w '{ini.ldap.user01.password}' -b '{user01_dn}'",
    f"ldapsearch -D '{user01_dn}' -w '{ini.ldap.user01.password}' -b '{search_dn01}'",
    f"ldapsearch -D '{user01_dn}' -w '{ini.ldap.user01.password}' -b '{user02_dn}'",
  ])

if __name__ == '__main__':
  main()
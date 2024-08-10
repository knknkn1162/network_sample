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
slapd slapd/internal/adminpw password {ini.ldap.admin.tmp_password}
slapd slapd/internal/generated_adminpw password {ini.ldap.admin.tmp_password}
slapd slapd/password1 password {ini.ldap.admin.tmp_password}
slapd slapd/password2 password {ini.ldap.admin.tmp_password}
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
    f"ldapsearch -x -D '{ini.ldap.admin.dn}' -w '{ini.ldap.admin.tmp_password}' -b '{search_dn}'",
    # -L: print responses in LDIFv1 format
    f"ldapsearch -x -L -D '{ini.ldap.admin.dn}' -w '{ini.ldap.admin.tmp_password}' -b '{search_dn}'",
    # show trace
    f"ldapsearch -x -D '{ini.ldap.admin.dn}' -w '{ini.ldap.admin.tmp_password}' -b '{search_dn}' -d -1",
    f"ldapsearch -D '{ini.ldap.admin.dn}' -b '{search_dn}' -Y EXTERNAL -H '{ini.ldap.url}'",
    f"ldapwhoami -x -vvv -H '{ini.ldap.url}' -D '{ini.ldap.admin.dn}' -w '{ini.ldap.admin.tmp_password}'",
    f"journalctl -u slapd | tee /dev/null",
  ])

  # set config password
  ldif_file="config.ldif"
  hash = ubuntu_0.exec(f"slappasswd -s {ini.ldap.config.password}")
  ubuntu_0.execs([
    f"""cat <<EOF > {ldif_file}
dn: olcDatabase={{0}}config,cn=config
changetype: modify
# set config password
add: olcRootPW
olcRootPW: {hash.strip()}
EOF
"""
  ])
  wait.seconds(2)
  # $ sudo ls -R /etc/ldap/slapd.d/cn\=config
  # '/etc/ldap/slapd.d/cn=config':
  # 'cn=module{0}.ldif'  'olcDatabase={-1}frontend.ldif'
  # 'cn=schema'          'olcDatabase={0}config.ldif'
  # 'cn=schema.ldif'     'olcDatabase={1}mdb.ldif'

  # '/etc/ldap/slapd.d/cn=config/cn=schema':
  # 'cn={0}core.ldif'    'cn={2}nis.ldif'
  # 'cn={1}cosine.ldif'  'cn={3}inetorgperson.ldif'
  search_dn = "olcDatabase={0}config,cn=config"
  ubuntu_0.execs([
    # Insufficient access (50)
    f"sudo ldapadd  -x -D '{ini.ldap.admin.dn}' -w {ini.ldap.admin.tmp_password} -f {ldif_file}",
    f"sudo ldapadd -H {ini.ldap.url} -Y EXTERNAL -f {ldif_file}",
    #f"ldapwhoami -x -vvv -H '{ini.ldap.url}' -D '{ini.ldap.config.dn}' -w '{ini.ldap.config.password}'",
    f"ldapsearch -x -b '{search_dn}' -D '{ini.ldap.config.dn}' -w '{ini.ldap.config.password}'",
  ])

  ## change root password for security reason
  ldif_file="admin_pass.ldif"
  hash = ubuntu_0.exec(f"slappasswd -s {ini.ldap.admin.password}")
  ubuntu_0.execs([
    f"""cat <<EOF > {ldif_file}
# Admin schema password
dn: olcDatabase={{1}}mdb,cn=config
changetype: modify
replace: olcRootPW
olcRootPW: {hash.strip()}
EOF
"""
  ])
  wait.seconds(2)

  # check
  search_dn = f"dc={ini.ldap.admin.domain_unit_names[0]},dc={ini.ldap.admin.domain_unit_names[1]}"
  ubuntu_0.execs([
    # expected error
    f"ldapsearch -x -D '{ini.ldap.admin.dn}' -w '{ini.ldap.admin.password}' -b '{search_dn}'",
    # change admin password(by simple authe)
    f"sudo ldapmodify -x -D '{ini.ldap.config.dn}' -w '{ini.ldap.config.password}' -f {ldif_file}",
    # f"sudo ldapmodify -Y EXTERNAL -H {ini.ldap.url} -f {ldif_file}",
    f"ldapsearch -x -D '{ini.ldap.admin.dn}' -w '{ini.ldap.admin.password}' -b '{search_dn}'",
  ])

if __name__ == '__main__':
  main()
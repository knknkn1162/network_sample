from cml import Cml
import cml
import yaml

lab = Cml().lab

pyats_testbed = lab.get_pyats_testbed(hostname=f"{cml.CONTROLLER_NAME}:{cml.CONTROLLER_PORT}")

data = yaml.safe_load(pyats_testbed)
data['devices']['terminal_server']['credentials']['default'] = {
  "username": cml.CML_USER, 'password': cml.PASSWORD
}

del data['devices']['iosvl2']['credentials']

with open(cml.CONFIG_YAML, "w") as f: 
    f.write(yaml.dump(data))
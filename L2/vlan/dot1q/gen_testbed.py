from cml import Cml
import cml
import yaml

lab = Cml().lab

pyats_testbed = lab.get_pyats_testbed(hostname=f"{cml.CONTROLLER_NAME}:{cml.CONTROLLER_PORT}")

data = yaml.safe_load(pyats_testbed)
data['devices']['terminal_server']['credentials']['default'] = {
  "username": cml.CML_USER, 'password': cml.PASSWORD
}
for elem in ['iosv', 'iosvl2' 'iosvl2_0', 'iosvl2_1', 'iosvl2_2', 'iosvl2_3', 'iosvl2_4', 'iosvl2_5',
             'iosv_0', 'iosv_1', 'iosv_2', 'iosv_3', 'iosv_4', 'iosv_5']:
  if data['devices'].get(elem) is None:
     continue
  del data['devices'][elem]['credentials']

with open(cml.CONFIG_YAML, "w") as f: 
    f.write(yaml.dump(data))
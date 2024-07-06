import os
from dotenv import load_dotenv
from virl2_client import ClientLibrary, models
from virl2_client.models.authentication import TokenAuth
import requests, time
import datetime
import logging
from yaml import safe_load, dump
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

# .envファイルの内容を読み込見込む
load_dotenv()
URL=os.environ['URL']
CML_USER=os.environ['CML_USER']
PASSWORD=os.environ['PASSWORD']
LAB_NAME=os.environ['LAB_NAME']
CONFIG_YAML=os.environ['CONFIG_YAML']
CONTROLLER_NAME=os.environ['CONTROLLER_NAME']
CONTROLLER_PORT=os.environ['CONTROLLER_PORT']

class Cml:
  def __init__(self):
    self.conn = ClientLibrary(URL, CML_USER, PASSWORD, ssl_verify=False)
    self.auth_token = TokenAuth(self.conn).token
    logger.debug(f"token: {self.auth_token}")
    self.lab = self._find_or_create_lab(LAB_NAME)
    logger.debug(f"lab_id: {self.lab.id}")
    
  def _find_or_create_lab(self, title: str):
    labs = self.conn.find_labs_by_title(title)
    if len(labs) == 0:
      return Lab(self.conn.create_lab(title))
    return Lab(labs[0])

class Node:
  def __init__(self, node: models.Node, interfaces: list[models.Interface]):
    self.node = node
    self.lab = Lab(node.lab)
    self.kind = node.node_definition
    self.label = self.node.label
    self.interfaces = interfaces
    if self.kind in ["iosv", "iosvl2"]:
      self.set_hostname(self.node.label)

  def __getitem__(self, idx: int):
    return self.interface(idx)
  
  def interface(self, idx: int):
    return self.interfaces[idx]
  def set_config(self, conf: str):
    self.node.config = conf
  def set_hostname(self, hostname: str):
    self.set_config(
      f"hostname {hostname}"
    )
  
  def create_links(self, interfaces: list[models.Interface]) -> list[models.Interface]:
    return [self.lab.find_or_create_link(i1, i2) for i1, i2 in zip(self.interfaces, interfaces)]

class Lab:
  def __init__(self, lab: models.Lab):
    self.lab = lab
    self.id = lab.id

  def get_link_by_nodes(self, node1: str, node2: str):
    return self.lab.get_link_by_nodes(
      self._get_node_by_label(node1),
      self._get_node_by_label(node2)
    )
  
  def find_or_create_link(self, i1: models.Interface, i2: models.Interface) -> models.Link:
    if i1.connected or i2.connected:
      return i1.get_link_to(i2)
    return self.lab.create_link(i1, i2)

  def print_nodes(self):
    for node in self.lab.nodes():
        print(vars(node))
  
  def create_server(self, label: str, xpos: int, ypos: int, slots: int) -> Node:
    return self._create_node(label, "server", xpos, ypos, slots)
  
  def create_iosv(self, label: str, xpos: int, ypos: int, slots: int) -> Node:
    return self._create_node(label, "iosv", xpos, ypos, slots)
  
  def create_iosvl2(self, label: str, xpos: int, ypos: int, slots: int) -> Node:
    return self._create_node(label, "iosvl2", xpos, ypos, slots)
  
  def create_unmanaged_switch(self, label: str, xpos: int, ypos: int, slots: int) -> Node:
    return self._create_node(label, "unmanaged_switch", xpos, ypos, slots)

  def _create_node(self, label: str, type0: str, xpos: int, ypos: int, slots: int) -> Node:
    node = self.lab.create_node(label, type0, xpos, ypos)
    interfaces = [node.create_interface(slot=i) for i in range(slots)]
    return Node(node, interfaces)
  
  def _get_node_by_label(self, node: str):
    return self.lab.get_node_by_label(node)
  
  def start(self, wait_time=15):
    logger.info("start!")
    self.lab.start(wait=False)
    logger.info(f"sleep {wait_time}[s]")
    time.sleep(wait_time)

  def delete_all(self, is_wipe=True):
    self.lab.stop()
    if is_wipe:
      self.lab.wipe()
    self.lab.remove()

  def gen_testbed(self):
    hostname = f"{CONTROLLER_NAME}:{CONTROLLER_PORT}"
    pyats_testbed = self.lab.get_pyats_testbed(hostname)

    data = safe_load(pyats_testbed)
    data['devices']['terminal_server']['credentials']['default'] = {
      "username": CML_USER,
      'password': PASSWORD,
    }
    for key, _ in data['devices'].items():
      if str(key).startswith('iosv'):
        del data['devices'][key]['credentials']

    with open(CONFIG_YAML, "w") as f: 
        f.write(dump(data))

class Pcap:
  def __init__(self, cml: Cml, node1: str, node2: str):
    self.cml = cml
    self.node1 = node1
    self.node2 = node2
    self.link = cml.get_link_by_nodes(node1, node2)
    logger.debug(f"link_id: {self.link.id}")
    self.lab = self.cml.lab
    self.auth_token = self.cml.auth_token
    self.endpoint = f"{URL}/api/v0"
    self.headers = {
      "Authorization": f"Bearer {self.auth_token}",
      "Content-Type": "application/json"
    }
    self.key = None

  def start(self, maxpackets=50):
    api_url = f"{self.endpoint}/labs/{self.lab.id}/links/{self.link.id}/capture/start"
    logger.info(api_url)
    logger.info(datetime.datetime.now())
    res = requests.put(api_url,
      headers = self.headers,
      json={
        "maxpackets": maxpackets,
      }
    )
    api_url = f"{self.endpoint}/labs/{self.lab.id}/links/{self.link.id}/capture/status"
    logger.info(api_url)
    res = requests.get(api_url,
      headers = self.headers
    )
    data = res.json()
    self.key = data.get("config", {}).get("link_capture_key", {})
    return data

  def stop(self):
    api_url = f"{self.endpoint}/labs/{self.lab.id}/links/{self.link.id}/capture/stop"
    logger.info(api_url)
    res = requests.put(api_url,
      headers = self.headers
    )
    return res

  def download(self, file: str):
    if self.key is None:
      raise Exception("key not found")
    api_url = f"{self.endpoint}/pcap/{self.key}"
    logger.info(api_url)
    res = requests.get(api_url,
      headers = self.headers
    )
    with open(file, "wb") as f:
      f.write(res.content)
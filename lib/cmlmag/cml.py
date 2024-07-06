import os
from dotenv import load_dotenv
from virl2_client import ClientLibrary, models
from virl2_client.models.authentication import TokenAuth
import requests, time
import datetime
import logging
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
    self.lab = self.find_or_create_lab(LAB_NAME)
    logger.debug(f"lab_id: {self.lab.id}")
    
  def find_or_create_lab(self, title):
    labs = self.conn.find_labs_by_title(title)
    if len(labs) == 0:
      return Lab(self.conn.create_lab(title))
    return Lab(labs[0])

class Lab:
  def __init__(self, lab: models.Lab):
    self.lab = lab

  def get_link_by_nodes(self, node1: str, node2: str):
    return self.lab.get_link_by_nodes(
      self._get_node_by_label(node1),
      self._get_node_by_label(node2)
    )
  
  def create_server(self, label: str, xpos: int, ypos: int):
    return self._create_node(label, "server", xpos, ypos)
  
  def create_iosv(self, label: str, xpos: int, ypos: int):
    return self._create_node(label, "iosv", xpos, ypos)
  
  def create_iosvl2(self, label: str, xpos: int, ypos: int):
    return self._create_node(label, "iosvl2", xpos, ypos)
  
  def create_unmanaged_switch(self, label: str, xpos: int, ypos: int):
    return self._create_node(label, "unmanaged_switch", xpos, ypos)

  def _create_node(self, label: str, type0: str, xpos: int, ypos: int):
    return self.lab.create_node(label, type0, xpos, ypos)
  
  def _get_node_by_label(self, node: str):
    return self.lab.get_node_by_label(node)



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

class Lab:
  def __init__(self, lab):
    self.lab = lab
  def start(self):
    self.lab.start(wait=False)
    logger.info("sleep..")
    time.sleep(10)
  def delete_all(self):
    self.lab.stop()
    self.lab.wipe()
    self.lab.remove()
import os
from dotenv import load_dotenv
from virl2_client import ClientLibrary
from virl2_client.models.authentication import TokenAuth
import requests

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
    print(URL, CML_USER)
    self.conn = ClientLibrary(URL, CML_USER, PASSWORD, ssl_verify=False)
    self.auth_token = TokenAuth(self.conn).token
    self.lab = self.find_or_create_lab(LAB_NAME)
    
  def find_or_create_lab(self, title):
    labs = self.conn.find_labs_by_title(title)
    if len(labs) == 0:
      return self.conn.create_lab(title)
    return labs[0]

  def get_link_by_nodes(self, node1: str, node2: str):
    lab = self.lab
    return lab.get_link_by_nodes(
      lab.get_node_by_label(node1),
      lab.get_node_by_label(node2)
    )

class Pcap:
  def __init__(self, cml: Cml, node1: str, node2: str):
    self.cml = cml
    self.node1 = node1
    self.node2 = node2
    self.link = cml.get_link_by_nodes(node1, node2)
    print(f"link_id: {self.link.id}, link: {self.link}")
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
    print(api_url)
    res = requests.put(api_url,
      headers = self.headers,
      json={
        "maxpackets": maxpackets,
      },
      verify = False
    )
    api_url = f"{self.endpoint}/labs/{self.lab.id}/links/{self.link.id}/capture/status"
    print(api_url)
    res = requests.get(api_url,
      headers = self.headers,
      verify = False
    )
    data = res.json()
    self.key = data.get("config", {}).get("link_capture_key", {})
    return data

  def stop(self):
    api_url = f"{self.endpoint}/labs/{self.lab.id}/links/{self.link.id}/capture/stop"
    print(api_url)
    res = requests.put(api_url,
      headers = self.headers,
      verify = False
    )
    return res

  def _download(self, file: str):
    if self.key is None:
      raise Exception("key not found")
    api_url = f"{self.endpoint}/pcap/{self.key}"
    print(api_url)
    res = requests.get(api_url,
      headers = self.headers,
      verify = False
    )
    with open(file, "wb") as f:
      f.write(res.content)
  def download(self, file: str):
    self.stop()
    self._download(file)
  
class Lab:
  def __init__(self, lab):
    self.lab = lab
  
  def delete_all(self):
    self.lab.stop()
    self.lab.wipe()
    self.lab.remove()
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
    self.conn = ClientLibrary(URL, CML_USER, PASSWORD, ssl_verify=False)
    self.auth_token = TokenAuth(self.conn).token
    self.lab = self.find_or_create_lab(LAB_NAME)
    self.endpoint = f"{URL}/api/v0"
    self.headers = {
      "Authorization": f"Bearer {self.auth_token}",
      "Content-Type": "application/json"
    }
    
  def find_or_create_lab(self, title):
    labs = self.conn.find_labs_by_title(title)
    if len(labs) == 0:
      return self.conn.create_lab(title)
    return labs[0]
  
  def start_pcap(self, link, maxpackets=50):
    api_url = f"{self.endpoint}/labs/{self.lab.id}/links/{link.id}/capture/start"
    print(api_url)
    res = requests.put(api_url,
      headers = self.headers,
      json={
        "maxpackets": maxpackets,
      }
    )
    api_url = f"{self.endpoint}/labs/{self.lab.id}/links/{link.id}/capture/status"
    print(api_url)
    res = requests.get(api_url,
      headers = self.headers
    )
    return res.json()
  
  def download_pcap(self, link_capture_key: str):
    api_url = f"{self.endpoint}/pcap/{link_capture_key}"
    print(api_url)
    res = requests.get(api_url,
      headers = self.headers
    )
    return res.content
  
class Lab:
  def __init__(self, lab):
    self.lab = lab
  
  def delete_all(self):
    self.lab.stop()
    self.lab.wipe()
    self.lab.remove()
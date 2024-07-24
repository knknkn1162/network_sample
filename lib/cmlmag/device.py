from .structure.node import NodeType
import logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

class Device:
  def __init__(self, tb, name: str):
    self.tb = tb
    self.name = name
    self.kind = self.get_kind()
    self.conn = self.tb.devices[name]
    self.conn.connect()

  def get_kind(self):
    if(self.name.startswith('iosv')):
      return NodeType.iosv
    elif(self.name.startswith('iosvl2')):
      return NodeType.iosvl2
    elif(self.name.startswith('server')):
      return NodeType.server
    elif(self.name.startswith('switch')):
      return NodeType.unmanaged_switch
    
  def is_connected(self):
    return self.conn.is_connected()

  def exec(self, cmd: str):
    return self.conn.execute(cmd)
  
  def execs(self, cmds: list[str | object]):
    print(f"#### device {self.name} ####")
    res = []
    for cmd in cmds:
      if type(cmd) is str:
        res.append(self.conn.execute(cmd))
      elif isinstance(cmd, list):
        res.append(self.conn.configure(cmd))
      else:
        Exception(f"error execs @ ${cmd}")
    return res

  def parse(self, cmd):
    data = self.conn.parse(cmd, continue_on_failure=True)
    logger.debug(data)
    return data
  
  def server_ping(self, target_ip: str, count: int=5):
    res: list[str] = self.execs([
      f"ping {target_ip} -c {count}",
      f"echo $?",
    ])
    return int(res[1].strip())

  def vpcs_ping(self, target_ip: str, count: int=5):
    res: list[str] = self.execs([
      f"ping {target_ip} -c {count}",
    ])
    return res

  def router_ping(self, target_ip: str, count: int=5):
    res = self.execs([
      f"ping {target_ip} repeat {count}",
    ])
    return res[0]

  def show_mac_ip(self):
    return self.execs([
      f"show interfaces | i (.* line protocol is )|(.* address is)",
    ])

  def show_ospf_neighbor(self):
    return self.execs([
      f"show ip ospf neighbor"
    ])
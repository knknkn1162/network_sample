class Device:
  def __init__(self, tb, name):
    self.tb = tb
    self.name = name
    self.conn = self.tb.devices[name]
    self.conn.connect()

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
    return self.conn.parse(cmd, continue_on_failure=True)
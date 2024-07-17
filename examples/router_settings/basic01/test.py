from genie import testbed
from cmlmag.cml import CONFIG_YAML, Cml
from cmlmag.device import Device
from cmlmag import wait, ipv4
import cmlmag.parse as parse
import cmlmag.wait_until as wait_until
import ini
from cmlmag.structure.stp_info import (
  Role as StpRole,
  State as StpState
)

def main():
  tb = testbed.load(CONFIG_YAML)
  # switch
  iosv_0 = Device(tb, ini.iosv_0.__name__)

  print("####### exec #######")
  cml = Cml()

  iosv_0.execs([
    [
      f"no ip domain-lookup",  
    ],
    f"dummy",
  ])

  iosv_0.execs([
    [
      f"line console 0",
      # console 常にlogが出た場合でも元の入力文字列を保存してくれる
      #f"logging synchronous",
    ],
  ])



if __name__ == '__main__':
  main()
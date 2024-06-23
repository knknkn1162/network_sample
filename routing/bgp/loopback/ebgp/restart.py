from cml import Cml
import ini as ini
import time

cml = Cml()
lab = cml.lab
print("stop...")
lab.stop()
lab.wipe()
print("start...")
lab.start(wait=False)
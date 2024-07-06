from cml import Cml
import ini as ini

cml = Cml()
lab = cml.lab
print("stop...")
lab.stop()
lab.wipe()
print("start...")
lab.start()
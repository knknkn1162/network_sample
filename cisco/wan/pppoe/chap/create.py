from cmlmag.cml import Cml
import ini as ini
import time

def main():
    cml = Cml()
    lab = cml.lab

    r1 = lab.create_iosv(ini.iosv_1.__name__, 700, 700, slots=1)
    r2 = lab.create_iosv(ini.iosv_2.__name__, 1000, 400, slots=2)

    r2.create_links([r1[0]])
    r1.create_links([r2[0]])
    
    lab.start()

    # print nodes and interfaces states:
    lab.print_nodes()

if __name__ == '__main__':
    main()
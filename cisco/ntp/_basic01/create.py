from cmlmag.cml import Cml
import ini as ini
import time

def main():
    cml = Cml()
    lab = cml.lab

    r0 = lab.create_iosv(ini.iosv_0.__name__, 400, 400, slots=2)
    r1 = lab.create_iosv(ini.iosv_1.__name__, 800, 400, slots=2)

    r0.create_links([r1[0]])
    r1.create_links([r0[0]])

    lab.start()

    # print nodes and interfaces states:
    lab.print_nodes()

if __name__ == '__main__':
    main()
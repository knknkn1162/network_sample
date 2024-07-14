from cmlmag.cml import Cml
import ini as ini
import time

def main():
    cml = Cml()
    lab = cml.lab

    r0 = lab.create_iosvl2(ini.iosvl2_0.__name__, 200, 200, slots=2)
    r1 = lab.create_iosvl2(ini.iosvl2_1.__name__, 200, 700, slots=2)

    r0.create_links([r1[0], r1[1]])
    r1.create_links([r0[0], r0[1]])

    lab.start()

    # print nodes and interfaces states:
    lab.print_nodes()

if __name__ == '__main__':
    main()
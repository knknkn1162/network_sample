from cmlmag.cml import Cml
import ini as ini
import time

def main():
    cml = Cml()
    lab = cml.lab

    r0 = lab.create_iosv(ini.iosv_0.__name__, 400, 600, slots=3)
    r1 = lab.create_iosv(ini.iosv_1.__name__, 700, 600, slots=3)
    c0 = lab.create_server(ini.server_0.__name__, 200, 200, slots=1)
    c1 = lab.create_server(ini.server_1.__name__, 200, 1000, slots=1)
    c2 = lab.create_server(ini.server_2.__name__, 1000, 200, slots=1)
    c3 = lab.create_server(ini.server_3.__name__, 1000, 1000, slots=1)

    c0.create_links([r0[0]])
    c1.create_links([r0[1]])
    c2.create_links([r1[0]])
    c3.create_links([r1[1]])
    r0.create_links([c0[0], c1[0], r0[2]])
    r1.create_links([c2[1], c3[1], r1[2]])

    lab.start()

    # print nodes and interfaces states:
    lab.print_nodes()

if __name__ == '__main__':
    main()
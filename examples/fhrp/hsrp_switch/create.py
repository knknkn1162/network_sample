from cmlmag.cml import Cml
import ini as ini
import time

def main():
    cml = Cml()
    lab = cml.lab

    r0 = lab.create_iosvl2(ini.iosvl2_0.__name__, 700, 200, slots=2)
    r1 = lab.create_iosvl2(ini.iosvl2_1.__name__, 700, 700, slots=2)
    r2 = lab.create_iosv(ini.iosv_0.__name__, 1000, 400, slots=2)


    s0 = lab.create_unmanaged_switch(ini.sw_0.__name__, 400, 700, slots=4)
    c0 = lab.create_server(ini.server_0.__name__, 100, 200, slots=1)
    c1 = lab.create_server(ini.server_1.__name__, 100, 700, slots=1)

    c0.create_links([s0[0]])
    c1.create_links([s0[1]])
    s0.create_links([c0[0], c1[0], r0[0], r1[0]])
    r0.create_links([s0[2], r2[0]])
    r1.create_links([s0[3], r2[1]])
    r2.create_links([r0[1], r1[1]])

    lab.start()

    # print nodes and interfaces states:
    lab.print_nodes()

if __name__ == '__main__':
    main()